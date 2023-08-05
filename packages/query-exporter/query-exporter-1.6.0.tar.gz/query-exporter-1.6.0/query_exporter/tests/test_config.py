from operator import attrgetter

import pytest
import yaml

from ..config import (
    ConfigError,
    load_config,
)


@pytest.fixture
def config_full():
    yield {
        'databases': {
            'db': {
                'dsn': 'postgres:///foo'
            }
        },
        'metrics': {
            'm': {
                'type': 'gauge'
            }
        },
        'queries': {
            'q': {
                'interval': 10,
                'databases': ['db'],
                'metrics': ['m'],
                'sql': 'SELECT 1'
            }
        }
    }


@pytest.fixture
def write_config(tmpdir):

    path = tmpdir / 'config'

    def write(data):
        path.write_text(yaml.dump(data), 'utf-8')
        return path

    yield write


CONFIG_UNKNOWN_DBS = {
    'metrics': {
        'm': {
            'type': 'summary'
        }
    },
    'queries': {
        'q': {
            'interval': 10,
            'databases': ['db1', 'db2'],
            'metrics': ['m'],
            'sql': 'SELECT 1'
        }
    }
}

CONFIG_UNKNOWN_METRICS = {
    'databases': {
        'db': {
            'dsn': 'postgres:///foo'
        }
    },
    'queries': {
        'q': {
            'interval': 10,
            'databases': ['db'],
            'metrics': ['m1', 'm2'],
            'sql': 'SELECT 1'
        }
    }
}

CONFIG_MISSING_KEY = {'queries': {'q1': {'interval': 10}}}


class TestLoadConfig:

    def test_load_databases_section(self, write_config):
        """The 'databases' section is loaded from the config file."""
        config = {
            'databases': {
                'db1': {
                    'dsn': 'postgres:///foo'
                },
                'db2': {
                    'dsn': 'postgres:///bar'
                }
            }
        }
        config_file = write_config(config)
        with config_file.open() as fd:
            result = load_config(fd)
        database1, database2 = sorted(result.databases, key=attrgetter('name'))
        assert database1.name == 'db1'
        assert database1.dsn == 'postgres:///foo'
        assert database2.name == 'db2'
        assert database2.dsn == 'postgres:///bar'

    def test_load_metrics_section(self, write_config):
        """The 'metrics' section is loaded from the config file."""
        config = {
            'metrics': {
                'metric1': {
                    'type': 'summary',
                    'description': 'metric one'
                },
                'metric2': {
                    'type': 'histogram',
                    'description': 'metric two',
                    'buckets': [10, 100, 1000]
                }
            }
        }
        config_file = write_config(config)
        with config_file.open() as fd:
            result = load_config(fd)
        metric1, metric2 = sorted(result.metrics, key=attrgetter('name'))
        assert metric1.type == 'summary'
        assert metric1.description == 'metric one'
        assert metric1.config == {'labels': ['database']}
        assert metric2.type == 'histogram'
        assert metric2.description == 'metric two'
        assert metric2.config == {
            'labels': ['database'],
            'buckets': [10, 100, 1000]
        }

    def test_load_databases_missing_dsn(self, write_config):
        """An error is raised if the 'dsn' key is missing for a database."""
        config_file = write_config({'databases': {'db1': {}}})
        with pytest.raises(ConfigError) as err, config_file.open() as fd:
            load_config(fd)
        assert str(err.value) == "Missing key 'dsn' for database 'db1'"

    def test_load_metrics_unsupported_type(self, write_config):
        """An error is raised if an unsupported metric type is passed."""
        config = {
            'metrics': {
                'metric1': {
                    'type': 'info',
                    'description': 'info metric'
                }
            }
        }
        config_file = write_config(config)
        with pytest.raises(ConfigError) as err, config_file.open() as fd:
            load_config(fd)
        assert str(err.value) == "Unsupported metric type: 'info'"

    def test_load_queries_section(self, write_config):
        """The 'queries` section is loaded from the config file."""
        config = {
            'databases': {
                'db1': {
                    'dsn': 'postgres:///foo'
                },
                'db2': {
                    'dsn': 'postgres:///bar'
                }
            },
            'metrics': {
                'm1': {
                    'type': 'summary'
                },
                'm2': {
                    'type': 'histogram'
                }
            },
            'queries': {
                'q1': {
                    'interval': 10,
                    'databases': ['db1'],
                    'metrics': ['m1'],
                    'sql': 'SELECT 1'
                },
                'q2': {
                    'interval': 10,
                    'databases': ['db2'],
                    'metrics': ['m2'],
                    'sql': 'SELECT 2'
                }
            }
        }
        config_file = write_config(config)
        with config_file.open() as fd:
            result = load_config(fd)
        query1, query2 = sorted(result.queries, key=attrgetter('name'))
        assert query1.name == 'q1'
        assert query1.databases == ['db1']
        assert query1.metrics == ['m1']
        assert query1.sql == 'SELECT 1'
        assert query2.name == 'q2'
        assert query2.databases == ['db2']
        assert query2.metrics == ['m2']
        assert query2.sql == 'SELECT 2'

    @pytest.mark.parametrize(
        'config,error_message', [
            (CONFIG_UNKNOWN_DBS, "Unknown databases for query 'q': db1, db2"),
            (CONFIG_UNKNOWN_METRICS, "Unknown metrics for query 'q': m1, m2"),
            (CONFIG_MISSING_KEY, "Missing key 'databases' for query 'q1'")
        ])
    def test_configuration_incorrect(
            self, config, error_message, write_config):
        """An error is raised if configuration is incorrect."""
        config_file = write_config(config)
        with pytest.raises(ConfigError) as err, config_file.open() as fd:
            load_config(fd)
        assert str(err.value) == error_message

    def test_load_queries_missing_interval_default_to_none(self, write_config):
        """If the interval is not specified, it defaults to None."""
        config = {
            'databases': {
                'db': {
                    'dsn': 'postgres:///foo'
                }
            },
            'metrics': {
                'm': {
                    'type': 'summary'
                }
            },
            'queries': {
                'q': {
                    'databases': ['db'],
                    'metrics': ['m'],
                    'sql': 'SELECT 1'
                }
            }
        }
        config_file = write_config(config)
        with config_file.open() as fd:
            config = load_config(fd)
        assert config.queries[0].interval is None

    @pytest.mark.parametrize(
        'interval,value', [
            (10, 10), ('10', 10), ('10s', 10), ('10m', 600), ('1h', 3600),
            ('1d', 3600 * 24), (None, None)
        ])
    def test_load_queries_interval(
            self, interval, value, config_full, write_config):
        """The query interval can be specified with suffixes."""
        config_full['queries']['q']['interval'] = interval
        config_file = write_config(config_full)
        with config_file.open() as fd:
            config = load_config(fd)
        [query] = config.queries
        assert query.interval == value

    def test_load_queries_interval_not_specified(
            self, config_full, write_config):
        """If the interval is not specified, it's set to None."""
        del config_full['queries']['q']['interval']
        config_file = write_config(config_full)
        with config_file.open() as fd:
            config = load_config(fd)
        [query] = config.queries
        assert query.interval is None

    @pytest.mark.parametrize('interval', ['1x', 'wrong', '1.5m', 0, -20])
    def test_load_queries_invalid_interval(
            self, interval, config_full, write_config):
        """An invalid query interval raises an error."""
        config_full['queries']['q']['interval'] = interval
        config_file = write_config(config_full)
        with pytest.raises(ConfigError) as err, config_file.open() as fd:
            load_config(fd)
        assert str(err.value) == "Invalid interval for query 'q'"
