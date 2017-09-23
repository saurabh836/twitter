def if_dict(val):
    print isinstance(val, dict)
    return isinstance(val, dict)


dict1 = {
        'a': 1,
        'b': 2,
        'c': {
            'a': 3,
            'b': 4,
            'c': {
                'a': 9,
                'b': 3
                }
            }
        }


def findin_dict(dic, k1):
    lis = []
    for k, v in dic.iteritems():
        if k == k1:
            lis.append(v)
        if isinstance(v, dict):
            lis += findin_dict(v, k1)
    return lis


def lis_findin_dict(dic, ke):
    f = []
    for i, k in enumerate(dic):
        f += findin_dict(k, ke)
    return f

