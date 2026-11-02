# D04 | Source Academy Python §3

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

def running_totals(xs, start):
    if is_none(xs):
        return None
    updated = start + head(xs)
    return pair(updated, running_totals(tail(xs), updated))

def pa_case_01():
    xs = pa_list([])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 0)
    pa_values(result, [])
    pa_fresh(result, saved, 0)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_02():
    xs = pa_list([8])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 10)
    pa_values(result, [18])
    pa_fresh(result, saved, 1)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_03():
    xs = pa_list([4, 4])
    saved = pa_snapshot(xs)
    result = running_totals(xs, -8)
    pa_values(result, [-4, 0])
    pa_fresh(result, saved, 2)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_04():
    xs = pa_list([5, 2, -4, 3])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 5)
    pa_values(result, [10, 12, 8, 11])
    pa_fresh(result, saved, 4)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_05():
    xs = pa_list([0])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 0)
    pa_values(result, [0])
    pa_fresh(result, saved, 1)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_06():
    xs = pa_list([-7])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 10)
    pa_values(result, [3])
    pa_fresh(result, saved, 1)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_07():
    xs = pa_list([1, 2])
    saved = pa_snapshot(xs)
    result = running_totals(xs, -8)
    pa_values(result, [-7, -5])
    pa_fresh(result, saved, 2)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_08():
    xs = pa_list([2, 1])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 5)
    pa_values(result, [7, 8])
    pa_fresh(result, saved, 2)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_09():
    xs = pa_list([0, 0, 0])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 0)
    pa_values(result, [0, 0, 0])
    pa_fresh(result, saved, 3)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_10():
    xs = pa_list([5, 5, 5, 5, 5, 5, 5])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 10)
    pa_values(result, [15, 20, 25, 30, 35, 40, 45])
    pa_fresh(result, saved, 7)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_11():
    xs = pa_list([-1, -2, -3])
    saved = pa_snapshot(xs)
    result = running_totals(xs, -8)
    pa_values(result, [-9, -11, -14])
    pa_fresh(result, saved, 3)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_12():
    xs = pa_list([1, -1, 1, -1, 1, -1, 1, -1, 1, -1])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 5)
    pa_values(result, [6, 5, 6, 5, 6, 5, 6, 5, 6, 5])
    pa_fresh(result, saved, 10)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_13():
    xs = pa_list([0, 1, 2, 3, 4, 5, 6, 7, 8])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 0)
    pa_values(result, [0, 1, 3, 6, 10, 15, 21, 28, 36])
    pa_fresh(result, saved, 9)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_14():
    xs = pa_list([9, 8, 7, 6, 5, 4, 3, 2, 1])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 10)
    pa_values(result, [19, 27, 34, 40, 45, 49, 52, 54, 55])
    pa_fresh(result, saved, 9)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_15():
    xs = pa_list([3, 3, 1, 3, 3, 3])
    saved = pa_snapshot(xs)
    result = running_totals(xs, -8)
    pa_values(result, [-5, -2, -1, 2, 5, 8])
    pa_fresh(result, saved, 6)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_16():
    xs = pa_list([0, 7, 0, -2, 0])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 5)
    pa_values(result, [5, 12, 12, 10, 10])
    pa_fresh(result, saved, 5)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_17():
    xs = pa_list([1000000, -1000000, 1])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 0)
    pa_values(result, [1000000, 0, 1])
    pa_fresh(result, saved, 3)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_18():
    xs = pa_list([-4, -1, 2, -6])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 10)
    pa_values(result, [6, 5, 7, 1])
    pa_fresh(result, saved, 4)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_19():
    xs = pa_list([7, 11, 11, 11, -5])
    saved = pa_snapshot(xs)
    result = running_totals(xs, -8)
    pa_values(result, [-1, 10, 21, 32, 27])
    pa_fresh(result, saved, 5)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_20():
    xs = pa_list([-9, -9, -1, -5, 10, -10, -8, 12, 11, -4, -9])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 5)
    pa_values(result, [-4, -13, -14, -19, -9, -19, -27, -15, -4, -8, -17])
    pa_fresh(result, saved, 11)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_21():
    xs = pa_list([-8, 7, 9, 2, 8, 5, 7, 6, -7, 3, -8, 7, -7, 3, -6, 6])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 0)
    pa_values(result, [-8, -1, 8, 10, 18, 23, 30, 36, 29, 32, 24, 31, 24, 27, 21, 27])
    pa_fresh(result, saved, 16)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_22():
    xs = pa_list([-8, -7, -10, -9, -9, 8, 9, -10, 9, -6, 5, -12, -11, -4, -6, 2, 4, 3, 2, -11, -12, -4, -8])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 10)
    pa_values(result, [2, -5, -15, -24, -33, -25, -16, -26, -17, -23, -18, -30, -41, -45, -51, -49, -45, -42, -40, -51, -63, -67, -75])
    pa_fresh(result, saved, 23)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_23():
    xs = pa_list([5, 12, -5, 5, -1, -5, 0, 4, -12, 7, 12, -1, 5, -10, 0, -8, 0, 6, -8, -3, -10, 1, 2, 0, 2, 1, 3, -12, -3, -1, 5, 2, -1, 6, 6, 7, 5, 6, -8, 5])
    saved = pa_snapshot(xs)
    result = running_totals(xs, -8)
    pa_values(result, [-3, 9, 4, 9, 8, 3, 3, 7, -5, 2, 14, 13, 18, 8, 8, 0, 0, 6, -2, -5, -15, -14, -12, -12, -10, -9, -6, -18, -21, -22, -17, -15, -16, -10, -4, 3, 8, 14, 6, 11])
    pa_fresh(result, saved, 40)
    pa_unchanged(saved)
    return pa_case_ok[0]

