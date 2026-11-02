# D11 | Source Academy Python §3

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

def snake_rows(rows, cols):
    out = [None] * rows
    for r in range(rows):
        out[r] = [0] * cols
        for c in range(cols):
            offset = c if r % 2 == 0 else cols - 1 - c
            out[r][c] = r * cols + offset + 1
    return out

def pa_case_01():
    result = snake_rows(1, 1)
    pa_check(result == [[1]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_02():
    result = snake_rows(1, 4)
    pa_check(result == [[1, 2, 3, 4]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_03():
    result = snake_rows(4, 1)
    pa_check(result == [[1], [2], [3], [4]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_04():
    result = snake_rows(2, 3)
    pa_check(result == [[1, 2, 3], [6, 5, 4]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_05():
    result = snake_rows(3, 2)
    pa_check(result == [[1, 2], [4, 3], [5, 6]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_06():
    result = snake_rows(2, 2)
    pa_check(result == [[1, 2], [4, 3]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_07():
    result = snake_rows(3, 3)
    pa_check(result == [[1, 2, 3], [6, 5, 4], [7, 8, 9]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_08():
    result = snake_rows(2, 7)
    pa_check(result == [[1, 2, 3, 4, 5, 6, 7], [14, 13, 12, 11, 10, 9, 8]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_09():
    result = snake_rows(7, 2)
    pa_check(result == [[1, 2], [4, 3], [5, 6], [8, 7], [9, 10], [12, 11], [13, 14]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_10():
    result = snake_rows(4, 5)
    pa_check(result == [[1, 2, 3, 4, 5], [10, 9, 8, 7, 6], [11, 12, 13, 14, 15], [20, 19, 18, 17, 16]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_11():
    result = snake_rows(5, 4)
    pa_check(result == [[1, 2, 3, 4], [8, 7, 6, 5], [9, 10, 11, 12], [16, 15, 14, 13], [17, 18, 19, 20]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_12():
    result = snake_rows(6, 3)
    pa_check(result == [[1, 2, 3], [6, 5, 4], [7, 8, 9], [12, 11, 10], [13, 14, 15], [18, 17, 16]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_13():
    result = snake_rows(3, 6)
    pa_check(result == [[1, 2, 3, 4, 5, 6], [12, 11, 10, 9, 8, 7], [13, 14, 15, 16, 17, 18]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_14():
    result = snake_rows(1, 9)
    pa_check(result == [[1, 2, 3, 4, 5, 6, 7, 8, 9]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_15():
    result = snake_rows(9, 1)
    pa_check(result == [[1], [2], [3], [4], [5], [6], [7], [8], [9]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_16():
    result = snake_rows(2, 8)
    pa_check(result == [[1, 2, 3, 4, 5, 6, 7, 8], [16, 15, 14, 13, 12, 11, 10, 9]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_17():
    result = snake_rows(8, 2)
    pa_check(result == [[1, 2], [4, 3], [5, 6], [8, 7], [9, 10], [12, 11], [13, 14], [16, 15]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_18():
    result = snake_rows(4, 4)
    pa_check(result == [[1, 2, 3, 4], [8, 7, 6, 5], [9, 10, 11, 12], [16, 15, 14, 13]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_19():
    result = snake_rows(5, 5)
    pa_check(result == [[1, 2, 3, 4, 5], [10, 9, 8, 7, 6], [11, 12, 13, 14, 15], [20, 19, 18, 17, 16], [21, 22, 23, 24, 25]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_20():
    result = snake_rows(6, 2)
    pa_check(result == [[1, 2], [4, 3], [5, 6], [8, 7], [9, 10], [12, 11]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_21():
    result = snake_rows(2, 6)
    pa_check(result == [[1, 2, 3, 4, 5, 6], [12, 11, 10, 9, 8, 7]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_22():
    result = snake_rows(7, 3)
    pa_check(result == [[1, 2, 3], [6, 5, 4], [7, 8, 9], [12, 11, 10], [13, 14, 15], [18, 17, 16], [19, 20, 21]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_23():
    result = snake_rows(3, 7)
    pa_check(result == [[1, 2, 3, 4, 5, 6, 7], [14, 13, 12, 11, 10, 9, 8], [15, 16, 17, 18, 19, 20, 21]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

def pa_case_24():
    result = snake_rows(8, 5)
    pa_check(result == [[1, 2, 3, 4, 5], [10, 9, 8, 7, 6], [11, 12, 13, 14, 15], [20, 19, 18, 17, 16], [21, 22, 23, 24, 25], [30, 29, 28, 27, 26], [31, 32, 33, 34, 35], [40, 39, 38, 37, 36]], 'Unexpected result')
    pa_matrix_fresh(result, [])
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Snake 1 by 1', 'Snake 1 by 4', 'Snake 4 by 1', 'Snake 2 by 3', 'Snake 3 by 2', 'Snake 2 by 2', 'Snake 3 by 3', 'Snake 2 by 7', 'Snake 7 by 2', 'Snake 4 by 5', 'Snake 5 by 4', 'Snake 6 by 3', 'Snake 3 by 6', 'Snake 1 by 9', 'Snake 9 by 1', 'Snake 2 by 8', 'Snake 8 by 2', 'Snake 4 by 4', 'Snake 5 by 5', 'Snake 6 by 2', 'Snake 2 by 6', 'Snake 7 by 3', 'Snake 3 by 7', 'Snake 8 by 5']
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
print("D11 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
