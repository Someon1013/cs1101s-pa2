
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

def d_partition(xs, pred):
    yes = None
    no = None
    ylast = None
    nlast = None
    while not is_none(xs):
        nxt = tail(xs)
        set_tail(xs, None)
        if pred(head(xs)):
            if is_none(yes):
                yes = xs
            else:
                set_tail(ylast, xs)
            ylast = xs
        else:
            if is_none(no):
                no = xs
            else:
                set_tail(nlast, xs)
            nlast = xs
        xs = nxt
    return [yes, no]

xs = llist(4, 1, 6, 3)
saved = pa_snapshot(xs)
parts = d_partition(xs, lambda x: x >= 4)
pa_values(parts[0], [4, 6])
pa_values(parts[1], [1, 3])
pa_check(parts[0] is saved[0][0], "Yes head identity")
pa_check(tail(parts[0]) is saved[2][0], "Yes tail identity")
pa_check(parts[1] is saved[1][0], "No head identity")
pa_check(tail(parts[1]) is saved[3][0], "No tail identity")
print("D18: all supplied checks passed")
