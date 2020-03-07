#%%
import os
from click.testing import CliRunner

#%%
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))


# %%
import runpy
import walk_replace as r
import unittest.mock

from importlib import reload  # Python 3.4+ only.


#%%
import walk_replace.__main__ as rm

rm = reload(rm)
r = reload(r)

fixdir = os.path.dirname(__file__) + '/../tests/fixture'

test_args = [
    '-e',
    fixdir + '/replace.conf1',
    'yyy-dir'
]
os.environ['WALK_SECRET'] = '$secret'
os.environ['ENV_CODE'] = 'test'


runner = CliRunner()
result = runner.invoke(rm.main, test_args)


# %%
