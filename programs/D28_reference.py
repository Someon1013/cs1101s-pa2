# D28 | Source Academy Python §3
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

def interleave(s, t):
    if is_none(s):
        return t
    return pair(head(s), memo_fun(lambda: interleave(t, stream_tail(s))))

def pa_case_01():
    a = pa_stream([])
    b = pa_stream([])
    s = interleave(a, b)
    pa_prefix(s, [], True, False)
    return pa_case_ok[0]

def pa_case_02():
    a = pa_stream([1, 2, 3])
    b = pa_stream([8, 9])
    s = interleave(a, b)
    pa_prefix(s, [1, 8, 2, 9, 3], True, False)
    return pa_case_ok[0]

def pa_case_03():
    a = pa_stream([4, 4])
    b = pa_stream([1, 2])
    s = interleave(a, b)
    pa_prefix(s, [4, 1, 4, 2], True, False)
    return pa_case_ok[0]

def pa_case_04():
    a = pa_stream([5, 2, -4, 3])
    b = pa_stream([5, 5, 5, 5, 5, 5, 5])
    s = interleave(a, b)
    pa_prefix(s, [5, 5, 2, 5, -4, 5, 3, 5, 5, 5, 5], True, False)
    return pa_case_ok[0]

def pa_case_05():
    a = pa_stream([0])
    b = pa_stream([0, 1, 2, 3, 4, 5, 6, 7, 8])
    s = interleave(a, b)
    pa_prefix(s, [0, 0, 1, 2, 3, 4, 5, 6, 7, 8], True, False)
    return pa_case_ok[0]

def pa_case_06():
    a = pa_stream([-7])
    b = pa_stream([0, 7, 0, -2, 0])
    s = interleave(a, b)
    pa_prefix(s, [-7, 0, 7, 0, -2, 0], True, False)
    return pa_case_ok[0]

def pa_case_07():
    a = pa_stream([1, 2])
    b = pa_stream([7, 11, 11, 11, -5])
    s = interleave(a, b)
    pa_prefix(s, [1, 7, 2, 11, 11, 11, -5], True, False)
    return pa_case_ok[0]

def pa_case_08():
    a = pa_stream([2, 1])
    b = pa_stream([-8, -7, -10, -9, -9, 8, 9, -10, 9, -6])
    s = interleave(a, b)
    pa_prefix(s, [2, -8, 1, -7, -10, -9, -9, 8, 9, -10, 9, -6], True, False)
    return pa_case_ok[0]

def pa_case_09():
    a = pa_stream([0, 0, 0])
    b = pa_stream([])
    s = interleave(a, b)
    pa_prefix(s, [0, 0, 0], True, False)
    return pa_case_ok[0]

def pa_case_10():
    a = pa_stream([5, 5, 5, 5, 5, 5, 5])
    b = pa_stream([5, 2, -4, 3])
    s = interleave(a, b)
    pa_prefix(s, [5, 5, 5, 2, 5, -4, 5, 3, 5, 5, 5], True, False)
    return pa_case_ok[0]

def pa_case_11():
    a = pa_stream([-1, -2, -3])
    b = pa_stream([1, 2])
    s = interleave(a, b)
    pa_prefix(s, [-1, 1, -2, 2, -3], True, False)
    return pa_case_ok[0]

def pa_case_12():
    a = pa_stream([1, -1, 1, -1, 1, -1, 1, -1, 1, -1])
    b = pa_stream([5, 5, 5, 5, 5, 5, 5])
    s = interleave(a, b)
    pa_prefix(s, [1, 5, -1, 5, 1, 5, -1, 5, 1, 5, -1, 5, 1, 5, -1, 1, -1], True, False)
    return pa_case_ok[0]

def pa_case_13():
    a = pa_stream([0, 1, 2, 3, 4, 5, 6, 7, 8])
    b = pa_stream([0, 1, 2, 3, 4, 5, 6, 7, 8])
    s = interleave(a, b)
    pa_prefix(s, [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8], True, False)
    return pa_case_ok[0]

def pa_case_14():
    a = pa_stream([9, 8, 7, 6, 5, 4, 3, 2, 1])
    b = pa_stream([0, 7, 0, -2, 0])
    s = interleave(a, b)
    pa_prefix(s, [9, 0, 8, 7, 7, 0, 6, -2, 5, 0, 4, 3, 2, 1], True, False)
    return pa_case_ok[0]

def pa_case_15():
    a = pa_stream([3, 3, 1, 3, 3, 3])
    b = pa_stream([7, 11, 11, 11, -5])
    s = interleave(a, b)
    pa_prefix(s, [3, 7, 3, 11, 1, 11, 3, 11, 3, -5, 3], True, False)
    return pa_case_ok[0]

def pa_case_16():
    a = pa_stream([0, 7, 0, -2, 0])
    b = pa_stream([-8, -7, -10, -9, -9, 8, 9, -10, 9, -6])
    s = interleave(a, b)
    pa_prefix(s, [0, -8, 7, -7, 0, -10, -2, -9, 0, -9, 8, 9, -10, 9, -6], True, False)
    return pa_case_ok[0]

