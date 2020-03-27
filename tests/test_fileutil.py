import os
import pytest
from devopslib import fileutil

@pytest.fixture(scope="session")
def fixdir_fileutil(fixdir):
    return f"{fixdir}/fileutil"

@pytest.fixture(scope="session")
def fixdir_search(fixdir_fileutil):
    return f"{fixdir_fileutil}/search"

@pytest.fixture(scope="session")
def fixdir_config(fixdir_fileutil):
    return f"{fixdir_fileutil}/config"

@pytest.fixture
def substitute_plaintext_file(tmpdir):
    filename = f"{tmpdir}/file.txt"
    with open(filename, 'w') as file:
        file.write("White bird in my garden.")
    return filename

@pytest.fixture
def substitute_template_file(tmpdir):
    filename = f"{tmpdir}/file.txt"
    with open(filename, 'w') as file:
        file.write("White ${animal} in my garden.")
    return filename



def test_search_files_single_pattern(fixdir_search):
    expected = ["file-1.txt", "dir1/file-1-1.txt"]
    expected = sorted([os.path.abspath(f"{fixdir_search}/{entry}") for entry in expected])
    actual = sorted(fileutil.search_files(f"{fixdir_search}/**/*.txt"))
    assert actual == expected


def test_search_files_multiple_pattern(fixdir_search):
    expected = ["file-1.txt","file-1.doc", "dir1/file-1-1.txt", "dir1/file-1-1.doc"]
    expected = sorted([os.path.abspath(f"{fixdir_search}/{entry}") for entry in expected])
    search_pattern = (f"{fixdir_search}/**/*.txt\n" +
                      f"{fixdir_search}/**/*-1.doc," +
                      f"{fixdir_search}/**/*-1-1.doc")
    actual = sorted(fileutil.search_files(search_pattern))
    assert actual == expected

def test_search_files_ignores_dirs(fixdir_search):
    expected = ["file-1.txt","dir1/file-1-1.txt"]
    expected = sorted([os.path.abspath(f"{fixdir_search}/{entry}") for entry in expected])
    search_pattern = (f"{fixdir_search}/**/*.txt\n" +
                      f"{fixdir_search}/**/dir*")
    actual = sorted(fileutil.search_files(search_pattern))
    assert actual == expected

def test_read_config(fixdir_config):
    os.environ['ENVIRONMENT_NAME'] = 'ask'
    config_filename = f'{fixdir_config}/some.config'
    config = fileutil.read_config(config_filename, env_vars='environment_name')
    expected = { 'a':'Hello', 'b': 'ask' }
    assert expected == dict(config['settings'])


def test_read_config_all_env_vars(fixdir_config):
    os.environ['SOMETHING_HERE'] = 'ask'
    os.environ['ENVIRONMENT_NAME'] = 'ask'
    config_filename = f'{fixdir_config}/some.config'
    config = fileutil.read_config(config_filename, env_vars='something_here,*')
    expected = { 'a':'Hello', 'b': 'ask' }
    assert expected == dict(config['settings'])


def test_read_config_raises_filenotfound(tmpdir):
    with pytest.raises(FileNotFoundError):
        fileutil.read_config(tmpdir + "/notfound.conf")

def test_substitute_plaintext(substitute_plaintext_file):
    expected = "White fox in my garden."
    fileutil.text_substitute(substitute_plaintext_file, {'bird':'fox'})
    with open(substitute_plaintext_file, 'r') as file:
        actual = file.read()
    assert expected == actual

def test_substitute_template(substitute_template_file):
    expected = "White fox in my garden."
    fileutil.text_substitute(substitute_template_file, 
                             {'animal':'fox'}, 
                             fileutil.SubstituteMethod.TEMPLATE)
    with open(substitute_template_file, 'r') as file:
        actual = file.read()
    assert expected == actual

def test_pivot_mapping():
    mapping = {
               'search.name': '<name>',
               'replace.name': 'John',
               'search.age': '<age>',
              }
    expect = {
              '<name>': 'John',
              '<age>': '',
             }

    actual =  fileutil.pivot_mapping(mapping, 'search.', 'replace.')
    assert expect == actual
