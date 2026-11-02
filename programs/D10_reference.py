# D10 | Source Academy Python §3

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

def transpose(mat):
    rows = len(mat)
    cols = len(mat[0])
    out = [None] * cols
    for c in range(cols):
        out[c] = [0] * rows
        for r in range(rows):
            out[c][r] = mat[r][c]
    return out

def pa_case_01():
    mat = [[-10]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10]], rows)
    return pa_case_ok[0]

def pa_case_02():
    mat = [[-10, -9, -8, -7]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10], [-9], [-8], [-7]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7]], rows)
    return pa_case_ok[0]

def pa_case_03():
    mat = [[-10], [90], [190], [290]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10], [90], [190], [290]], rows)
    return pa_case_ok[0]

def pa_case_04():
    mat = [[-10, -9, -8], [90, 91, 92]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90], [-9, 91], [-8, 92]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8], [90, 91, 92]], rows)
    return pa_case_ok[0]

def pa_case_05():
    mat = [[-10, -9], [90, 91], [190, 191]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190], [-9, 91, 191]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9], [90, 91], [190, 191]], rows)
    return pa_case_ok[0]

def pa_case_06():
    mat = [[-10, -9], [90, 91]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90], [-9, 91]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9], [90, 91]], rows)
    return pa_case_ok[0]

def pa_case_07():
    mat = [[-10, -9, -8], [90, 91, 92], [190, 191, 192]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190], [-9, 91, 191], [-8, 92, 192]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8], [90, 91, 92], [190, 191, 192]], rows)
    return pa_case_ok[0]

def pa_case_08():
    mat = [[-10, -9, -8, -7, -6, -5, -4], [90, 91, 92, 93, 94, 95, 96]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90], [-9, 91], [-8, 92], [-7, 93], [-6, 94], [-5, 95], [-4, 96]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6, -5, -4], [90, 91, 92, 93, 94, 95, 96]], rows)
    return pa_case_ok[0]

def pa_case_09():
    mat = [[-10, -9], [90, 91], [190, 191], [290, 291], [390, 391], [490, 491], [590, 591]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490, 590], [-9, 91, 191, 291, 391, 491, 591]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9], [90, 91], [190, 191], [290, 291], [390, 391], [490, 491], [590, 591]], rows)
    return pa_case_ok[0]

def pa_case_10():
    mat = [[-10, -9, -8, -7, -6], [90, 91, 92, 93, 94], [190, 191, 192, 193, 194], [290, 291, 292, 293, 294]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290], [-9, 91, 191, 291], [-8, 92, 192, 292], [-7, 93, 193, 293], [-6, 94, 194, 294]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6], [90, 91, 92, 93, 94], [190, 191, 192, 193, 194], [290, 291, 292, 293, 294]], rows)
    return pa_case_ok[0]

def pa_case_11():
    mat = [[-10, -9, -8, -7], [90, 91, 92, 93], [190, 191, 192, 193], [290, 291, 292, 293], [390, 391, 392, 393]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390], [-9, 91, 191, 291, 391], [-8, 92, 192, 292, 392], [-7, 93, 193, 293, 393]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7], [90, 91, 92, 93], [190, 191, 192, 193], [290, 291, 292, 293], [390, 391, 392, 393]], rows)
    return pa_case_ok[0]

def pa_case_12():
    mat = [[-10, -9, -8], [90, 91, 92], [190, 191, 192], [290, 291, 292], [390, 391, 392], [490, 491, 492]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490], [-9, 91, 191, 291, 391, 491], [-8, 92, 192, 292, 392, 492]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8], [90, 91, 92], [190, 191, 192], [290, 291, 292], [390, 391, 392], [490, 491, 492]], rows)
    return pa_case_ok[0]

def pa_case_13():
    mat = [[-10, -9, -8, -7, -6, -5], [90, 91, 92, 93, 94, 95], [190, 191, 192, 193, 194, 195]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190], [-9, 91, 191], [-8, 92, 192], [-7, 93, 193], [-6, 94, 194], [-5, 95, 195]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6, -5], [90, 91, 92, 93, 94, 95], [190, 191, 192, 193, 194, 195]], rows)
    return pa_case_ok[0]

def pa_case_14():
    mat = [[-10, -9, -8, -7, -6, -5, -4, -3, -2]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10], [-9], [-8], [-7], [-6], [-5], [-4], [-3], [-2]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6, -5, -4, -3, -2]], rows)
    return pa_case_ok[0]

def pa_case_15():
    mat = [[-10], [90], [190], [290], [390], [490], [590], [690], [790]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490, 590, 690, 790]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10], [90], [190], [290], [390], [490], [590], [690], [790]], rows)
    return pa_case_ok[0]

def pa_case_16():
    mat = [[-10, -9, -8, -7, -6, -5, -4, -3], [90, 91, 92, 93, 94, 95, 96, 97]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90], [-9, 91], [-8, 92], [-7, 93], [-6, 94], [-5, 95], [-4, 96], [-3, 97]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6, -5, -4, -3], [90, 91, 92, 93, 94, 95, 96, 97]], rows)
    return pa_case_ok[0]

