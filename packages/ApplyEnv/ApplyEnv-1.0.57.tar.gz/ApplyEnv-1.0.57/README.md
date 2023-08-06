# Applies values from a flat dict ("environment") to a tree-like structure ("schema"). 


## Examples

```
    >>> from applyenv import apply
    >>> schema = dict(a="A", b=dict(c="C"))
    >>> environ = dict(A=3, C=5)
    >>> apply(schema, environ)
    {'a': 3, b: {'c': 5}} 

```

Note: feel free to use os.environ to populate env values directly into your schema.

