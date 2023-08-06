
def get_key(d, key, delimiter='/'):
    """ Get value

    >>> get_key(dict(a=dict(b=2)), "a/b")
    2

    :param d:
    :param key:
    :param delimiter:
    :return:
    """
    if key == "":
        return d
    r = d
    for k in key.split(delimiter):
        r = r[k]
    return r


def set_key(d, key, value, delimiter='/'):
    """ Set value

    >>> set_key(dict(a=dict(b=2)), "a/b", 3)
    {'a': {'b': 3}}

    """
    keys = key.split(delimiter)
    path, last = keys[:-1], keys[-1]
    r = d
    for k in path:
        r = r[k]
    r[last] = value
    return d


def join_prefix(x, y, delimiter="/"):
    """ Join prefixes

    :param x:
    :param y:
    :param delimiter:
    :return:
    """
    if x == "":
        return y
    return f"{x.rstrip(delimiter)}{delimiter}{y}"


def collect_keys(d):
    """ Collect all keys to be processed (flatten hierarchical data structure)

    >>> collect_keys(dict(a=dict(b="2")))
    ['a/b']

    >>> collect_keys(dict(a=dict(b="2", c=dict(d="3")), t="1"))
    ['t', 'a/b', 'a/c/d']


    :param d:
    :return:
    """
    root = ""
    leaves = []
    prefixes = [root]
    while True:
        if len(prefixes) == 0:
            break
        newprefixes = []
        for prefix in prefixes:
            for k, v in get_key(d, prefix).items():
                if isinstance(v, dict):
                    newprefixes.append(join_prefix(prefix, k))
                elif isinstance(v, str):
                    leaves.append(join_prefix(prefix, k))
        prefixes = newprefixes
    return leaves


def apply(schema, environ):
    """ Walk the supplied schema tree, replacing leaf names with values from environ.


    >>> apply_env(dict(a='b'), environ=dict(b='vb'))
    {'a': 'vb'}

    >>> apply_env(dict(a=dict(b='c')), environ=dict(c='vc'))
    {'a': {'b': 'vc'}}

    """
    result = dict(schema)
    config_keys = collect_keys(schema)
    for config_key in config_keys:
        var_name = get_key(schema, config_key)
        var_value = environ[var_name]
        result = set_key(result, config_key, var_value)
    return result

