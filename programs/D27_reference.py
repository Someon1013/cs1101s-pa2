# D27 | Source Academy Python §3
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

def stream_scan(s, total):
    if is_none(s):
        return None
    updated = total + head(s)
    return pair(updated, memo_fun(lambda: stream_scan(stream_tail(s), updated)))

def pa_case_01():
    source = pa_stream([])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 0)
    pa_prefix(result, [], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 0, "Input head changed")
    return pa_case_ok[0]

def pa_case_02():
    source = pa_stream([8])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 10)
    pa_prefix(result, [18], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 8, "Input head changed")
    return pa_case_ok[0]

def pa_case_03():
    source = pa_stream([4, 4])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, -5)
    pa_prefix(result, [-1, 3], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 4, "Input head changed")
    return pa_case_ok[0]

def pa_case_04():
    source = pa_stream([5, 2, -4, 3])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 0)
    pa_prefix(result, [5, 7, 3, 6], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 5, "Input head changed")
    return pa_case_ok[0]

def pa_case_05():
    source = pa_stream([0])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 10)
    pa_prefix(result, [10], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 0, "Input head changed")
    return pa_case_ok[0]

def pa_case_06():
    source = pa_stream([-7])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, -5)
    pa_prefix(result, [-12], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == -7, "Input head changed")
    return pa_case_ok[0]

def pa_case_07():
    source = pa_stream([1, 2])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 0)
    pa_prefix(result, [1, 3], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 1, "Input head changed")
    return pa_case_ok[0]

def pa_case_08():
    source = pa_stream([2, 1])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 10)
    pa_prefix(result, [12, 13], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 2, "Input head changed")
    return pa_case_ok[0]

def pa_case_09():
    source = pa_stream([0, 0, 0])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, -5)
    pa_prefix(result, [-5, -5, -5], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 0, "Input head changed")
    return pa_case_ok[0]

def pa_case_10():
    source = pa_stream([5, 5, 5, 5, 5, 5, 5])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 0)
    pa_prefix(result, [5, 10, 15, 20, 25, 30, 35], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 5, "Input head changed")
    return pa_case_ok[0]

def pa_case_11():
    source = pa_stream([-1, -2, -3])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 10)
    pa_prefix(result, [9, 7, 4], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == -1, "Input head changed")
    return pa_case_ok[0]

def pa_case_12():
    source = pa_stream([1, -1, 1, -1, 1, -1, 1, -1, 1, -1])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, -5)
    pa_prefix(result, [-4, -5, -4, -5, -4, -5, -4, -5, -4, -5], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 1, "Input head changed")
    return pa_case_ok[0]

def pa_case_13():
    source = pa_stream([0, 1, 2, 3, 4, 5, 6, 7, 8])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 0)
    pa_prefix(result, [0, 1, 3, 6, 10, 15, 21, 28, 36], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 0, "Input head changed")
    return pa_case_ok[0]

def pa_case_14():
    source = pa_stream([9, 8, 7, 6, 5, 4, 3, 2, 1])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 10)
    pa_prefix(result, [19, 27, 34, 40, 45, 49, 52, 54, 55], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 9, "Input head changed")
    return pa_case_ok[0]

def pa_case_15():
    source = pa_stream([3, 3, 1, 3, 3, 3])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, -5)
    pa_prefix(result, [-2, 1, 2, 5, 8, 11], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 3, "Input head changed")
    return pa_case_ok[0]

def pa_case_16():
    source = pa_stream([0, 7, 0, -2, 0])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 0)
    pa_prefix(result, [0, 7, 7, 5, 5], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 0, "Input head changed")
    return pa_case_ok[0]

def pa_case_17():
    source = pa_stream([1000000, -1000000, 1])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, 10)
    pa_prefix(result, [1000010, 10, 11], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == 1000000, "Input head changed")
    return pa_case_ok[0]

def pa_case_18():
    source = pa_stream([-4, -1, 2, -6])
    old_tail = None if is_none(source) else tail(source)
    result = stream_scan(source, -5)
    pa_prefix(result, [-9, -10, -8, -14], True, True)
    if not is_none(source):
        pa_check(tail(source) is old_tail, "Input tail changed")
        pa_check(head(source) == -4, "Input head changed")
    return pa_case_ok[0]

