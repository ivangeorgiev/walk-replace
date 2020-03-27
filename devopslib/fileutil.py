import os
import glob
import re
import enum
import string
import configparser


class SubstituteMethod(enum.Enum):
    PLAINTEXT = 'plaintext'
    TEMPLATE = 'template'

def search_files(pattern:str, abspath:bool=True, recursive:bool=True):
    """Search files using match one or more match pattern.

    Supported pattern separators: ",", ";", ":", "\n"
    Separators can be mixed.

    Example Patterns
    ----------------
    patterns1 = "*.txt;*.py"
    patterns2 = "input/**/*"
    """

    def filter_entry(entry):
        for filter in filter_list:
            entry = filter(entry)
            if not entry:
                break
        return entry

    filter_list = []
    filter_list.append(lambda entry: entry if os.path.isfile(entry) else None)
    filter_list.append(os.path.abspath if abspath else lambda entry: entry)
    patterns = [p for pl in pattern.splitlines() for p in re.split(',|:|;', pl)]
    result = [entry
        for entry in
        [filter_entry(entry) for this_pattern in patterns
            for entry in glob.iglob(this_pattern, recursive=recursive)]
        if entry
    ]
    return set(result)


def read_config(config_filepath:str,
                env_vars:str=None,
                env_vars_section:str='ENV',
                env_vars_upper:bool=True):
    """Read configuration file, passing given list of 
    environment variables as settings from ENV section.

    Params:
    -------
    config_filepath - Path to the config file

    env_vars - List of environment variables to be passed.
        Supported separators: ",", ":", ";"
        If empty or None, no environment variables will be passed.

    env_vars_section - Environment variables will be passed to 
        this section.

    env_vars_upper - If set to True, environment variable
        names will be converted to upper case before accessed from the
        environment.
    """
    
    def read_env_vars(env_vars):
        if isinstance(env_vars, str):
            env_vars = re.split(",|:|;", env_vars)
        if '*' in env_vars:
            env_vars = os.environ.keys()
        else:
            env_vars = [var.strip() for var in env_vars]
            if env_vars_upper:
                env_vars = [var.upper() for var in env_vars]
        env_dict = {var_name.replace('$', '$$'): os.environ[var_name].replace('$', '$$')   for var_name in env_vars }
        config.read_dict({env_vars_section: env_dict})

    if not os.path.isfile(config_filepath):
        raise FileNotFoundError(f"Config file not found: {config_filepath}")
    config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation()
                )
    if env_vars: read_env_vars(env_vars)
    config.read(config_filepath)
    return config

def _substitute_plaintext(content:str, mapping:dict):
    """Substitute, using plaintext search and replace."""
    for search, replace in mapping.items():
        content = content.replace(search, replace)
    return content

def _substitute_template(content:str, mapping:dict):
    """Substitute, using Python's Template."""
    template = string.Template(content)
    return template.substitute(mapping)

def _get_substitute_handler(method:SubstituteMethod):
    """Get callable substitute handler for given method."""
    handler_function_name = "_substitute_" + method.name.lower()
    substitute_handler = globals()[handler_function_name]
    return lambda content, mapping: substitute_handler(content, mapping)

def text_substitute(file_path:str, mapping:dict, method:SubstituteMethod=SubstituteMethod.PLAINTEXT):
    """Perform in-place text substition for a file using given search-replace mapping."""
    with open(file_path, 'r') as file:
        content = file.read()
    result = _get_substitute_handler(method)(content, mapping)
    with open(file_path, 'w') as file:
        file.write(result)

def pivot_mapping(mapping:dict, key_prefix:str='key.', value_prefix:str='value.'):
    """Convert pivoted mapping into simple mapping.

    Example:
    >>> input_map = {
    ...              'search.name': '<name>',
    ...              'replace.name': 'John',
    ...              'search.age': '<age>',
    ...              }
    >>> pivot_mapping(input_map, 'search.', 'replace.')
    {'<name>': 'John', '<age>': ''}
    """
    result = {}
    for key, value in mapping.items():
        if not key.startswith(key_prefix):
            continue
        key_name = key[len(key_prefix):]
        result[value] = mapping.get(value_prefix + key_name, '')
    return result

if __name__ == '__main__': # pragma: no cover
    import doctest
    doctest.testmod()
