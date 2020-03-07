#%%
import contextlib

#%%
@contextlib.contextmanager
def change_to_dir(new_dir):
    old_dir = os.path.abspath(os.curdir)
    print("Old dir:", old_dir)
    try:
        print("Change to:", os.path.abspath(new_dir))
        os.chdir(new_dir)
        yield new_dir
    finally:
        print("Restoring to:", old_dir)
        os.chdir(old_dir)

#%%
new_dir = os.path.abspath(os.path.dirname(__file__) + '/../tests/fixture')
with change_to_dir(new_dir) as dd:
    print("Currently in:", os.path.abspath(os.curdir))

# %%
