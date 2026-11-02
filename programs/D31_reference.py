# D31 | Source Academy Python §3

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

def lower_bound(a, target):
    lo = 0
    hi = len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo

def pa_case_01():
    a = []
    pa_check(lower_bound(a, 5) == 0, 'Unexpected result')
    pa_check(a == [], "Input changed")
    return pa_case_ok[0]

def pa_case_02():
    a = [3]
    pa_check(lower_bound(a, 3) == 0, 'Unexpected result')
    pa_check(a == [3], "Input changed")
    return pa_case_ok[0]

def pa_case_03():
    a = [1, 3, 3, 7]
    pa_check(lower_bound(a, 3) == 1, 'Unexpected result')
    pa_check(a == [1, 3, 3, 7], "Input changed")
    return pa_case_ok[0]

def pa_case_04():
    a = [1, 3, 3, 7]
    pa_check(lower_bound(a, 8) == 4, 'Unexpected result')
    pa_check(a == [1, 3, 3, 7], "Input changed")
    return pa_case_ok[0]

def pa_case_05():
    a = [3]
    pa_check(lower_bound(a, 2) == 0, 'Unexpected result')
    pa_check(a == [3], "Input changed")
    return pa_case_ok[0]

def pa_case_06():
    a = [3]
    pa_check(lower_bound(a, 4) == 1, 'Unexpected result')
    pa_check(a == [3], "Input changed")
    return pa_case_ok[0]

def pa_case_07():
    a = [2, 2, 2, 2, 2, 2, 2, 2]
    pa_check(lower_bound(a, 2) == 0, 'Unexpected result')
    pa_check(a == [2, 2, 2, 2, 2, 2, 2, 2], "Input changed")
    return pa_case_ok[0]

def pa_case_08():
    a = [2, 2, 2, 2, 2, 2, 2, 2]
    pa_check(lower_bound(a, 1) == 0, 'Unexpected result')
    pa_check(a == [2, 2, 2, 2, 2, 2, 2, 2], "Input changed")
    return pa_case_ok[0]

def pa_case_09():
    a = [2, 2, 2, 2, 2, 2, 2, 2]
    pa_check(lower_bound(a, 3) == 8, 'Unexpected result')
    pa_check(a == [2, 2, 2, 2, 2, 2, 2, 2], "Input changed")
    return pa_case_ok[0]

def pa_case_10():
    a = [-9, -5, -5, 0]
    pa_check(lower_bound(a, -5) == 1, 'Unexpected result')
    pa_check(a == [-9, -5, -5, 0], "Input changed")
    return pa_case_ok[0]

def pa_case_11():
    a = [-9, -5, 0]
    pa_check(lower_bound(a, -7) == 1, 'Unexpected result')
    pa_check(a == [-9, -5, 0], "Input changed")
    return pa_case_ok[0]

def pa_case_12():
    a = [1, 2, 4, 8]
    pa_check(lower_bound(a, 3) == 2, 'Unexpected result')
    pa_check(a == [1, 2, 4, 8], "Input changed")
    return pa_case_ok[0]

def pa_case_13():
    a = [0, 0, 0]
    pa_check(lower_bound(a, -13) == 0, 'Unexpected result')
    pa_check(a == [0, 0, 0], "Input changed")
    return pa_case_ok[0]

def pa_case_14():
    a = [5, 5, 5, 5, 5, 5, 5]
    pa_check(lower_bound(a, -1) == 0, 'Unexpected result')
    pa_check(a == [5, 5, 5, 5, 5, 5, 5], "Input changed")
    return pa_case_ok[0]

def pa_case_15():
    a = [-3, -2, -1]
    pa_check(lower_bound(a, 0) == 3, 'Unexpected result')
    pa_check(a == [-3, -2, -1], "Input changed")
    return pa_case_ok[0]

def pa_case_16():
    a = [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1]
    pa_check(lower_bound(a, 3) == 10, 'Unexpected result')
    pa_check(a == [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1], "Input changed")
    return pa_case_ok[0]

def pa_case_17():
    a = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    pa_check(lower_bound(a, 7) == 7, 'Unexpected result')
    pa_check(a == [0, 1, 2, 3, 4, 5, 6, 7, 8], "Input changed")
    return pa_case_ok[0]

