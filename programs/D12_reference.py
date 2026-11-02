
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

def eval_postfix_extended(tokens):
    stack = [None] * len(tokens)
    top = 0
    for i in range(len(tokens)):
        token = tokens[i]
        if token == 'neg':
            stack[top - 1] = -stack[top - 1]
        elif is_string(token):
            right = stack[top - 1]
            left = stack[top - 2]
            top = top - 1
            if token == '+':
                value = left + right
            elif token == '-':
                value = left - right
            elif token == '*':
                value = left * right
            else:
                value = left / right
            stack[top - 1] = value
        else:
            stack[top] = token
            top = top + 1
    return stack[0]

pa_check(eval_postfix_extended([8, 3, '-', 'neg', 2, '/']) == -2.5, "Arity and order")
pa_check(eval_postfix_extended([9, 4, '-', 2, '/']) == 2.5, "Right pop first")
pa_check(eval_postfix_extended([123]) == 123, "Single operand")
pa_check(eval_postfix_extended([2, 8, '/']) == 0.25, "Division is not reversed")
print("D12: all supplied checks passed")
