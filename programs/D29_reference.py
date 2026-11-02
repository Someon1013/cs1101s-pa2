# D29 | Source Academy Python §3
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

def pa_case_01():
    source = pa_stream([])
    s = expand_run_stream(source)
    pa_prefix(s, [], True, True)
    return pa_case_ok[0]

def pa_case_02():
    source = pa_stream([pair(5, 1)])
    s = expand_run_stream(source)
    pa_prefix(s, [5], True, True)
    return pa_case_ok[0]

def pa_case_03():
    source = pa_stream([pair(5, 2), pair(-1, 3)])
    s = expand_run_stream(source)
    pa_prefix(s, [5, 5, -1, -1, -1], True, True)
    return pa_case_ok[0]

def pa_case_04():
    source = pa_stream([pair(0, 4)])
    s = expand_run_stream(source)
    pa_prefix(s, [0, 0, 0, 0], True, True)
    return pa_case_ok[0]

def pa_case_05():
    source = pa_stream([pair(2, 1), pair(2, 3)])
    s = expand_run_stream(source)
    pa_prefix(s, [2, 2, 2, 2], True, True)
    return pa_case_ok[0]

def pa_case_06():
    source = pa_stream([pair(1, 80)])
    s = expand_run_stream(source)
    pa_prefix(s, [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], True, True)
    return pa_case_ok[0]

def pa_case_07():
    source = pa_stream([pair(0, 1), pair(-2, 1), pair(5, 1)])
    s = expand_run_stream(source)
    pa_prefix(s, [0, -2, 5], True, True)
    return pa_case_ok[0]

def pa_case_08():
    source = pa_stream([pair(2, 3)])
    s = expand_run_stream(source)
    pa_prefix(s, [2, 2, 2], True, True)
    return pa_case_ok[0]

def pa_case_09():
    source = pa_stream([pair(2, 8), pair(-1, 4)])
    s = expand_run_stream(source)
    pa_prefix(s, [2, 2, 2, 2, 2, 2, 2, 2, -1, -1, -1, -1], True, True)
    return pa_case_ok[0]

def pa_case_10():
    source = pa_stream([pair(-3, 7), pair(1, 5), pair(0, 4)])
    s = expand_run_stream(source)
    pa_prefix(s, [-3, -3, -3, -3, -3, -3, -3, 1, 1, 1, 1, 1, 0, 0, 0, 0], True, True)
    return pa_case_ok[0]

def pa_case_11():
    source = pa_stream([pair(2, 7), pair(3, 2), pair(1, 1), pair(-2, 2)])
    s = expand_run_stream(source)
    pa_prefix(s, [2, 2, 2, 2, 2, 2, 2, 3, 3, 1, -2, -2], True, True)
    return pa_case_ok[0]

def pa_case_12():
    source = pa_stream([pair(1, 7), pair(-1, 4), pair(2, 8), pair(2, 1), pair(0, 2)])
    s = expand_run_stream(source)
    pa_prefix(s, [1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0], True, True)
    return pa_case_ok[0]

def pa_case_13():
    source = pa_stream([pair(1, 4), pair(1, 5), pair(2, 3), pair(3, 7), pair(-1, 8), pair(-2, 4)])
    s = expand_run_stream(source)
    pa_prefix(s, [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, -1, -1, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2], True, True)
    return pa_case_ok[0]

def pa_case_14():
    source = pa_stream([pair(-2, 2), pair(2, 4), pair(-3, 4), pair(-3, 3), pair(3, 8), pair(3, 5), pair(-3, 5)])
    s = expand_run_stream(source)
    pa_prefix(s, [-2, -2, 2, 2, 2, 2, -3, -3, -3, -3, -3, -3, -3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, -3, -3, -3, -3, -3], True, True)
    return pa_case_ok[0]

def pa_case_15():
    source = pa_stream([pair(-2, 2)])
    s = expand_run_stream(source)
    pa_prefix(s, [-2, -2], True, True)
    return pa_case_ok[0]

def pa_case_16():
    source = pa_stream([pair(3, 3), pair(-1, 6)])
    s = expand_run_stream(source)
    pa_prefix(s, [3, 3, 3, -1, -1, -1, -1, -1, -1], True, True)
    return pa_case_ok[0]

