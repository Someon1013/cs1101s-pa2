def memo_fun(f):
    done = False
    value = None
    def force():
        nonlocal done, value
        if not done:
            value = f()
            done = True
        return value
    return force

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

def smooth_numbers():
    # Replace this line with your solution.
    return error("Not implemented yet")

s = smooth_numbers()
pa_prefix(s, [1,2,3,4,5,6,8,9,10,12,15,16])
pa_check(stream_tail(s) is stream_tail(s), "Shared tail")
current = s
previous = 0
for i in range(1000):
    value = head(current)
    pa_check(value > previous, "Strictly increasing; remove duplicates")
    leftover = value
    for j in range(3):
        factor = [2, 3, 5][j]
        while leftover % factor == 0:
            leftover = leftover // factor
    pa_check(leftover == 1, "Only factors 2, 3, 5")
    previous = value
    if i < 999:
        current = stream_tail(current)
pa_check(previous == 51200000, "1000th smooth number")
print("D30: all supplied checks passed")