def pa_case_17():
    mat = [[-10, -9], [90, 91], [190, 191], [290, 291], [390, 391], [490, 491], [590, 591], [690, 691]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490, 590, 690], [-9, 91, 191, 291, 391, 491, 591, 691]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9], [90, 91], [190, 191], [290, 291], [390, 391], [490, 491], [590, 591], [690, 691]], rows)
    return pa_case_ok[0]

def pa_case_18():
    mat = [[-10, -9, -8, -7], [90, 91, 92, 93], [190, 191, 192, 193], [290, 291, 292, 293]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290], [-9, 91, 191, 291], [-8, 92, 192, 292], [-7, 93, 193, 293]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7], [90, 91, 92, 93], [190, 191, 192, 193], [290, 291, 292, 293]], rows)
    return pa_case_ok[0]

def pa_case_19():
    mat = [[-10, -9, -8, -7, -6], [90, 91, 92, 93, 94], [190, 191, 192, 193, 194], [290, 291, 292, 293, 294], [390, 391, 392, 393, 394]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390], [-9, 91, 191, 291, 391], [-8, 92, 192, 292, 392], [-7, 93, 193, 293, 393], [-6, 94, 194, 294, 394]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6], [90, 91, 92, 93, 94], [190, 191, 192, 193, 194], [290, 291, 292, 293, 294], [390, 391, 392, 393, 394]], rows)
    return pa_case_ok[0]

def pa_case_20():
    mat = [[-10, -9], [90, 91], [190, 191], [290, 291], [390, 391], [490, 491]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490], [-9, 91, 191, 291, 391, 491]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9], [90, 91], [190, 191], [290, 291], [390, 391], [490, 491]], rows)
    return pa_case_ok[0]

def pa_case_21():
    mat = [[-10, -9, -8, -7, -6, -5], [90, 91, 92, 93, 94, 95]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90], [-9, 91], [-8, 92], [-7, 93], [-6, 94], [-5, 95]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6, -5], [90, 91, 92, 93, 94, 95]], rows)
    return pa_case_ok[0]

def pa_case_22():
    mat = [[-10, -9, -8], [90, 91, 92], [190, 191, 192], [290, 291, 292], [390, 391, 392], [490, 491, 492], [590, 591, 592]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490, 590], [-9, 91, 191, 291, 391, 491, 591], [-8, 92, 192, 292, 392, 492, 592]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8], [90, 91, 92], [190, 191, 192], [290, 291, 292], [390, 391, 392], [490, 491, 492], [590, 591, 592]], rows)
    return pa_case_ok[0]

def pa_case_23():
    mat = [[-10, -9, -8, -7, -6, -5, -4], [90, 91, 92, 93, 94, 95, 96], [190, 191, 192, 193, 194, 195, 196]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190], [-9, 91, 191], [-8, 92, 192], [-7, 93, 193], [-6, 94, 194], [-5, 95, 195], [-4, 96, 196]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6, -5, -4], [90, 91, 92, 93, 94, 95, 96], [190, 191, 192, 193, 194, 195, 196]], rows)
    return pa_case_ok[0]

def pa_case_24():
    mat = [[-10, -9, -8, -7, -6], [90, 91, 92, 93, 94], [190, 191, 192, 193, 194], [290, 291, 292, 293, 294], [390, 391, 392, 393, 394], [490, 491, 492, 493, 494], [590, 591, 592, 593, 594], [690, 691, 692, 693, 694]]
    rows = pa_copy_rows(mat)
    result = transpose(mat)
    pa_check(result == [[-10, 90, 190, 290, 390, 490, 590, 690], [-9, 91, 191, 291, 391, 491, 591, 691], [-8, 92, 192, 292, 392, 492, 592, 692], [-7, 93, 193, 293, 393, 493, 593, 693], [-6, 94, 194, 294, 394, 494, 594, 694]], 'Unexpected result')
    pa_matrix_fresh(result, mat)
    pa_matrix_unchanged(mat, [[-10, -9, -8, -7, -6], [90, 91, 92, 93, 94], [190, 191, 192, 193, 194], [290, 291, 292, 293, 294], [390, 391, 392, 393, 394], [490, 491, 492, 493, 494], [590, 591, 592, 593, 594], [690, 691, 692, 693, 694]], rows)
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Transpose 1 by 1', 'Transpose 1 by 4', 'Transpose 4 by 1', 'Transpose 2 by 3', 'Transpose 3 by 2', 'Transpose 2 by 2', 'Transpose 3 by 3', 'Transpose 2 by 7', 'Transpose 7 by 2', 'Transpose 4 by 5', 'Transpose 5 by 4', 'Transpose 6 by 3', 'Transpose 3 by 6', 'Transpose 1 by 9', 'Transpose 9 by 1', 'Transpose 2 by 8', 'Transpose 8 by 2', 'Transpose 4 by 4', 'Transpose 5 by 5', 'Transpose 6 by 2', 'Transpose 2 by 6', 'Transpose 7 by 3', 'Transpose 3 by 7', 'Transpose 8 by 5']
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
print("D10 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
