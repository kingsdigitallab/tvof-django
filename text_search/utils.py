def haystack_id(obj):
    ret = '{}.{:03d}'.format(obj.location, int(obj.n))
    return ret
