
# Practice helpers, defined here; these are not extra built-ins.
def pa_check(condition, message):
    if not condition:
        return error(message)
    return True

def pa_values(xs, expected):
    current = xs
    for i in range(len(expected)):
        pa_check(not is_none(current), "Linked result ended early")
        pa_check(head(current) == expected[i], "Unexpected linked value")
        current = tail(current)
    return pa_check(is_none(current), "Unexpected extra linked values")

def pa_snapshot(xs):
    saved = [None] * length(xs)
    for i in range(len(saved)):
        saved[i] = [xs, head(xs), tail(xs)]
        xs = tail(xs)
    return saved

def pa_unchanged(saved):
    for i in range(len(saved)):
        node = saved[i][0]
        pa_check(head(node) == saved[i][1], "An input head changed")
        pa_check(tail(node) is saved[i][2], "An input tail changed")
    return True

def pa_prefix(s, expected):
    current = s
    for i in range(len(expected)):
        pa_check(not is_none(current), "Stream ended early")
        pa_check(head(current) == expected[i], "Unexpected stream value")
        if i + 1 < len(expected):
            current = stream_tail(current)
    return True

def d_keep(xs, pred):
    result = None
    last = None
    while not is_none(xs):
        nxt = tail(xs)
        if pred(head(xs)):
            set_tail(xs, None)
            if is_none(result):
                result = xs
            else:
                set_tail(last, xs)
            last = xs
        xs = nxt
    return result

xs = llist(5, 2, 8, 3)
saved = pa_snapshot(xs)
result = d_keep(xs, lambda x: x % 2 == 0)
pa_values(result, [2, 8])
pa_check(result is saved[1][0], "Reused first kept node")
pa_check(tail(result) is saved[2][0], "Reused second kept node")
pa_values(d_keep(llist(1,3), lambda x: x % 2 == 0), [])
print("D14: all supplied checks passed")