def pa_case_17():
    a = pa_stream([1000000, -1000000, 1])
    b = pa_stream([])
    s = interleave(a, b)
    pa_prefix(s, [1000000, -1000000, 1], True, False)
    return pa_case_ok[0]

def pa_case_18():
    a = pa_stream([-4, -1, 2, -6])
    b = pa_stream([5, 2, -4, 3])
    s = interleave(a, b)
    pa_prefix(s, [-4, 5, -1, 2, 2, -4, -6, 3], True, False)
    return pa_case_ok[0]

def pa_case_19():
    s = interleave(pa_integers(0, 1), pa_integers(100, 1))
    pa_prefix(s, [0, 100, 1, 101, 2, 102, 3, 103, 4, 104, 5, 105, 6, 106, 7, 107, 8, 108, 9, 109, 10, 110, 11, 111, 12, 112, 13, 113, 14, 114, 15, 115, 16, 116, 17, 117, 18, 118, 19, 119, 20, 120, 21, 121, 22, 122, 23, 123, 24, 124, 25, 125, 26, 126, 27, 127, 28, 128, 29, 129], False, True)
    return pa_case_ok[0]

def pa_case_20():
    s = interleave(pa_integers(10, -1), pa_integers(100, 1))
    pa_prefix(s, [10, 100, 9, 101, 8, 102, 7, 103, 6, 104, 5, 105, 4, 106, 3, 107, 2, 108, 1, 109, 0, 110, -1, 111, -2, 112, -3, 113, -4, 114, -5, 115, -6, 116, -7, 117, -8, 118, -9, 119, -10, 120, -11, 121, -12, 122, -13, 123, -14, 124, -15, 125, -16, 126, -17, 127, -18, 128, -19, 129], False, True)
    return pa_case_ok[0]

def pa_case_21():
    s = interleave(pa_integers(-10, 3), pa_integers(100, 1))
    pa_prefix(s, [-10, 100, -7, 101, -4, 102, -1, 103, 2, 104, 5, 105, 8, 106, 11, 107, 14, 108, 17, 109, 20, 110, 23, 111, 26, 112, 29, 113, 32, 114, 35, 115, 38, 116, 41, 117, 44, 118, 47, 119, 50, 120, 53, 121, 56, 122, 59, 123, 62, 124, 65, 125, 68, 126, 71, 127, 74, 128, 77, 129], False, True)
    return pa_case_ok[0]

def pa_case_22():
    s = interleave(pa_integers(0, 0), pa_integers(100, 1))
    pa_prefix(s, [0, 100, 0, 101, 0, 102, 0, 103, 0, 104, 0, 105, 0, 106, 0, 107, 0, 108, 0, 109, 0, 110, 0, 111, 0, 112, 0, 113, 0, 114, 0, 115, 0, 116, 0, 117, 0, 118, 0, 119, 0, 120, 0, 121, 0, 122, 0, 123, 0, 124, 0, 125, 0, 126, 0, 127, 0, 128, 0, 129], False, True)
    return pa_case_ok[0]

def pa_case_23():
    ca = [0]
    cb = [0]
    s = interleave(pa_counted_stream([1, 2, 3], ca), pa_counted_stream([8, 9], cb))
    pa_check(ca[0] == 0 and cb[0] == 0, "Construction forced an input")
    second = stream_tail(s)
    pa_check(head(second) == 8, "Wrong second source")
    pa_check(ca[0] <= 1 and cb[0] == 0, "Advanced input too far")
    old = ca[0]
    pa_check(stream_tail(s) is second, "New interleave tail not memoized")
    pa_check(ca[0] == old, "Repeated source work")
    return pa_case_ok[0]

def pa_case_24():
    ca = [0]
    cb = [0]
    s = interleave(pa_counted_stream([0, -1], ca), pa_counted_stream([4, 4, 4], cb))
    pa_check(ca[0] == 0 and cb[0] == 0, "Construction forced an input")
    second = stream_tail(s)
    pa_check(head(second) == 4, "Wrong second source")
    pa_check(ca[0] <= 1 and cb[0] == 0, "Advanced input too far")
    old = ca[0]
    pa_check(stream_tail(s) is second, "New interleave tail not memoized")
    pa_check(ca[0] == old, "Repeated source work")
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Finite lengths 0 and 0', 'Finite lengths 3 and 2', 'Finite lengths 2 and 2', 'Finite lengths 4 and 7', 'Finite lengths 1 and 9', 'Finite lengths 1 and 5', 'Finite lengths 2 and 5', 'Finite lengths 2 and 10', 'Finite lengths 3 and 0', 'Finite lengths 7 and 4', 'Finite lengths 3 and 2', 'Finite lengths 10 and 7', 'Finite lengths 9 and 9', 'Finite lengths 9 and 5', 'Finite lengths 6 and 5', 'Finite lengths 5 and 10', 'Finite lengths 3 and 0', 'Finite lengths 4 and 4', 'Two infinite sources 0, 1', 'Two infinite sources 10, -1', 'Two infinite sources -10, 3', 'Two infinite sources 0, 0', 'Interleave demand and sharing [1, 2, 3]', 'Interleave demand and sharing [0, -1]']
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
print("D28 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
