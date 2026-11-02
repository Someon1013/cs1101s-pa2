
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

def decode_runs(runs):

    def repeat(value, count, rest):
        if count == 0:
            return decode_runs(rest)
        return pair(value, repeat(value, count - 1, rest))
    if is_none(runs):
        return None
    record = head(runs)
    return repeat(head(record), tail(record), tail(runs))

runs = llist(pair(5, 2), pair(-1, 3))
saved = pa_snapshot(runs)
pa_values(decode_runs(runs), [5, 5, -1, -1, -1])
pa_values(decode_runs(None), [])
pa_check(tail(head(runs)) == 2, "Input count changed")
pa_unchanged(saved)
print("D08: all supplied checks passed")
