
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

def tree_map(tree, f):
    if is_none(tree):
        return None
    if not is_pair(tree):
        return f(tree)
    return pair(tree_map(head(tree), f), tree_map(tail(tree), f))

tree = llist(2, llist(3, None), 4)
result = tree_map(tree, lambda x: x * x)
pa_check(head(result) == 4, "First leaf")
pa_check(head(head(tail(result))) == 9, "Nested leaf")
pa_check(is_none(head(tail(head(tail(result))))), "Preserve empty subtree")
pa_check(result is not tree, "Fresh outer nodes")
pa_check(head(tail(result)) is not head(tail(tree)), "Fresh nested nodes")
pa_check(head(tree) == 2, "Input preserved")
print("D32: all supplied checks passed")
