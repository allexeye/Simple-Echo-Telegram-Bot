import warnings
from os import environ as os_env, path
from os.path import pardir


def _set_from_string(s):
    if s:
        return frozenset(s.split(","))
    return frozenset()


class Config:
    bot_dir = path.abspath(path.dirname(__file__))  # This directory
    bot_project_root = path.abspath(
        path.join(bot_dir, pardir))
    bot_migrations = path.abspath(
        path.join(bot_project_root, "migrations"))
    bot_static = path.abspath(
        path.join(bot_project_root, "bot/static"))


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    sql_url = os_env.get("SQL_URL", "")  # noqa


class TestConfig(Config):
    """Production configuration."""
    ENV = 'test'
    DEBUG = True
    sql_url = os_env.get("SQL_URL", "mysql://root@127.0.0.1:3306/test")  # noqa


_configs = {
    ProdConfig.ENV: ProdConfig,
    TestConfig.ENV: TestConfig,
}


def get(name):
    return _configs.get(name)


_env = os_env.get('ENV')
if not _env:
    warnings.warn('Environment variable ("ENV") not set, "prod" '
                  'environment will be used by default')
    _env = 'prod'
    # _env = 'test'

config = get(_env)
