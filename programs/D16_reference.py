
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

def d_merge_desc(xs, ys):
    if is_none(xs):
        return ys
    if is_none(ys):
        return xs
    if head(xs) >= head(ys):
        set_tail(xs, d_merge_desc(tail(xs), ys))
        return xs
    set_tail(ys, d_merge_desc(xs, tail(ys)))
    return ys

xs = llist(9, 4, 4)
ys = llist(8, 4, 1)
a = pa_snapshot(xs)
b = pa_snapshot(ys)
result = d_merge_desc(xs, ys)
pa_values(result, [9, 8, 4, 4, 4, 1])
pa_check(result is a[0][0], "First node identity")
pa_check(tail(result) is b[0][0], "Second node identity")
pa_check(tail(tail(result)) is a[1][0], "Left tie must precede right")
pa_check(d_merge_desc(None, None) is None, "Empty merge")
print("D16: all supplied checks passed")
