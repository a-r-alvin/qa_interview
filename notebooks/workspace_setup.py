# Note: `get_ipython().run_line_magic()` commands are runnable from both a Notebook and a py file; `%` magic commands are runnable from a Notebook only.

# clear_output() clears cell output such as print(). Useful to remove intermediate status update messages at the end of a function.
from IPython.display import clear_output

# Prevent tab autocomplete from bringing up extraneous suggestions?
#%config IPCompleter.greedy = True # Must be False to allow file paths to be autocompleted? But if False, you also get a lot of irrelevant autocomplete suggestions.
get_ipython().run_line_magic('config', 'IPCompleter.greedy = True')

# ! Use with caution: may cause unexpected conflicts or interfere with long-running processes.
# N.B. "%autoreload 1" (auto-reload marked packages) is safer than "%autoreload 2" (auto-reload all packages).
get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '1')

# Enable %memit for memory profiling.
#!pip install memory_profiler
#get_ipython().run_line_magic('load_ext', 'memory_profiler')

# Enable import from parent, grandparent or great-grandparent directory.
import sys
[sys.path.append(i) for i in ['.', '..', '../..']]
#sys.path.append('D:/src')
sys.path = list(set(sys.path)) # Remove duplicate paths.

clear_output() # This works even if this function is called from a py file via Notebook magic command %run.
print('✔ workspace_setup.')