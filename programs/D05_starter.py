
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

def route_peak(mat, route):
    # Replace this line with your solution.
    return error("Not implemented yet")

mat = [[0, 7, 2], [4, 0, 6], [9, 1, 0]]
pa_check(route_peak(mat, llist(2, 0, 1)) == 9, "Directed largest leg")
pa_check(route_peak(mat, llist(1, 0, 2)) == 4, "Do not transpose indices")
pa_check(route_peak(mat, None) == 0, "Empty route")
pa_check(route_peak(mat, llist(1)) == 0, "No legs")
print("D05: all supplied checks passed")