def pa_case_18():
    a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pa_check(lower_bound(a, 20) == 9, 'Unexpected result')
    pa_check(a == [1, 2, 3, 4, 5, 6, 7, 8, 9], "Input changed")
    return pa_case_ok[0]

def pa_case_19():
    a = [1, 3, 3, 3, 3, 3]
    pa_check(lower_bound(a, -13) == 0, 'Unexpected result')
    pa_check(a == [1, 3, 3, 3, 3, 3], "Input changed")
    return pa_case_ok[0]

def pa_case_20():
    a = [-2, 0, 0, 0, 7]
    pa_check(lower_bound(a, -1) == 1, 'Unexpected result')
    pa_check(a == [-2, 0, 0, 0, 7], "Input changed")
    return pa_case_ok[0]

def pa_case_21():
    a = [-1000000, 1, 1000000]
    pa_check(lower_bound(a, 0) == 1, 'Unexpected result')
    pa_check(a == [-1000000, 1, 1000000], "Input changed")
    return pa_case_ok[0]

def pa_case_22():
    a = [-6, -4, -1, 2]
    pa_check(lower_bound(a, 3) == 4, 'Unexpected result')
    pa_check(a == [-6, -4, -1, 2], "Input changed")
    return pa_case_ok[0]

def pa_case_23():
    a = [-5, 7, 11, 11, 11]
    pa_check(lower_bound(a, 7) == 1, 'Unexpected result')
    pa_check(a == [-5, 7, 11, 11, 11], "Input changed")
    return pa_case_ok[0]

def pa_case_24():
    a = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324, 326, 328, 330, 332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 352, 354, 356, 358, 360, 362, 364, 366, 368, 370, 372, 374, 376, 378, 380, 382, 384, 386, 388, 390, 392, 394, 396, 398, 400, 402, 404, 406, 408, 410, 412, 414, 416, 418, 420, 422, 424, 426, 428, 430, 432, 434, 436, 438, 440, 442, 444, 446, 448, 450, 452, 454, 456, 458, 460, 462, 464, 466, 468, 470, 472, 474, 476, 478, 480, 482, 484, 486, 488, 490, 492, 494, 496, 498, 500, 502, 504, 506, 508, 510]
    pa_check(lower_bound(a, 255) == 128, 'Unexpected result')
    pa_check(a == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200, 202, 204, 206, 208, 210, 212, 214, 216, 218, 220, 222, 224, 226, 228, 230, 232, 234, 236, 238, 240, 242, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 264, 266, 268, 270, 272, 274, 276, 278, 280, 282, 284, 286, 288, 290, 292, 294, 296, 298, 300, 302, 304, 306, 308, 310, 312, 314, 316, 318, 320, 322, 324, 326, 328, 330, 332, 334, 336, 338, 340, 342, 344, 346, 348, 350, 352, 354, 356, 358, 360, 362, 364, 366, 368, 370, 372, 374, 376, 378, 380, 382, 384, 386, 388, 390, 392, 394, 396, 398, 400, 402, 404, 406, 408, 410, 412, 414, 416, 418, 420, 422, 424, 426, 428, 430, 432, 434, 436, 438, 440, 442, 444, 446, 448, 450, 452, 454, 456, 458, 460, 462, 464, 466, 468, 470, 472, 474, 476, 478, 480, 482, 484, 486, 488, 490, 492, 494, 496, 498, 500, 502, 504, 506, 508, 510], "Input changed")
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Boundary for 5, size 0', 'Boundary for 3, size 1', 'Boundary for 3, size 4', 'Boundary for 8, size 4', 'Boundary for 2, size 1', 'Boundary for 4, size 1', 'Boundary for 2, size 8', 'Boundary for 1, size 8', 'Boundary for 3, size 8', 'Boundary for -5, size 4', 'Boundary for -7, size 3', 'Boundary for 3, size 4', 'Boundary for -13, size 3', 'Boundary for -1, size 7', 'Boundary for 0, size 3', 'Boundary for 3, size 10', 'Boundary for 7, size 9', 'Boundary for 20, size 9', 'Boundary for -13, size 6', 'Boundary for -1, size 5', 'Boundary for 0, size 3', 'Boundary for 3, size 4', 'Boundary for 7, size 5', 'Boundary for 255, size 256']
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
print("D31 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