def pa_case_19():
    source = pa_integers(0, 1)
    result = stream_scan(source, 11)
    pa_prefix(result, [11, 12, 14, 17, 21, 26, 32, 39, 47, 56, 66, 77, 89, 102, 116, 131, 147, 164, 182, 201, 221, 242, 264, 287, 311, 336, 362, 389, 417, 446, 476, 507, 539, 572, 606, 641, 677, 714, 752, 791, 831, 872, 914, 957, 1001, 1046, 1092, 1139, 1187, 1236], False, True)
    return pa_case_ok[0]

def pa_case_20():
    source = pa_integers(5, -2)
    result = stream_scan(source, 11)
    pa_prefix(result, [16, 19, 20, 19, 16, 11, 4, -5, -16, -29, -44, -61, -80, -101, -124, -149, -176, -205, -236, -269, -304, -341, -380, -421, -464, -509, -556, -605, -656, -709, -764, -821, -880, -941, -1004, -1069, -1136, -1205, -1276, -1349, -1424, -1501, -1580, -1661, -1744, -1829, -1916, -2005, -2096, -2189], False, True)
    return pa_case_ok[0]

def pa_case_21():
    source = pa_integers(-7, 0)
    result = stream_scan(source, 11)
    pa_prefix(result, [4, -3, -10, -17, -24, -31, -38, -45, -52, -59, -66, -73, -80, -87, -94, -101, -108, -115, -122, -129, -136, -143, -150, -157, -164, -171, -178, -185, -192, -199, -206, -213, -220, -227, -234, -241, -248, -255, -262, -269, -276, -283, -290, -297, -304, -311, -318, -325, -332, -339], False, True)
    return pa_case_ok[0]

def pa_case_22():
    source = pa_integers(100, 3)
    result = stream_scan(source, 11)
    pa_prefix(result, [111, 214, 320, 429, 541, 656, 774, 895, 1019, 1146, 1276, 1409, 1545, 1684, 1826, 1971, 2119, 2270, 2424, 2581, 2741, 2904, 3070, 3239, 3411, 3586, 3764, 3945, 4129, 4316, 4506, 4699, 4895, 5094, 5296, 5501, 5709, 5920, 6134, 6351, 6571, 6794, 7020, 7249, 7481, 7716, 7954, 8195, 8439, 8686], False, True)
    return pa_case_ok[0]

def pa_case_23():
    forced = [0]
    source = pa_counted_stream([2, 5, 9, 14], forced)
    old_tail = tail(source)
    result = stream_scan(source, 10)
    pa_check(forced[0] <= 0, "Forced too much at construction")
    first = stream_tail(result)
    pa_check(forced[0] <= 1, "Forced too far for second result")
    count = forced[0]
    pa_check(stream_tail(result) is first, "Repeated tail identity")
    pa_check(forced[0] == count, "Repeated forcing repeated source work")
    pa_check(tail(source) is old_tail, "Source tail changed")
    return pa_case_ok[0]

def pa_case_24():
    forced = [0]
    source = pa_counted_stream([0, -1, -3, -6], forced)
    old_tail = tail(source)
    result = stream_scan(source, 10)
    pa_check(forced[0] <= 0, "Forced too much at construction")
    first = stream_tail(result)
    pa_check(forced[0] <= 1, "Forced too far for second result")
    count = forced[0]
    pa_check(stream_tail(result) is first, "Repeated tail identity")
    pa_check(forced[0] == count, "Repeated forcing repeated source work")
    pa_check(tail(source) is old_tail, "Source tail changed")
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Finite stream, length 0, pattern 1', 'Finite stream, length 1, pattern 2', 'Finite stream, length 2, pattern 3', 'Finite stream, length 4, pattern 4', 'Finite stream, length 1, pattern 5', 'Finite stream, length 1, pattern 6', 'Finite stream, length 2, pattern 7', 'Finite stream, length 2, pattern 8', 'Finite stream, length 3, pattern 9', 'Finite stream, length 7, pattern 10', 'Finite stream, length 3, pattern 11', 'Finite stream, length 10, pattern 12', 'Finite stream, length 9, pattern 13', 'Finite stream, length 9, pattern 14', 'Finite stream, length 6, pattern 15', 'Finite stream, length 5, pattern 16', 'Finite stream, length 3, pattern 17', 'Finite stream, length 4, pattern 18', 'Infinite source 0, step 1', 'Infinite source 5, step -2', 'Infinite source -7, step 0', 'Infinite source 100, step 3', 'Demand / repeated forcing [2, 5, 9, 14]', 'Demand / repeated forcing [0, -1, -3, -6]']
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
print("D27 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
