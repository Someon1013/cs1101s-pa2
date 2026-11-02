# D36 | Source Academy Python §3
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

def route_cost_stream(mat, start, deltas):

    def build(source, current, total):
        if is_none(source):
            return None
        dest = current + head(source)
        updated = total + mat[current][dest]
        return (
            pair(updated, memo_fun(lambda: build(stream_tail(source), dest, updated)))
        )
    return build(deltas, start, 0)

def pa_case_01():
    mat = [[0]]
    rows = pa_copy_rows(mat)
    source = pa_stream([])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [], True, True)
    pa_matrix_unchanged(mat, [[0]], rows)
    return pa_case_ok[0]

def pa_case_02():
    mat = [[1, 8], [4, 1]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-1])
    s = route_cost_stream(mat, 1, source)
    pa_prefix(s, [4], True, True)
    pa_matrix_unchanged(mat, [[1, 8], [4, 1]], rows)
    return pa_case_ok[0]

def pa_case_03():
    mat = [[2, 9, 16], [5, 2, 2], [8, 15, 2]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-1, 0, 0, 0])
    s = route_cost_stream(mat, 2, source)
    pa_prefix(s, [15, 17, 19, 21], True, True)
    pa_matrix_unchanged(mat, [[2, 9, 16], [5, 2, 2], [8, 15, 2]], rows)
    return pa_case_ok[0]

def pa_case_04():
    mat = [[3, 10, 0, 7], [6, 3, 3, 10], [9, 16, 3, 13], [12, 2, 9, 3]]
    rows = pa_copy_rows(mat)
    source = pa_stream([0, -1, -2, 0, 1, 0, 0])
    s = route_cost_stream(mat, 3, source)
    pa_prefix(s, [3, 12, 21, 24, 34, 37, 40], True, True)
    pa_matrix_unchanged(mat, [[3, 10, 0, 7], [6, 3, 3, 10], [9, 16, 3, 13], [12, 2, 9, 3]], rows)
    return pa_case_ok[0]

def pa_case_05():
    mat = [[0, 11, 1, 8, 15], [7, 0, 4, 11, 1], [10, 0, 0, 14, 4], [13, 3, 10, 0, 7], [16, 6, 13, 3, 0]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-4, 3, 1, -2, 2, -1, -3, 3, 1, 0, -1, -2, 2, -1, 1])
    s = route_cost_stream(mat, 4, source)
    pa_prefix(s, [16, 24, 31, 44, 48, 51, 64, 72, 79, 79, 82, 85, 96, 106, 120], True, True)
    pa_matrix_unchanged(mat, [[0, 11, 1, 8, 15], [7, 0, 4, 11, 1], [10, 0, 0, 14, 4], [13, 3, 10, 0, 7], [16, 6, 13, 3, 0]], rows)
    return pa_case_ok[0]

def pa_case_06():
    mat = [[1]]
    rows = pa_copy_rows(mat)
    source = pa_stream([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], True, True)
    pa_matrix_unchanged(mat, [[1]], rows)
    return pa_case_ok[0]

def pa_case_07():
    mat = [[2, 13], [9, 2]]
    rows = pa_copy_rows(mat)
    source = pa_stream([])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [], True, True)
    pa_matrix_unchanged(mat, [[2, 13], [9, 2]], rows)
    return pa_case_ok[0]

def pa_case_08():
    mat = [[3, 14, 4], [10, 3, 7], [13, 3, 3]]
    rows = pa_copy_rows(mat)
    source = pa_stream([1])
    s = route_cost_stream(mat, 1, source)
    pa_prefix(s, [7], True, True)
    pa_matrix_unchanged(mat, [[3, 14, 4], [10, 3, 7], [13, 3, 3]], rows)
    return pa_case_ok[0]

def pa_case_09():
    mat = [[0, 15, 5, 12], [11, 0, 8, 15], [14, 4, 0, 1], [0, 7, 14, 0]]
    rows = pa_copy_rows(mat)
    source = pa_stream([3, -3, 3, -1])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [12, 12, 24, 38], True, True)
    pa_matrix_unchanged(mat, [[0, 15, 5, 12], [11, 0, 8, 15], [14, 4, 0, 1], [0, 7, 14, 0]], rows)
    return pa_case_ok[0]

