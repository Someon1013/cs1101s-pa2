
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

def chunk_sums(xs, k):
    if is_none(xs):
        return None
    total = 0
    used = 0
    while used < k and (not is_none(xs)):
        total = total + head(xs)
        used = used + 1
        xs = tail(xs)
    return pair(total, chunk_sums(xs, k))

xs = llist(1, 2, 3, 4, 5)
saved = pa_snapshot(xs)
pa_values(chunk_sums(xs, 2), [3, 7, 5])
pa_values(chunk_sums(xs, 9), [15])
pa_values(chunk_sums(None, 3), [])
pa_unchanged(saved)
print("D09: all supplied checks passed")
