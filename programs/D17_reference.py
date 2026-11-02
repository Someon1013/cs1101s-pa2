
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

def d_merge_asc(xs, ys):
    if is_none(xs):
        return ys
    if is_none(ys):
        return xs
    if head(xs) <= head(ys):
        set_tail(xs, d_merge_asc(tail(xs), ys))
        return xs
    set_tail(ys, d_merge_asc(xs, tail(ys)))
    return ys

def d_merge_sort(xs):
    if is_none(xs) or is_none(tail(xs)):
        return xs
    slow = xs
    fast = tail(xs)
    while not is_none(fast) and (not is_none(tail(fast))):
        slow = tail(slow)
        fast = tail(tail(fast))
    second = tail(slow)
    set_tail(slow, None)
    return d_merge_asc(d_merge_sort(xs), d_merge_sort(second))

xs = llist(4, 1, 4, 2, 0)
saved = pa_snapshot(xs)
result = d_merge_sort(xs)
pa_values(result, [0, 1, 2, 4, 4])
pa_check(result is saved[4][0], "No replacement nodes")
last_two = tail(tail(tail(result)))
pa_check(last_two is saved[0][0], "Stable first equal node")
pa_check(tail(last_two) is saved[2][0], "Stable second equal node")
for i in range(len(saved)):
    pa_check(head(saved[i][0]) == saved[i][1], "Do not swap heads")
pa_values(d_merge_sort(None), [])
print("D17: all supplied checks passed")
