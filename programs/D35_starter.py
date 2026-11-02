
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

def eval_let(expr, env):
    # Replace this line with your solution.
    return error("Not implemented yet")

expr = ['let','x',['num',2],
    ['add', ['let','x',['add',['var','x'],['num',3]],['var','x']],
            ['var','x']]]
pa_check(eval_let(expr, None) == 7, "RHS sees outer x, body shadows locally")
env = llist(pair('x',4), pair('x',9))
pa_check(eval_let(['mul',['var','x'],['num',3]], env) == 12, "Nearest binding")
pa_check(head(head(env)) == 'x' and tail(head(env)) == 4, "Environment preserved")
print("D35: all supplied checks passed")
