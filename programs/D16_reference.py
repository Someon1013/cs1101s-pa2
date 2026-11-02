# D16 | Source Academy Python §3

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

def d_merge_desc(xs, ys):
    if is_none(xs):
        return ys
    if is_none(ys):
        return xs
    if head(xs) >= head(ys):
        set_tail(xs, d_merge_desc(tail(xs), ys))
        return xs
    set_tail(ys, d_merge_desc(xs, tail(ys)))
    return ys

def pa_case_01():
    xs = pa_list([])
    ys = pa_list([])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_02():
    xs = pa_list([8])
    ys = pa_list([])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_03():
    xs = pa_list([])
    ys = pa_list([4, 4])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_04():
    xs = pa_list([9, 4, 4])
    ys = pa_list([8, 4, 1])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_05():
    xs = pa_list([0])
    ys = pa_list([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_06():
    xs = pa_list([-7])
    ys = pa_list([8, 7, 6, 5, 4, 3, 2, 1, 0])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_07():
    xs = pa_list([2, 1])
    ys = pa_list([9, 8, 7, 6, 5, 4, 3, 2, 1])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_08():
    xs = pa_list([2, 1])
    ys = pa_list([3, 3, 3, 3, 3, 1])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_09():
    xs = pa_list([0, 0, 0])
    ys = pa_list([7, 0, 0, 0, -2])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -2, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_10():
    xs = pa_list([5, 5, 5, 5, 5, 5, 5])
    ys = pa_list([1000000, 1, -1000000])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1000000, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1000000, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_11():
    xs = pa_list([-1, -2, -3])
    ys = pa_list([2, -1, -4, -6])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -2, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_12():
    xs = pa_list([1, 1, 1, 1, 1, -1, -1, -1, -1, -1])
    ys = pa_list([11, 11, 11, 7, -5])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_13():
    xs = pa_list([8, 7, 6, 5, 4, 3, 2, 1, 0])
    ys = pa_list([12, 11, 10, -1, -4, -5, -8, -9, -9, -9, -10])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 10, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is b[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is b[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_14():
    xs = pa_list([9, 8, 7, 6, 5, 4, 3, 2, 1])
    ys = pa_list([9, 8, 7, 7, 7, 6, 5, 3, 2, -7, -8, -8])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is b[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is b[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_15():
    xs = pa_list([3, 3, 3, 3, 3, 1])
    ys = pa_list([9, 9, 8, 5, -6, -7, -8, -9, -9, -10, -10, -12])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is b[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is b[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is b[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_16():
    xs = pa_list([7, 0, 0, 0, -2])
    ys = pa_list([12, 12, 7, 5, 5, 4, 0, -1, -1, -5, -5, -12])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -2, "Head changed")
    current = tail(current)
    pa_check(current is b[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is b[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is b[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_17():
    xs = pa_list([1000000, 1, -1000000])
    ys = pa_list([12, 5, 4, 2, 0, 0, -4, -6, -7, -9, -10, -11])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1000000, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is b[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is b[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(current is b[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is b[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is b[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is b[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -11, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1000000, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_18():
    xs = pa_list([2, -1, -4, -6])
    ys = pa_list([])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_19():
    xs = pa_list([11, 11, 11, 7, -5])
    ys = pa_list([8])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_20():
    xs = pa_list([12, 11, 10, -1, -4, -5, -8, -9, -9, -9, -10])
    ys = pa_list([4, 4])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 10, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_21():
    xs = pa_list([9, 8, 7, 7, 7, 6, 6, 5, 3, 3, 2, -6, -7, -7, -8, -8])
    ys = pa_list([5, 3, 2, -4])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is a[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(current is a[12][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is a[13][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is a[14][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[15][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_22():
    xs = pa_list([9, 9, 8, 5, 4, 3, 2, 2, -4, -4, -6, -6, -7, -8, -8, -9, -9, -10, -10, -11, -11, -12, -12])
    ys = pa_list([0])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is a[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is a[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(current is a[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(current is a[12][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is a[13][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[14][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[15][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[16][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[17][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[18][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[19][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -11, "Head changed")
    current = tail(current)
    pa_check(current is a[20][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -11, "Head changed")
    current = tail(current)
    pa_check(current is a[21][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(current is a[22][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_23():
    xs = pa_list([12, 12, 7, 7, 6, 6, 6, 6, 5, 5, 5, 5, 5, 5, 4, 3, 2, 2, 2, 1, 1, 0, 0, 0, 0, -1, -1, -1, -1, -3, -3, -5, -5, -8, -8, -8, -10, -10, -12, -12])
    ys = pa_list([-7])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[12][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[13][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[14][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[15][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[16][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[17][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[18][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[19][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[20][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[21][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[22][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[23][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[24][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[25][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[26][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[27][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[28][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[29][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is a[30][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is a[31][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is a[32][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is a[33][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[34][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[35][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[36][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[37][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[38][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(current is a[39][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

def pa_case_24():
    xs = pa_list([12, 12, 12, 11, 11, 10, 10, 10, 9, 9, 9, 8, 8, 8, 8, 8, 8, 8, 7, 6, 5, 5, 5, 5, 5, 4, 4, 4, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -2, -2, -3, -3, -3, -3, -4, -5, -5, -5, -5, -6, -7, -7, -8, -8, -9, -9, -9, -9, -10, -10, -10, -10, -10, -11, -11, -12])
    ys = pa_list([2, 1])
    a = pa_snapshot(xs)
    b = pa_snapshot(ys)
    result = d_merge_desc(xs, ys)
    current = result
    pa_check(current is a[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[2][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 12, "Head changed")
    current = tail(current)
    pa_check(current is a[3][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is a[4][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 11, "Head changed")
    current = tail(current)
    pa_check(current is a[5][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 10, "Head changed")
    current = tail(current)
    pa_check(current is a[6][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 10, "Head changed")
    current = tail(current)
    pa_check(current is a[7][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 10, "Head changed")
    current = tail(current)
    pa_check(current is a[8][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[9][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[10][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 9, "Head changed")
    current = tail(current)
    pa_check(current is a[11][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[12][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[13][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[14][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[15][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[16][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[17][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 8, "Head changed")
    current = tail(current)
    pa_check(current is a[18][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 7, "Head changed")
    current = tail(current)
    pa_check(current is a[19][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 6, "Head changed")
    current = tail(current)
    pa_check(current is a[20][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[21][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[22][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[23][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[24][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 5, "Head changed")
    current = tail(current)
    pa_check(current is a[25][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[26][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[27][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[28][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 4, "Head changed")
    current = tail(current)
    pa_check(current is a[29][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[30][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[31][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[32][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[33][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 3, "Head changed")
    current = tail(current)
    pa_check(current is a[34][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[35][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[36][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[37][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is b[0][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 2, "Head changed")
    current = tail(current)
    pa_check(current is a[38][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[39][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[40][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[41][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is b[1][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 1, "Head changed")
    current = tail(current)
    pa_check(current is a[42][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[43][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[44][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[45][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[46][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[47][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[48][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == 0, "Head changed")
    current = tail(current)
    pa_check(current is a[49][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[50][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[51][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -1, "Head changed")
    current = tail(current)
    pa_check(current is a[52][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -2, "Head changed")
    current = tail(current)
    pa_check(current is a[53][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -2, "Head changed")
    current = tail(current)
    pa_check(current is a[54][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is a[55][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is a[56][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is a[57][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -3, "Head changed")
    current = tail(current)
    pa_check(current is a[58][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -4, "Head changed")
    current = tail(current)
    pa_check(current is a[59][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is a[60][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is a[61][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is a[62][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -5, "Head changed")
    current = tail(current)
    pa_check(current is a[63][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -6, "Head changed")
    current = tail(current)
    pa_check(current is a[64][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is a[65][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -7, "Head changed")
    current = tail(current)
    pa_check(current is a[66][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[67][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -8, "Head changed")
    current = tail(current)
    pa_check(current is a[68][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[69][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[70][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[71][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -9, "Head changed")
    current = tail(current)
    pa_check(current is a[72][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[73][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[74][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[75][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[76][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -10, "Head changed")
    current = tail(current)
    pa_check(current is a[77][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -11, "Head changed")
    current = tail(current)
    pa_check(current is a[78][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -11, "Head changed")
    current = tail(current)
    pa_check(current is a[79][0], "Merge identity / stable tie order")
    if not is_pair(current):
        return False
    pa_check(head(current) == -12, "Head changed")
    current = tail(current)
    pa_check(is_none(current), "Extra nodes or cycle")
    pa_heads(a)
    pa_heads(b)
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Left 0, right 0 / pattern 1', 'Left 1, right 0 / pattern 2', 'Left 0, right 2 / pattern 3', 'Left 3, right 3 / pattern 4', 'Left 1, right 10 / pattern 5', 'Left 1, right 9 / pattern 6', 'Left 2, right 9 / pattern 7', 'Left 2, right 6 / pattern 8', 'Left 3, right 5 / pattern 9', 'Left 7, right 3 / pattern 10', 'Left 3, right 4 / pattern 11', 'Left 10, right 5 / pattern 12', 'Left 9, right 11 / pattern 13', 'Left 9, right 12 / pattern 14', 'Left 6, right 12 / pattern 15', 'Left 5, right 12 / pattern 16', 'Left 3, right 12 / pattern 17', 'Left 4, right 0 / pattern 18', 'Left 5, right 1 / pattern 19', 'Left 11, right 2 / pattern 20', 'Left 16, right 4 / pattern 21', 'Left 23, right 1 / pattern 22', 'Left 40, right 1 / pattern 23', 'Left 80, right 2 / pattern 24']
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
print("D16 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
