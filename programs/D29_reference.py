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

def expand_run_stream(s):

    def emit(value, left, source):

        def later():
            if left > 1:
                return emit(value, left - 1, source)
            return expand_run_stream(stream_tail(source))
        return pair(value, memo_fun(later))
    if is_none(s):
        return None
    record = head(s)
    return emit(head(record), tail(record), s)

s = expand_run_stream(stream(pair('a', 2), pair('b', 1)))
pa_prefix(s, ['a', 'a', 'b'])
pa_check(stream_tail(s) is stream_tail(s), "Repeat forcing")
pa_check(is_none(expand_run_stream(None)), "No runs")
(
    pa_check(head(expand_run_stream(stream(pair(7, 1000000)))) == 7,
    "Do not eagerly expand a run")
)
print("D29: all supplied checks passed")
