# PyProfyler
a simple memory profiler for python programs.

## Installation:
```sh
sudo pip3 install git+https://github.com/AlyShmahell/PyProfyler
```
or  
```sh
sudo pip3 install pyprofyler
```
## Example:
```python
from pyprofyler import PyProfyler

def wrapped_function():
    array = []
    for i in range(1,1000000):
        array.append(i)
    return array

@PyProfyler
def decorated_function():
    a_list = []
    for i in range(1,1000000):
        a_list.append(i)
    return a_list

if __name__ == '__main__':
    ##############################################
    #    Profiling a function by wrapping it     #
    ##############################################
    wrapped_profile = PyProfyler(wrapped_function)
    # "Not Profiled Yet" Message
    print(wrapped_profile)
    result = wrapped_profile()
    # Profile Message, through __str__
    print(wrapped_profile)
    # Function Execution Result
    print(f"execution result: {result[10]}")
    # Profile Message, through __getitem__
    print(wrapped_profile['profile'])
    ##############################################
    #      Profiling a decorated function        #
    ##############################################
    # "Not Profiled Yet" Message
    print(decorated_function)
    result = decorated_function()
    # Profile Message, through __str__
    print(decorated_function)
    # Function Execution Result
    print(f"execution result: {result[10]}")
    # Profile Message, through __getitem__
    print(decorated_function['profile'])
```