def pa_case_10():
    mat = [[1, 16, 6, 13, 3], [12, 1, 9, 16, 6], [15, 5, 1, 2, 9], [1, 8, 15, 1, 12], [4, 11, 1, 8, 1]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-3, 2, -2, 3, -1, -2, 2])
    s = route_cost_stream(mat, 4, source)
    pa_prefix(s, [11, 27, 35, 41, 49, 57, 73], True, True)
    pa_matrix_unchanged(mat, [[1, 16, 6, 13, 3], [12, 1, 9, 16, 6], [15, 5, 1, 2, 9], [1, 8, 15, 1, 12], [4, 11, 1, 8, 1]], rows)
    return pa_case_ok[0]

def pa_case_11():
    mat = [[2]]
    rows = pa_copy_rows(mat)
    source = pa_stream([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30], True, True)
    pa_matrix_unchanged(mat, [[2]], rows)
    return pa_case_ok[0]

def pa_case_12():
    mat = [[3, 1], [14, 3]]
    rows = pa_copy_rows(mat)
    source = pa_stream([0, 0, 0, -1, 1, 0, 0, -1, 1, 0, -1, 1, 0, -1, 0, 1, -1, 0, 1, 0, -1, 0, 0, 1, 0, -1, 1, -1, 0, 0])
    s = route_cost_stream(mat, 1, source)
    pa_prefix(s, [3, 6, 9, 23, 24, 27, 30, 44, 45, 48, 62, 63, 66, 80, 83, 84, 98, 101, 102, 105, 119, 122, 125, 126, 129, 143, 144, 158, 161, 164], True, True)
    pa_matrix_unchanged(mat, [[3, 1], [14, 3]], rows)
    return pa_case_ok[0]

def pa_case_13():
    mat = [[0, 2, 9], [15, 0, 12], [1, 8, 0]]
    rows = pa_copy_rows(mat)
    source = pa_stream([])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [], True, True)
    pa_matrix_unchanged(mat, [[0, 2, 9], [15, 0, 12], [1, 8, 0]], rows)
    return pa_case_ok[0]

def pa_case_14():
    mat = [[1, 3, 10, 0], [16, 1, 13, 3], [2, 9, 1, 6], [5, 12, 2, 1]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-1])
    s = route_cost_stream(mat, 1, source)
    pa_prefix(s, [16], True, True)
    pa_matrix_unchanged(mat, [[1, 3, 10, 0], [16, 1, 13, 3], [2, 9, 1, 6], [5, 12, 2, 1]], rows)
    return pa_case_ok[0]

def pa_case_15():
    mat = [[2, 4, 11, 1, 8], [0, 2, 14, 4, 11], [3, 10, 2, 7, 14], [6, 13, 3, 2, 0], [9, 16, 6, 13, 2]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-2, 0, -2, 2])
    s = route_cost_stream(mat, 4, source)
    pa_prefix(s, [6, 8, 11, 22], True, True)
    pa_matrix_unchanged(mat, [[2, 4, 11, 1, 8], [0, 2, 14, 4, 11], [3, 10, 2, 7, 14], [6, 13, 3, 2, 0], [9, 16, 6, 13, 2]], rows)
    return pa_case_ok[0]

def pa_case_16():
    mat = [[3]]
    rows = pa_copy_rows(mat)
    source = pa_stream([0, 0, 0, 0, 0, 0, 0])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [3, 6, 9, 12, 15, 18, 21], True, True)
    pa_matrix_unchanged(mat, [[3]], rows)
    return pa_case_ok[0]

def pa_case_17():
    mat = [[0, 6], [2, 0]]
    rows = pa_copy_rows(mat)
    source = pa_stream([1, -1, 1, -1, 0, 1, 0, -1, 0, 0, 0, 0, 1, 0, -1])
    s = route_cost_stream(mat, 0, source)
    pa_prefix(s, [6, 8, 14, 16, 16, 22, 22, 24, 24, 24, 24, 24, 30, 30, 32], True, True)
    pa_matrix_unchanged(mat, [[0, 6], [2, 0]], rows)
    return pa_case_ok[0]

def pa_case_18():
    mat = [[1, 7, 14], [3, 1, 0], [6, 13, 1]]
    rows = pa_copy_rows(mat)
    source = pa_stream([-1, 0, 0, -1, 0, 1, -1, 0, 1, 0, 0, 0, 1, -1, 0, 0, -1, 1, -1, 0, 0, 1, 1, 0, -1, 0, 1, -2, 0, 0])
    s = route_cost_stream(mat, 2, source)
    pa_prefix(s, [13, 14, 15, 18, 19, 26, 29, 30, 37, 38, 39, 40, 40, 53, 54, 55, 58, 65, 68, 69, 70, 77, 77, 78, 91, 92, 92, 98, 99, 100], True, True)
    pa_matrix_unchanged(mat, [[1, 7, 14], [3, 1, 0], [6, 13, 1]], rows)
    return pa_case_ok[0]

