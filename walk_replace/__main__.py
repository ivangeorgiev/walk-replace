"""Walk replace main module."""

import click
from . import replace as r


@click.command()
@click.argument('config_file', type=click.STRING)
@click.argument('path', type=click.STRING)
@click.option('--env-vars', '-e', is_flag=True, default=False)
@click.option('--substitute-config-section', '-s', default='substitute')
@click.option('--substitute-mode', '-m', default='plaintext')
@click.option('--include-file-match', '-i', default='.*')
#pylint: disable=too-many-arguments
def main(path,
         config_file,
         env_vars,
         substitute_config_section,
         substitute_mode,
         include_file_match):
    """Main module function."""
    substitute_mode = getattr(r.SubstituteMode, substitute_mode.upper())

    return r.main(path,
                  config_file,
                  env_vars=env_vars,
                  substitute_config_section=substitute_config_section,
                  substitute_mode=substitute_mode,
                  include_file_match=include_file_match)

if __name__ == '__main__': # pragma: no cover
    #pylint: disable=no-value-for-parameter
    main()