def pa_case_17():
    source = pa_stream([pair(1, 3), pair(-1, 1), pair(2, 3)])
    s = expand_run_stream(source)
    pa_prefix(s, [1, 1, 1, -1, 2, 2, 2], True, True)
    return pa_case_ok[0]

def pa_case_18():
    source = pa_stream([pair(-1, 6), pair(2, 8), pair(0, 4), pair(3, 3)])
    s = expand_run_stream(source)
    pa_prefix(s, [-1, -1, -1, -1, -1, -1, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 3, 3], True, True)
    return pa_case_ok[0]

def pa_case_19():
    forced = [0]
    record = pair(7, 1000000)
    source = pa_counted_stream([record], forced)
    s = expand_run_stream(source)
    pa_prefix(s, [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], False, True)
    pa_check(forced[0] == 0, "Run source advanced too early")
    pa_check(head(record) == 7 and tail(record) == 1000000, "Run record mutated")
    return pa_case_ok[0]

def pa_case_20():
    forced = [0]
    record = pair(-2, 1000000)
    source = pa_counted_stream([record], forced)
    s = expand_run_stream(source)
    pa_prefix(s, [-2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2], False, True)
    pa_check(forced[0] == 0, "Run source advanced too early")
    pa_check(head(record) == -2 and tail(record) == 1000000, "Run record mutated")
    return pa_case_ok[0]

def pa_case_21():
    def source(i):
        return pair(pair(i, 1), lambda: source(i + 1))
    s = expand_run_stream(source(0))
    pa_prefix(s, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59], False, True)
    return pa_case_ok[0]

def pa_case_22():
    def source(i):
        return pair(pair(i, 3), lambda: source(i + 1))
    s = expand_run_stream(source(0))
    pa_prefix(s, [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 10, 11, 11, 11, 12, 12, 12, 13, 13, 13, 14, 14, 14, 15, 15, 15, 16, 16, 16, 17, 17, 17, 18, 18, 18, 19, 19, 19], False, True)
    return pa_case_ok[0]

def pa_case_23():
    forced = [0]
    source = pa_counted_stream([pair(7, 1), pair(9, 2)], forced)
    s = expand_run_stream(source)
    pa_check(forced[0] == 0, "Construction forced next run")
    current = s
    for i in range(0):
        current = stream_tail(current)
    pa_check(forced[0] == 0, "Early run boundary")
    next_run = stream_tail(current)
    pa_check(head(next_run) == 9, "Wrong next run")
    pa_check(forced[0] == 1, "Expected one boundary force")
    pa_check(stream_tail(current) is next_run, "Boundary not memoized")
    pa_check(forced[0] == 1, "Boundary work repeated")
    return pa_case_ok[0]

def pa_case_24():
    forced = [0]
    source = pa_counted_stream([pair(7, 2), pair(9, 2)], forced)
    s = expand_run_stream(source)
    pa_check(forced[0] == 0, "Construction forced next run")
    current = s
    for i in range(1):
        current = stream_tail(current)
    pa_check(forced[0] == 0, "Early run boundary")
    next_run = stream_tail(current)
    pa_check(head(next_run) == 9, "Wrong next run")
    pa_check(forced[0] == 1, "Expected one boundary force")
    pa_check(stream_tail(current) is next_run, "Boundary not memoized")
    pa_check(forced[0] == 1, "Boundary work repeated")
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Run stream 1, output length 0', 'Run stream 2, output length 1', 'Run stream 3, output length 5', 'Run stream 4, output length 4', 'Run stream 5, output length 4', 'Run stream 6, output length 80', 'Run stream 7, output length 3', 'Run stream 8, output length 3', 'Run stream 9, output length 12', 'Run stream 10, output length 16', 'Run stream 11, output length 12', 'Run stream 12, output length 22', 'Run stream 13, output length 31', 'Run stream 14, output length 31', 'Run stream 15, output length 2', 'Run stream 16, output length 9', 'Run stream 17, output length 7', 'Run stream 18, output length 21', 'Huge run stays lazy 7', 'Huge run stays lazy -2', 'Infinite stream of runs with count 1', 'Infinite stream of runs with count 3', 'Run boundary memoization, count 1', 'Run boundary memoization, count 2']
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
print("D29 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
