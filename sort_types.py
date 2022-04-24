def bubble_sort(_list):
    for j in range(len(_list)):
        f = True
        for i in range(len(_list)-1-j):
            if _list[i] > _list[i+1]:
                _list[i], _list[i+1] = _list[i+1], _list[i]
                f = False
        if f:
            return _list

#def mod_bubble_sort(_list):
#    return None

def quick_sort(_list):
    if len(_list) < 2:
        return _list
    else:
        x = _list.pop()
        return quick_sort([i for i in _list if i < x]) + [x] + quick_sort([i for i in _list if i >= x])

def selection_sort(_list):
    for i in range(len(_list)-1):
        n = _list.index(min(_list[i:]))
        _list[i], _list[n] = _list[n], _list[i]
    return _list

def insert_sort(_list):
    for i in range(1, len(_list)):
        j = i - 1
        key = _list[i]
        while _list[j] > key and j >= 0:
            _list[j+1] = _list[j]
            j -= 1
        _list[j+1] = key
    return _list

def shell_sort(_list):
    last = len(_list)
    step = last // 2
    while step:
        for i in range(step, last):
            j = i
            key = i - step
            while _list[j] < _list[key] and key >= 0:
                _list[j], _list[key] = _list[key], _list[j]
                j = key
                key = j - step
        step //= 2
    return _list
