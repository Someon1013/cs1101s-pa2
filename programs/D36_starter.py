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

def route_cost_stream(mat, start, deltas):
    # Replace this line with your solution.
    return error("Not implemented yet")

mat = [[0,4,9], [2,0,3], [7,1,0]]
s = route_cost_stream(mat, 0, stream(1,1,-2))
pa_prefix(s, [4, 7, 14])
pa_check(stream_tail(s) is stream_tail(s), "Memoized tail")
pa_prefix(route_cost_stream(mat, 0, stream(0,2,0,-1,1)), [0,9,9,10,13])
pa_check(is_none(route_cost_stream(mat, 0, None)), "No moves")
print("D36: all supplied checks passed")
