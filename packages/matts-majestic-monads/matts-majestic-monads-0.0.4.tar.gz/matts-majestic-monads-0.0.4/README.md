Matts Majestic Monads
---------------------

[![pipeline status](https://gitlab.com/matthewfranglen/matts-majestic-monads/badges/master/pipeline.svg)](https://gitlab.com/matthewfranglen/matts-majestic-monads/commits/master)
[![coverage report](https://gitlab.com/matthewfranglen/matts-majestic-monads/badges/master/coverage.svg)](https://gitlab.com/matthewfranglen/matts-majestic-monads/commits/master)

This overblown library implements Functor, Applicative and Monad in Python.

Synopsis
--------

You can use `Either.convert` or `Maybe.convert` as a decorator to convert return types.
This example converts exceptions into Left values:

```python
from monads import Either

@Either.convert
def parse_arguments():
    parser = argparse.ArgumentParser(description='Download a URL and print the length of the body')
    parser.add_argument('URL', help='URL to download')
    return parser.parse_args()
```

Once you have your Either you can use `fmap` and `bind` to operate over the contained value:

```python
result = (
    make_parser()
        .fmap(parse)
        .fmap(to_url)
        .bind(read)
)
```

The methods will be passed the current value.
You should use `fmap` when the function will return a normal value.
When the function returns a monad, use `bind`.

You can use `Function` as a decorator to convert functions.
Once converted they become composable:

```python
from monads import Function

@Function
def parse(parser):
    return parser.parse_args()

@Function
def to_url(arguments):
    return arguments.URL

both = parse.compose(to_url)
```