def pa_case_19():
    def moves(d):
        return pair(d, lambda: moves(-d))
    s = route_cost_stream([[0, 1], [3, 0]], 0, moves(1))
    pa_prefix(s, [1, 4, 5, 8, 9, 12, 13, 16, 17, 20, 21, 24, 25, 28, 29, 32, 33, 36, 37, 40, 41, 44, 45, 48, 49, 52, 53, 56, 57, 60, 61, 64, 65, 68, 69, 72, 73, 76, 77, 80, 81, 84, 85, 88, 89, 92, 93, 96, 97, 100], False, True)
    return pa_case_ok[0]

def pa_case_20():
    def moves(d):
        return pair(d, lambda: moves(-d))
    s = route_cost_stream([[0, 3], [5, 0]], 0, moves(1))
    pa_prefix(s, [3, 8, 11, 16, 19, 24, 27, 32, 35, 40, 43, 48, 51, 56, 59, 64, 67, 72, 75, 80, 83, 88, 91, 96, 99, 104, 107, 112, 115, 120, 123, 128, 131, 136, 139, 144, 147, 152, 155, 160, 163, 168, 171, 176, 179, 184, 187, 192, 195, 200], False, True)
    return pa_case_ok[0]

def pa_case_21():
    def moves(d):
        return pair(d, lambda: moves(-d))
    s = route_cost_stream([[0, 7], [9, 0]], 0, moves(1))
    pa_prefix(s, [7, 16, 23, 32, 39, 48, 55, 64, 71, 80, 87, 96, 103, 112, 119, 128, 135, 144, 151, 160, 167, 176, 183, 192, 199, 208, 215, 224, 231, 240, 247, 256, 263, 272, 279, 288, 295, 304, 311, 320, 327, 336, 343, 352, 359, 368, 375, 384, 391, 400], False, True)
    return pa_case_ok[0]

def pa_case_22():
    def moves(d):
        return pair(d, lambda: moves(-d))
    s = route_cost_stream([[0, 11], [13, 0]], 0, moves(1))
    pa_prefix(s, [11, 24, 35, 48, 59, 72, 83, 96, 107, 120, 131, 144, 155, 168, 179, 192, 203, 216, 227, 240, 251, 264, 275, 288, 299, 312, 323, 336, 347, 360, 371, 384, 395, 408, 419, 432, 443, 456, 467, 480, 491, 504, 515, 528, 539, 552, 563, 576, 587, 600], False, True)
    return pa_case_ok[0]

def pa_case_23():
    forced = [0]
    source = pa_counted_stream([1, -1, 1], forced)
    old = tail(source)
    s = route_cost_stream([[0, 5], [2, 0]], 0, source)
    pa_check(forced[0] == 0, "Construction forced future moves")
    second = stream_tail(s)
    pa_check(forced[0] == 1, "Second result consumed extra moves")
    pa_check(stream_tail(s) is second, "Route tail not memoized")
    pa_check(forced[0] == 1, "Source work repeated")
    pa_check(tail(source) is old, "Source changed")
    return pa_case_ok[0]

def pa_case_24():
    forced = [0]
    source = pa_counted_stream([0, 1, -1], forced)
    old = tail(source)
    s = route_cost_stream([[0, 5], [2, 0]], 0, source)
    pa_check(forced[0] == 0, "Construction forced future moves")
    second = stream_tail(s)
    pa_check(forced[0] == 1, "Second result consumed extra moves")
    pa_check(stream_tail(s) is second, "Route tail not memoized")
    pa_check(forced[0] == 1, "Source work repeated")
    pa_check(tail(source) is old, "Source changed")
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Finite route 1, moves 0', 'Finite route 2, moves 1', 'Finite route 3, moves 4', 'Finite route 4, moves 7', 'Finite route 5, moves 15', 'Finite route 6, moves 30', 'Finite route 7, moves 0', 'Finite route 8, moves 1', 'Finite route 9, moves 4', 'Finite route 10, moves 7', 'Finite route 11, moves 15', 'Finite route 12, moves 30', 'Finite route 13, moves 0', 'Finite route 14, moves 1', 'Finite route 15, moves 4', 'Finite route 16, moves 7', 'Finite route 17, moves 15', 'Finite route 18, moves 30', 'Infinite alternating route, outward cost 1', 'Infinite alternating route, outward cost 3', 'Infinite alternating route, outward cost 7', 'Infinite alternating route, outward cost 11', 'Route laziness [1, -1, 1]', 'Route laziness [0, 1, -1]']
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
print("D36 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
