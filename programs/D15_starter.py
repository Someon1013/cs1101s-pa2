
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

def d_split_at(xs, k):
    # Replace this line with your solution.
    return error("Not implemented yet")

xs = llist(6, 7, 8, 9)
saved = pa_snapshot(xs)
parts = d_split_at(xs, 2)
pa_values(parts[0], [6, 7])
pa_values(parts[1], [8, 9])
pa_check(parts[0] is xs and parts[1] is saved[2][0], "Head identities")
ys = llist(1, 2)
parts = d_split_at(ys, 0)
pa_check(is_none(parts[0]) and parts[1] is ys, "Zero cut")
pa_values(d_split_at(None, 0)[1], [])
print("D15: all supplied checks passed")
