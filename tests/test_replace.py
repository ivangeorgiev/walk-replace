"""pytest test cases for walk_replace package"""

import os.path
import shutil
import pytest
from click.testing import CliRunner
import walk_replace as r
import walk_replace.__main__ as rm

@pytest.fixture()
def fixdir():
    """directory with fixtures"""
    return os.path.abspath(os.path.dirname(__file__) + '/fixture')

@pytest.fixture()
#pylint: disable=redefined-outer-name
def fixreplace_dir(tmpdir, fixdir):
    """Directory with fixtures for replace test"""
    srcdir = fixdir + '/replace_dir'
    dstdir = str(tmpdir) + '/a'
    shutil.copytree(srcdir, dstdir)
    return dstdir

@pytest.fixture()
#pylint: disable=redefined-outer-name
def fixreplace_conf(fixdir):
    """Configuration file name for replace test."""
    conf_path = fixdir + '/replace.conf'
    return conf_path

def test_import():
    """Smoke test"""
    assert r.__version__ == '0.0.1'

def test_regex_match_returns_true_match():
    """Test that the output of regex_match is a boolean
    True on successfull match.
    """
    match = r.regex_match('.*fox.*')
    #pylint: disable=singleton-comparison
    assert match('lazy fox walked in') == True

def test_regex_match_returns_false_no_match():
    """Test that regex_match returns false if no match."""
    match = r.regex_match('.*fox.*')
    #pylint: disable=singleton-comparison
    assert match('lazy bear walked in') == False

#pylint: disable=redefined-outer-name
def test_walk_dir_walks_directory_and_yields_all_files(fixdir):
    """Test walk_dir returns generator with files walking on directories."""
    expect = [
        'walk_dir/root_file.txt',
        'walk_dir/subdir_with_file/some_file.txt',
        'walk_dir/other_dir/other_file.txt'
        ]
    expect = [os.path.abspath(f"{fixdir}/{item}") for item in expect]
    expect.sort()

    actual = r.walk_dir(fixdir + '/walk_dir')
    actual = [os.path.abspath(item) for item in actual]
    actual.sort()

    assert expect == actual

#pylint: disable=redefined-outer-name
def test_walk_dir_walks_directory_and_yields_include_regex_filter_files(fixdir):
    """Test walk_dir returns only files that match include filter."""
    expect = [
        'walk_dir/subdir_with_file/some_file.txt',
        'walk_dir/other_dir/other_file.txt'
        ]
    expect = [os.path.abspath(f"{fixdir}/{item}") for item in expect]
    expect.sort()

    actual = r.walk_dir(fixdir + '/walk_dir', r'.*(some|other).*')
    actual = [os.path.abspath(item) for item in actual]
    actual.sort()

    assert expect == actual

#pylint: disable=redefined-outer-name
def test_read_file_conent_entire_file(fixdir):
    """Test read_file_content reads and returns content of the entire file."""
    expect = "Hello world!\nI am alive!"
    actual = r.read_file_content(fixdir + '/file_known_content.txt')
    assert actual == expect

def test_get_identity_returns_identity_function():
    """
    WHEN get_identity is called
         And result is called with a 'yes'
    THEN returned string is 'yes'
    """
    identity = r.get_identity()
    expect = "yes"
    actual = identity('yes')
    assert expect == actual

def test_template_filter_safe_substitute():
    """
    GIVEN Safe substitute filter {a: 1}
    WHEN Filter is invoked for 'My number is $a. It costs $5'
    THEN Result is 'My number is 5. It costs $5'
    """
    filter_func = r.get_template_filter(dict(a=1), safe=True)
    expect = 'My number is 1. It costs $5'
    actual = filter_func('My number is $a. It costs $5')
    assert actual == expect

#pylint: disable=invalid-name
def test_template_filter_raises_ValueError():
    """Test template filter raises ValueError for missing
    mapping.
    """
    filter_func = r.get_template_filter(dict(a=1))
    with pytest.raises(KeyError) as excinfo:
        filter_func('My number is $b')
    print(excinfo.value)

#pylint: disable=redefined-outer-name
def test_configparser_safe_dict():
    """Test configparser_save_dict function
    """
    data = {'my_secret': 'very $ecret',
            'my_$ecret': 'very $$ecret'}
    expect = {'my_secret': 'very $$ecret',
              'my_$ecret': 'very $$$$ecret'}
    actual = r.configparser_safe_dict(data)
    assert actual == expect

#pylint: disable=redefined-outer-name
def test_walk_replace_main_raises(fixreplace_dir, fixreplace_conf):
    """Test main function raises exception when config file or
    walk directory is missing or invalid."""

    # replace directory is missing
    with pytest.raises(FileNotFoundError):
        r.main(fixreplace_conf + '-not-found', fixreplace_conf)
    # replace directory is not a directory
    with pytest.raises(NotADirectoryError):
        r.main(fixreplace_conf, fixreplace_conf)
    # Config file is missing
    with pytest.raises(FileNotFoundError):
        r.main(fixreplace_dir, fixreplace_conf + "-not-found")
    # Config file is a directory
    with pytest.raises(FileNotFoundError):
        r.main(fixreplace_dir, fixreplace_dir)



#pylint: disable=redefined-outer-name
def test_walk_replace_main(fixreplace_dir, fixreplace_conf):
    """Test main function"""
    os.environ['WALK_SECRET'] = '$secret'
    os.environ['ENV_CODE'] = 'test'
    r.main(fixreplace_dir, fixreplace_conf,
           env_vars=True, include_file_match=r'.*\.txt$')

    # THEN include file is replaced
    actual = r.read_file_content(fixreplace_dir + '/some_file.txt')
    expect = "secret is: $secret\nenvironment is: test"

    assert actual == expect

    # And not include file is not replaced
    actual = r.read_file_content(fixreplace_dir + '/not_replaced')
    expect = "secret is: __secret__\nenvironment is: __environment__"

    assert actual == expect

#pylint: disable=redefined-outer-name
def test_execute_module(fixreplace_dir, fixreplace_conf):
    """Test walk_replace executed as module.
    Same as if started from the command line:

    python -m walk_replace

    """
    os.environ['WALK_SECRET'] = '$secret'
    os.environ['ENV_CODE'] = 'test'

    test_args = [
        '-e',
        '-i',
        r'.*\.txt$',
        fixreplace_conf,
        fixreplace_dir
    ]

    runner = CliRunner()
    result = runner.invoke(rm.main, test_args)

    if result.exit_code != 0:
        raise result.exception
    assert result.output == ""

    # THEN include file is replaced
    actual = r.read_file_content(fixreplace_dir + '/some_file.txt')
    expect = "secret is: $secret\nenvironment is: test"

    assert actual == expect, "Included file is replaced"

    # And not include file is not replaced
    actual = r.read_file_content(fixreplace_dir + '/not_replaced')
    expect = "secret is: __secret__\nenvironment is: __environment__"

    assert actual == expect, "Not included fie is not replaced"
