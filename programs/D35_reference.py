# D35 | Source Academy Python §3

# Test helpers for Python §3. These are not part of your solution.
# One case can check several properties, but earns only one point.
pa_case_ok = [True]
pa_details = [True]

def pa_check(condition, message):
    if not condition:
        pa_case_ok[0] = False
        if pa_details[0]:
            print(message)
    return condition

def pa_list(values):
    xs = None
    for i in range(len(values) - 1, -1, -1):
        xs = pair(values[i], xs)
    return xs

def pa_snapshot(xs):
    n = 0
    current = xs
    while not is_none(current):
        n = n + 1
        current = tail(current)
    saved = [None] * n
    for i in range(n):
        saved[i] = [xs, head(xs), tail(xs)]
        xs = tail(xs)
    return saved

def pa_unchanged(saved):
    for i in range(len(saved)):
        pa_check(head(saved[i][0]) == saved[i][1], 'Input head changed')
        pa_check(tail(saved[i][0]) is saved[i][2], 'Input tail changed')
    return pa_case_ok[0]

def pa_heads(saved):
    for i in range(len(saved)):
        pa_check(head(saved[i][0]) == saved[i][1], 'Original head changed')
    return pa_case_ok[0]

def pa_values(xs, expected):
    for i in range(len(expected)):
        if not pa_check(is_pair(xs), 'Missing linked node or wrong representation'):
            return False
        pa_check(head(xs) == expected[i], 'Unexpected linked value')
        xs = tail(xs)
    return pa_check(is_none(xs), 'Extra nodes or a cycle')

def pa_fresh(xs, saved, n):
    for i in range(n):
        if not is_pair(xs):
            return pa_check(False, 'Freshness check: missing node')
        for j in range(len(saved)):
            pa_check(xs is not saved[j][0], 'Output reused an input node')
        xs = tail(xs)
    return True

def pa_order(xs, saved, indices):
    for i in range(len(indices)):
        if not is_pair(xs):
            return pa_check(False, 'Identity check: missing node')
        pa_check(xs is saved[indices[i]][0], 'Wrong node identity or unstable order')
        pa_check(head(xs) == saved[indices[i]][1], 'Node head changed')
        xs = tail(xs)
    return pa_check(is_none(xs), 'Result must end at None')

def pa_rows(mat):
    return [mat, pa_copy_rows(mat)]

def pa_copy_rows(mat):
    rows = [None] * len(mat)
    for i in range(len(mat)):
        rows[i] = mat[i]
    return rows

def pa_matrix_unchanged(mat, expected, rows):
    pa_check(mat == expected, 'Input matrix values changed')
    for i in range(len(rows)):
        pa_check(mat[i] is rows[i], 'Input row replaced')
    return pa_case_ok[0]

def pa_matrix_fresh(result, mat):
    pa_check(result is not mat, 'Outer matrix was reused')
    for i in range(len(result)):
        for j in range(i):
            pa_check(result[i] is not result[j], 'Output rows alias each other')
        for j in range(len(mat)):
            pa_check(result[i] is not mat[j], 'Output row aliases input')
    return pa_case_ok[0]

def pa_runs(runs, expected, saved):
    earlier = None
    for i in range(len(expected)):
        if not is_pair(runs) or not is_pair(head(runs)):
            return pa_check(False, 'Expected outer node and pair(value, count) record')
        record = head(runs)
        pa_check(head(record) == expected[i][0], 'Wrong run value')
        pa_check(tail(record) == expected[i][1], 'Wrong run count or record representation')
        for j in range(len(saved)):
            pa_check(runs is not saved[j][0] and record is not saved[j][0], 'Run output aliases input')
        scan = earlier
        while not is_none(scan):
            pa_check(record is not head(scan), 'Run records share one pair')
            scan = tail(scan)
        earlier = pair(record, earlier)
        runs = tail(runs)
    return pa_check(is_none(runs), 'Extra run nodes')

def pa_records(items):
    result = None
    for i in range(len(items) - 1, -1, -1):
        result = pair(pair(items[i][0], items[i][1]), result)
    return result

