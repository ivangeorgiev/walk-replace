"""Walk and replace functions."""

import os
import re
import configparser
from enum import Enum
from string import Template

class SubstituteMode(Enum):
    """Substitute mode enum"""
    PLAINTEXT = 'plaintext'
    INTERPOLATE = 'interpolate'

def read_file_content(file_path):
    """Read the entire content of a file."""
    with open(file_path, 'r') as infile:
        return infile.read()

def regex_match(regex):
    """Get a regex matcher function."""
    return lambda x: bool(re.match(regex, x))


def walk_dir(dir_path, include_match='.*'):
    """Walk a directory and subdirectories and yield file paths found."""
    def is_included(path):
        return include_match(path)

    if isinstance(include_match, str):
        include_match = regex_match(include_match)

    for (this_dir, _, file_names) in os.walk(dir_path):
        for file_name in file_names:
            file_path = (f"{this_dir}/{file_name}").replace('\\', '/')
            if is_included(file_path):
                yield file_path

def get_identity():
    """Returns identity function."""
    return lambda x: x

def get_template_filter(mapping, safe=False):
    """Returns a template substitute function.
    """
    def do_filter(content):
        template = Template(content)
        if safe:
            return template.safe_substitute(mapping)
        return template.substitute(mapping)

    return do_filter

def configparser_safe_dict(the_dict):
    """Get a dictionary safe for use in ConfigParser with interpolation."""
    safe_dict = {k: v.replace('$', '$$') for k, v in the_dict.items()}
    return safe_dict

def _get_substitute_handler(substitute_mode, substitute_vars):
    #pylint: disable=possibly-unused-variable
    def plaintext_handler(content):
        for search, replace in substitute_vars.items():
            content = content.replace(search, replace)
        return content
    #pylint: enable=possibly-unused-variable
    handler_name = "{}_handler".format(substitute_mode.name).lower()
    return locals()[handler_name]

#pylint: disable=too-many-arguments
def main(path,
         config_file,
         env_vars=False,
         substitute_config_section='substitute',
         substitute_mode=SubstituteMode.PLAINTEXT,
         include_file_match='.*'):
    """To be used as main"""

    if not os.path.exists(path):
        raise FileNotFoundError(f"Replace path not exists: {path}")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Replace path is not a directory: {config_file}")

    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Config file not found:{config_file}")
    if not os.path.isfile(config_file):
        raise FileNotFoundError(f"Config file is not a file: {config_file}")

    config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation()
                )
    if env_vars:
        env = configparser_safe_dict(os.environ)
        config.read_dict({'ENV':env})
    config.read(config_file)
    substitute_vars = config[substitute_config_section]
    substitute = _get_substitute_handler(substitute_mode, substitute_vars)

    files = walk_dir(path, include_match=include_file_match)
    for filename in files:
        content = read_file_content(filename)
        substituted_content = substitute(content)
        with open(filename, 'w') as outfile:
            outfile.write(substituted_content)
