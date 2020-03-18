import os
import glob
import re
import configparser


def search_files(pattern, abspath=True, recursive=True):
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


def read_config(config_filepath,
                env_vars=None,
                env_vars_section='ENV',
                env_vars_upper=True):

    def read_env_vars(env_vars):
        if isinstance(env_vars, str):
            env_vars = re.split(",|:|;", env_vars)
        env_vars = [var.strip() for var in env_vars]
        if env_vars_upper:
            env_vars = [var.upper() for var in env_vars]
        env_dict = {var_name.replace('$', '$$'): os.environ[var_name].replace('$', '$$')   for var_name in env_vars }
        config.read_dict({env_vars_section: env_dict})

    if not os.path.isfile(config_filepath):
        raise FileNotFoundError(f"Config file not found: ${config_filepath}")
    config = configparser.ConfigParser(
                interpolation=configparser.ExtendedInterpolation()
                )
    if env_vars: read_env_vars(env_vars)
    config.read(config_filepath)
    return config

def text_substitute(file_path, mapping):
    with open(file_path, 'r') as file:
        content = file.read()
    for search, replace in mapping.items():
        content = content.replace(search, replace)
    with open(file_path, 'w') as file:
        file.write(content)
