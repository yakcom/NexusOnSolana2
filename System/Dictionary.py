
def DeepFind(d, k):
    if k in d:return d[k]
    for _,v in d.items():
        if isinstance(v, dict):
            r = DeepFind(v, k)
            if r is not None:return r
    return None