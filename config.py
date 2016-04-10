import logging

try:
    from configparser import ConfigParser
except ImportError:
    # Python 2 support
    from ConfigParser import ConfigParser

config = ConfigParser()
config.readfp(open('config.ini'))
env = 'config'

_cfg = lambda k: config.get(env, k)
_cfgi = lambda k: int(_cfg(k))
