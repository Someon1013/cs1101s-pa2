
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

def adjacent_gaps(xs):
    if is_none(xs) or is_none(tail(xs)):
        return None
    return pair(head(tail(xs)) - head(xs), adjacent_gaps(tail(xs)))

xs = llist(4, 9, 7, 7)
saved = pa_snapshot(xs)
result = adjacent_gaps(xs)
pa_values(result, [5, -2, 0])
pa_check(result is not xs, "Result must be fresh")
pa_values(adjacent_gaps(None), [])
pa_values(adjacent_gaps(llist(8)), [])
pa_unchanged(saved)
print("D03: all supplied checks passed")