def pa_case_24():
    xs = pa_list([-10, -7, 0, -4, 2, 5, 0, -9, -6, 12, 4, -11, 9, -9, 5, 8, 12, 7, 8, 9, 4, -12, -10, -5, 8, -2, 4, -5, 0, -8, 0, 5, 1, -1, 2, -7, 10, -10, 11, -1, 9, -3, -3, 0, -3, 10, 5, 10, 8, 2, -8, -9, 12, -10, 5, 8, 3, -9, 8, 4, 1, 1, -5, 3, -2, -10, -5, 11, 6, 0, 0, -11, 8, 3, 1, 3, 2, 3, -3, -1])
    saved = pa_snapshot(xs)
    result = running_totals(xs, 5)
    pa_values(result, [-5, -12, -12, -16, -14, -9, -9, -18, -24, -12, -8, -19, -10, -19, -14, -6, 6, 13, 21, 30, 34, 22, 12, 7, 15, 13, 17, 12, 12, 4, 4, 9, 10, 9, 11, 4, 14, 4, 15, 14, 23, 20, 17, 17, 14, 24, 29, 39, 47, 49, 41, 32, 44, 34, 39, 47, 50, 41, 49, 53, 54, 55, 50, 53, 51, 41, 36, 47, 53, 53, 53, 42, 50, 53, 54, 57, 59, 62, 59, 58])
    pa_fresh(result, saved, 80)
    pa_unchanged(saved)
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Empty, start 0', 'Singleton, start 10', 'Equal pair, start -8', 'Mixed signs, start 5', 'Length 1 / pattern 5, start 0', 'Length 1 / pattern 6, start 10', 'Length 2 / pattern 7, start -8', 'Length 2 / pattern 8, start 5', 'Length 3 / pattern 9, start 0', 'Length 7 / pattern 10, start 10', 'Length 3 / pattern 11, start -8', 'Length 10 / pattern 12, start 5', 'Length 9 / pattern 13, start 0', 'Length 9 / pattern 14, start 10', 'Length 6 / pattern 15, start -8', 'Length 5 / pattern 16, start 5', 'Length 3 / pattern 17, start 0', 'Length 4 / pattern 18, start 10', 'Length 5 / pattern 19, start -8', 'Length 11 / pattern 20, start 5', 'Length 16 / pattern 21, start 0', 'Length 23 / pattern 22, start 10', 'Length 40 / pattern 23, start -8', 'Length 80 / pattern 24, start 5']
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
print("D04 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