def pa_records_unchanged(saved, expected):
    pa_unchanged(saved)
    for i in range(len(saved)):
        pa_check(head(saved[i][1]) == expected[i][0], 'Input record value changed')
        pa_check(tail(saved[i][1]) == expected[i][1], 'Input record count changed')
    return pa_case_ok[0]

def pa_stream(values):
    def build(i):
        if i == len(values):
            return None
        return pair(values[i], lambda: build(i + 1))
    return build(0)

def pa_prefix(s, expected, finite, memo):
    for i in range(len(expected)):
        if not is_pair(s):
            return pa_check(False, 'Stream ended early or has wrong representation')
        pa_check(head(s) == expected[i], 'Wrong stream value')
        if i + 1 < len(expected) or finite:
            first = stream_tail(s)
            if memo:
                pa_check(stream_tail(s) is first, 'Output tail is not memoized')
            s = first
    if finite:
        pa_check(is_none(s), 'Finite stream has extra values')
    return pa_case_ok[0]

def pa_counted_stream(values, counter):
    def build(i):
        if i == len(values):
            return None
        def later():
            counter[0] = counter[0] + 1
            return build(i + 1)
        return pair(values[i], later)
    return build(0)

def pa_integers(start, step):
    return pair(start, lambda: pa_integers(start + step, step))

def pa_tree(spec):
    if is_none(spec) or not is_list(spec):
        return spec
    result = None
    for i in range(len(spec) - 1, -1, -1):
        result = pair(pa_tree(spec[i]), result)
    return result

def pa_tree_values(tree, spec):
    if is_list(spec):
        for i in range(len(spec)):
            if not is_pair(tree):
                return pa_check(False, 'Wrong tree shape')
            pa_tree_values(head(tree), spec[i])
            tree = tail(tree)
        return pa_check(is_none(tree), 'Extra tree nodes')
    return pa_check(tree == spec, 'Wrong leaf or empty subtree')

def pa_tree_nodes(tree):
    if not is_pair(tree):
        return None
    def join(xs, ys):
        if is_none(xs):
            return ys
        return pair(head(xs), join(tail(xs), ys))
    return pair(tree, join(pa_tree_nodes(head(tree)), pa_tree_nodes(tail(tree))))

def pa_tree_fresh(result, original_nodes):
    if is_pair(result):
        current = original_nodes
        while not is_none(current):
            pa_check(result is not head(current), 'Tree reused an input pair')
            current = tail(current)
        pa_tree_fresh(head(result), original_nodes)
        pa_tree_fresh(tail(result), original_nodes)
    return pa_case_ok[0]

def eval_let(expr, env):
    tag = expr[0]
    if tag == 'num':
        return expr[1]
    if tag == 'var':
        rest = env
        while not is_none(rest):
            binding = head(rest)
            if head(binding) == expr[1]:
                return tail(binding)
            rest = tail(rest)
        return error('Unbound variable')
    if tag == 'add':
        return eval_let(expr[1], env) + eval_let(expr[2], env)
    if tag == 'mul':
        return eval_let(expr[1], env) * eval_let(expr[2], env)
    value = eval_let(expr[2], env)
    extended = pair(pair(expr[1], value), env)
    return eval_let(expr[3], extended)

def pa_case_01():
    expr = ['num', 5]
    env = pa_records([])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 5, 'Unexpected result')
    pa_check(expr == ['num', 5], "Syntax mutated")
    pa_records_unchanged(saved, [])
    return pa_case_ok[0]

def pa_case_02():
    expr = ['var', 'x']
    env = pa_records([['x', 4], ['x', 9]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 4, 'Unexpected result')
    pa_check(expr == ['var', 'x'], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 4], ['x', 9]])
    return pa_case_ok[0]

def pa_case_03():
    expr = ['add', ['num', 2], ['num', 3]]
    env = pa_records([])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 5, 'Unexpected result')
    pa_check(expr == ['add', ['num', 2], ['num', 3]], "Syntax mutated")
    pa_records_unchanged(saved, [])
    return pa_case_ok[0]

