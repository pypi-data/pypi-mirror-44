[![codecov.io](https://codecov.io/github/naphta/defer/coverage.svg?branch=master)](https://codecov.io/github/naphta/defer)
[![image](https://img.shields.io/github/contributors/naphta/defer.svg)](https://github.com/naphta/defer/graphs/contributors)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/naphta)


Defer
============
Add a simple golang-esque deferral system for python.

# Usage

```
@defer.with_defer
def example_function(defer):
    print("Hello")
    defer(print, "!")
    print("World")
    
example_function()
> Hello
> World
> !
```