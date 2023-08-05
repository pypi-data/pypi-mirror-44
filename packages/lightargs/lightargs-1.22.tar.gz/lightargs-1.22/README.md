
# What is it

lightargs is a lightweigth easy-to-use arguments manager for Python 2.7 and 3. It has very limited functionalities, but is trivial to use.

# Installation

```bash
pip install lightargs
```

# Usage

See example.py for usage.

In short, in a hello_world.py file:

```python

import lightargs
import sys

# set_usage is used for documentation
lightargs.set_usage("lightargs hello world example")

def hello_world(name):
    if name is None:
        print(Hello World !")
        return
    print ("hello "+str(name)+" !")

# telling the program to call the hello_world function if "hello_world" passed as argument
lightargs.add("hello_world", # argument name
              hello_world, # function to be called of hello_world passed as argument
              nb_args=1, # function hello world takes 1 argument
              defaults=(None) # will be used as default argument
              man="print hello world" # explains what function 'hello_world' does
              category="basic" # used for documentation)
    
if __name__ == "__main__":

    try:
        lightargs.execute(sys.argv[1:])
    except lightargs.WrongParameters as e:
        print str(e)
    except lightargs.UnknownArgument as e:
        print str(e)
        
```

This can be used as follow:

```bash

# no argument, documentation will be printed
python hello_world.py

# invalid argument, an error message will be shown
python hello_world.py bonjour

# valid argument, using default value as argument to the function called
python hello_world.py hello_world

# valid argument, using Bob as argument to the function called
python hello_world.py hello_world bob

# valid argument, too many parameters, error message will be shown
python hello_world.py hello_world bob john


```