def pa_case_04():
    expr = ['let', 'x', ['num', 2], ['let', 'x', ['add', ['var', 'x'], ['num', 3]], ['var', 'x']]]
    env = pa_records([])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 5, 'Unexpected result')
    pa_check(expr == ['let', 'x', ['num', 2], ['let', 'x', ['add', ['var', 'x'], ['num', 3]], ['var', 'x']]], "Syntax mutated")
    pa_records_unchanged(saved, [])
    return pa_case_ok[0]

def pa_case_05():
    expr = ['add', ['let', 'x', ['num', 0], ['var', 'x']], ['var', 'x']]
    env = pa_records([['x', -5], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == -5, 'Unexpected result')
    pa_check(expr == ['add', ['let', 'x', ['num', 0], ['var', 'x']], ['var', 'x']], "Syntax mutated")
    pa_records_unchanged(saved, [['x', -5], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_06():
    expr = ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['mul', ['var', 'x'], ['num', 2]]]
    env = pa_records([['x', -4], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == -6, 'Unexpected result')
    pa_check(expr == ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['mul', ['var', 'x'], ['num', 2]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', -4], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_07():
    expr = ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 2], ['add', ['var', 'x'], ['var', 'y']]]]
    env = pa_records([['x', -3], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == -7, 'Unexpected result')
    pa_check(expr == ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 2], ['add', ['var', 'x'], ['var', 'y']]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', -3], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_08():
    expr = ['mul', ['let', 'x', ['num', 3], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]]
    env = pa_records([['x', -2], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == -3, 'Unexpected result')
    pa_check(expr == ['mul', ['let', 'x', ['num', 3], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', -2], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_09():
    expr = ['add', ['let', 'x', ['num', 4], ['var', 'x']], ['var', 'x']]
    env = pa_records([['x', -1], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 3, 'Unexpected result')
    pa_check(expr == ['add', ['let', 'x', ['num', 4], ['var', 'x']], ['var', 'x']], "Syntax mutated")
    pa_records_unchanged(saved, [['x', -1], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_10():
    expr = ['let', 'x', ['add', ['var', 'x'], ['num', 5]], ['mul', ['var', 'x'], ['num', 2]]]
    env = pa_records([['x', 0], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 10, 'Unexpected result')
    pa_check(expr == ['let', 'x', ['add', ['var', 'x'], ['num', 5]], ['mul', ['var', 'x'], ['num', 2]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 0], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_11():
    expr = ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 6], ['add', ['var', 'x'], ['var', 'y']]]]
    env = pa_records([['x', 1], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 9, 'Unexpected result')
    pa_check(expr == ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 6], ['add', ['var', 'x'], ['var', 'y']]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 1], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_12():
    expr = ['mul', ['let', 'x', ['num', 0], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]]
    env = pa_records([['x', 2], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 0, 'Unexpected result')
    pa_check(expr == ['mul', ['let', 'x', ['num', 0], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 2], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_13():
    expr = ['add', ['let', 'x', ['num', 1], ['var', 'x']], ['var', 'x']]
    env = pa_records([['x', 3], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 4, 'Unexpected result')
    pa_check(expr == ['add', ['let', 'x', ['num', 1], ['var', 'x']], ['var', 'x']], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 3], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_14():
    expr = ['let', 'x', ['add', ['var', 'x'], ['num', 2]], ['mul', ['var', 'x'], ['num', 2]]]
    env = pa_records([['x', 4], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 12, 'Unexpected result')
    pa_check(expr == ['let', 'x', ['add', ['var', 'x'], ['num', 2]], ['mul', ['var', 'x'], ['num', 2]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 4], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_15():
    expr = ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 3], ['add', ['var', 'x'], ['var', 'y']]]]
    env = pa_records([['x', 5], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 18, 'Unexpected result')
    pa_check(expr == ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 3], ['add', ['var', 'x'], ['var', 'y']]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 5], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_16():
    expr = ['mul', ['let', 'x', ['num', 4], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]]
    env = pa_records([['x', 6], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 28, 'Unexpected result')
    pa_check(expr == ['mul', ['let', 'x', ['num', 4], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 6], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_17():
    expr = ['add', ['let', 'x', ['num', 5], ['var', 'x']], ['var', 'x']]
    env = pa_records([['x', 7], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 12, 'Unexpected result')
    pa_check(expr == ['add', ['let', 'x', ['num', 5], ['var', 'x']], ['var', 'x']], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 7], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_18():
    expr = ['let', 'x', ['add', ['var', 'x'], ['num', 6]], ['mul', ['var', 'x'], ['num', 2]]]
    env = pa_records([['x', 8], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 28, 'Unexpected result')
    pa_check(expr == ['let', 'x', ['add', ['var', 'x'], ['num', 6]], ['mul', ['var', 'x'], ['num', 2]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 8], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_19():
    expr = ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 0], ['add', ['var', 'x'], ['var', 'y']]]]
    env = pa_records([['x', 9], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 27, 'Unexpected result')
    pa_check(expr == ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 0], ['add', ['var', 'x'], ['var', 'y']]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 9], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_20():
    expr = ['mul', ['let', 'x', ['num', 1], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]]
    env = pa_records([['x', 10], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 11, 'Unexpected result')
    pa_check(expr == ['mul', ['let', 'x', ['num', 1], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 10], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_21():
    expr = ['add', ['let', 'x', ['num', 2], ['var', 'x']], ['var', 'x']]
    env = pa_records([['x', 11], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 13, 'Unexpected result')
    pa_check(expr == ['add', ['let', 'x', ['num', 2], ['var', 'x']], ['var', 'x']], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 11], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_22():
    expr = ['let', 'x', ['add', ['var', 'x'], ['num', 3]], ['mul', ['var', 'x'], ['num', 2]]]
    env = pa_records([['x', 12], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 30, 'Unexpected result')
    pa_check(expr == ['let', 'x', ['add', ['var', 'x'], ['num', 3]], ['mul', ['var', 'x'], ['num', 2]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 12], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_23():
    expr = ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 4], ['add', ['var', 'x'], ['var', 'y']]]]
    env = pa_records([['x', 13], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 43, 'Unexpected result')
    pa_check(expr == ['let', 'y', ['mul', ['var', 'x'], ['num', 3]], ['let', 'x', ['num', 4], ['add', ['var', 'x'], ['var', 'y']]]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 13], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

def pa_case_24():
    expr = ['mul', ['let', 'x', ['num', 5], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]]
    env = pa_records([['x', 14], ['x', 99], ['y', 10]])
    saved = pa_snapshot(env)
    pa_check(eval_let(expr, env) == 75, 'Unexpected result')
    pa_check(expr == ['mul', ['let', 'x', ['num', 5], ['var', 'x']], ['let', 'x', ['add', ['var', 'x'], ['num', 1]], ['var', 'x']]], "Syntax mutated")
    pa_records_unchanged(saved, [['x', 14], ['x', 99], ['y', 10]])
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Lexical scope case 1', 'Lexical scope case 2', 'Lexical scope case 3', 'Lexical scope case 4', 'Lexical scope case 5', 'Lexical scope case 6', 'Lexical scope case 7', 'Lexical scope case 8', 'Lexical scope case 9', 'Lexical scope case 10', 'Lexical scope case 11', 'Lexical scope case 12', 'Lexical scope case 13', 'Lexical scope case 14', 'Lexical scope case 15', 'Lexical scope case 16', 'Lexical scope case 17', 'Lexical scope case 18', 'Lexical scope case 19', 'Lexical scope case 20', 'Lexical scope case 21', 'Lexical scope case 22', 'Lexical scope case 23', 'Lexical scope case 24']
# Set True to show each case's title and failed-property messages.
# Private-style mode defaults to case IDs only; the test source remains inspectable.
pa_reveal_details = False
pa_passed = 0
pa_public_passed = 0
pa_extra_passed = 0
for pa_i in range(len(pa_cases)):
    pa_case_ok[0] = True
    pa_details[0] = pa_reveal_details or pa_i < 4
    print("Running case", pa_i + 1)
    if pa_details[0]:
        print(pa_titles[pa_i])
    pa_returned = pa_cases[pa_i]()
    if pa_case_ok[0] and pa_returned:
        pa_passed = pa_passed + 1
        if pa_i < 4:
            pa_public_passed = pa_public_passed + 1
        else:
            pa_extra_passed = pa_extra_passed + 1
        print("PASS")
    else:
        print("FAIL")
print("D35 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
