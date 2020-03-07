#%%
import configparser
import pytest

#%%
# Documentation example
# https://docs.python.org/3/library/configparser.html#customizing-parser-behaviour

parser = configparser.ConfigParser()
parser.read_dict({'section1': {'key1': 'value1',
                               'key2': 'value2',
                               'key3': 'value3'},
                  'section2': {'keyA': 'valueA',
                               'keyB': 'valueB',
                               'keyC': 'valueC'},
                  'section3': {'foo': 'x',
                               'bar': 'y',
                               'baz': 'z'}
})
parser.sections()
[option for option in parser['section3']]

#%%
# Trying ExtendedInterpolation with defaults
defaults = dict(days=1)

config = { 'vars': {'name': 'Fox',
                    'greeting': 'Hello ${name}',
                    'name-replaced-current-section': '${name}',
                    'name-replaced-from-section': '${vars:name}',
                    'days-replaced-from-defaults': '${days}'}
}

parser = configparser.ConfigParser(
    defaults=defaults,
    interpolation=configparser.ExtendedInterpolation()
)
parser.read_dict(config)

dict(parser['vars'])
#%%
# ConfigParser interpolation with environment vars as defaults
import os
os.environ['CONFIG_PARSER_SECRET'] = 'very secret'
os.environ['CONFIG_PARSER_$ECRET'] = '$ecret'
defaults = {}
defaults.update({k: v.replace('$', '$$') for k,v in os.environ.items() })


config = { 'data': {'interpolated-from-env': '${CONFIG_PARSER_SECRET}'}} # { 'env': os.environ }
parser = configparser.ConfigParser(
    defaults=defaults,
    interpolation=configparser.ExtendedInterpolation()
)

parser.read_dict(config)

dict(parser['data'])

#%%
# ConfigParser interpolation with environment vars as ENV section
import os
os.environ['CONFIG_PARSER_SECRET'] = 'very secret'
os.environ['CONFIG_PARSER_$ECRET'] = '$ecret'
defaults = {}

env = {k: v.replace('$', '$$') for k,v in os.environ.items() }


config = { 'data': {'interpolated-from-env': '${ENV:CONFIG_PARSER_SECRET}'},
                    # NOTE: Following is not supported
                    # 'interpolated-from-env-$': '${ENV:CONFIG_PARSER_$ECRET}'
                   }

parser = configparser.ConfigParser(
    defaults=defaults,
    interpolation=configparser.ExtendedInterpolation()
)

parser.read_dict({'ENV': env})
parser.read_dict(config)

dict(parser['data'])




# %%
