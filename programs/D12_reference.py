# D12 | Source Academy Python §3

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

def pa_case_01():
    tokens = [123]
    pa_check(eval_postfix_extended(tokens) == 123, 'Unexpected result')
    pa_check(tokens == [123], "Tokens changed")
    return pa_case_ok[0]

def pa_case_02():
    tokens = [9, 4, '-']
    pa_check(eval_postfix_extended(tokens) == 5, 'Unexpected result')
    pa_check(tokens == [9, 4, '-'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_03():
    tokens = [2, 8, '/']
    pa_check(eval_postfix_extended(tokens) == 0.25, 'Unexpected result')
    pa_check(tokens == [2, 8, '/'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_04():
    tokens = [8, 3, '-', 'neg', 2, '/']
    pa_check(eval_postfix_extended(tokens) == -2.5, 'Unexpected result')
    pa_check(tokens == [8, 3, '-', 'neg', 2, '/'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_05():
    tokens = [0, 'neg']
    pa_check(eval_postfix_extended(tokens) == 0, 'Unexpected result')
    pa_check(tokens == [0, 'neg'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_06():
    tokens = [-3, 'neg']
    pa_check(eval_postfix_extended(tokens) == 3, 'Unexpected result')
    pa_check(tokens == [-3, 'neg'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_07():
    tokens = [5, 'neg', 'neg']
    pa_check(eval_postfix_extended(tokens) == 5, 'Unexpected result')
    pa_check(tokens == [5, 'neg', 'neg'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_08():
    tokens = [1, 2, '+']
    pa_check(eval_postfix_extended(tokens) == 3, 'Unexpected result')
    pa_check(tokens == [1, 2, '+'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_09():
    tokens = [2, 3, '*']
    pa_check(eval_postfix_extended(tokens) == 6, 'Unexpected result')
    pa_check(tokens == [2, 3, '*'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_10():
    tokens = [1, 8, '-']
    pa_check(eval_postfix_extended(tokens) == -7, 'Unexpected result')
    pa_check(tokens == [1, 8, '-'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_11():
    tokens = [4, 2, '/']
    pa_check(eval_postfix_extended(tokens) == 2.0, 'Unexpected result')
    pa_check(tokens == [4, 2, '/'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_12():
    tokens = [3, 4, '+', 2, '*']
    pa_check(eval_postfix_extended(tokens) == 14, 'Unexpected result')
    pa_check(tokens == [3, 4, '+', 2, '*'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_13():
    tokens = [3, 4, 2, '*', '+']
    pa_check(eval_postfix_extended(tokens) == 11, 'Unexpected result')
    pa_check(tokens == [3, 4, 2, '*', '+'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_14():
    tokens = [2, 3, 4, '+', '-']
    pa_check(eval_postfix_extended(tokens) == -5, 'Unexpected result')
    pa_check(tokens == [2, 3, 4, '+', '-'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_15():
    tokens = [2, 3, '-', 4, '-']
    pa_check(eval_postfix_extended(tokens) == -5, 'Unexpected result')
    pa_check(tokens == [2, 3, '-', 4, '-'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_16():
    tokens = [8, 2, 2, '/', '/']
    pa_check(eval_postfix_extended(tokens) == 8.0, 'Unexpected result')
    pa_check(tokens == [8, 2, 2, '/', '/'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_17():
    tokens = [2, 3, '+', 'neg']
    pa_check(eval_postfix_extended(tokens) == -5, 'Unexpected result')
    pa_check(tokens == [2, 3, '+', 'neg'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_18():
    tokens = [2, 3, 'neg', '+']
    pa_check(eval_postfix_extended(tokens) == -1, 'Unexpected result')
    pa_check(tokens == [2, 3, 'neg', '+'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_19():
    tokens = [2, 'neg', 3, 'neg', '*']
    pa_check(eval_postfix_extended(tokens) == 6, 'Unexpected result')
    pa_check(tokens == [2, 'neg', 3, 'neg', '*'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_20():
    tokens = [5, 5, '-', 2, '/']
    pa_check(eval_postfix_extended(tokens) == 0.0, 'Unexpected result')
    pa_check(tokens == [5, 5, '-', 2, '/'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_21():
    tokens = [1.5, 2, '*']
    pa_check(eval_postfix_extended(tokens) == 3.0, 'Unexpected result')
    pa_check(tokens == [1.5, 2, '*'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_22():
    tokens = [-8, 2, '/']
    pa_check(eval_postfix_extended(tokens) == -4.0, 'Unexpected result')
    pa_check(tokens == [-8, 2, '/'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_23():
    tokens = [2, 3, '+', 4, 1, '-', '*']
    pa_check(eval_postfix_extended(tokens) == 15, 'Unexpected result')
    pa_check(tokens == [2, 3, '+', 4, 1, '-', '*'], "Tokens changed")
    return pa_case_ok[0]

def pa_case_24():
    tokens = [10, 2, '-', 3, 1, '+', '/', 'neg']
    pa_check(eval_postfix_extended(tokens) == -2.0, 'Unexpected result')
    pa_check(tokens == [10, 2, '-', 3, 1, '+', '/', 'neg'], "Tokens changed")
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Postfix [123]', "Postfix [9, 4, '-']", "Postfix [2, 8, '/']", "Postfix [8, 3, '-', 'neg', 2, '/']", "Postfix [0, 'neg']", "Postfix [-3, 'neg']", "Postfix [5, 'neg', 'neg']", "Postfix [1, 2, '+']", "Postfix [2, 3, '*']", "Postfix [1, 8, '-']", "Postfix [4, 2, '/']", "Postfix [3, 4, '+', 2, '*']", "Postfix [3, 4, 2, '*', '+']", "Postfix [2, 3, 4, '+', '-']", "Postfix [2, 3, '-', 4, '-']", "Postfix [8, 2, 2, '/', '/']", "Postfix [2, 3, '+', 'neg']", "Postfix [2, 3, 'neg', '+']", "Postfix [2, 'neg', 3, 'neg', '*']", "Postfix [5, 5, '-', 2, '/']", "Postfix [1.5, 2, '*']", "Postfix [-8, 2, '/']", "Postfix [2, 3, '+', 4, 1, '-', '*']", "Postfix [10, 2, '-', 3, 1, '+', '/', 'neg']"]
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
print("D12 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
