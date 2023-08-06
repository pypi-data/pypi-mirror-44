from math import ceil


def generator_list(l, page_size, start=1):
    _list = list(l)
    for page in range(start, int(ceil(len(_list) / page_size) + 1)):
        yield _list[(page - 1) * page_size:page * page_size]


def merge_str(*args, dividing=':'):
    return dividing.join([str(_) for _ in args])
