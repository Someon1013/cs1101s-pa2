# D30 | Source Academy Python §3
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

def smooth_numbers():

    def scale(s, factor):
        return pair(head(s) * factor, memo_fun(lambda: scale(stream_tail(s), factor)))

    def merge(s, t):
        a = head(s)
        b = head(t)
        if a < b:
            return pair(a, memo_fun(lambda: merge(stream_tail(s), t)))
        if b < a:
            return pair(b, memo_fun(lambda: merge(s, stream_tail(t))))
        return pair(a, memo_fun(lambda: merge(stream_tail(s), stream_tail(t))))
    s = pair(1, memo_fun(lambda: merge(scale(s, 2), merge(scale(s, 3), scale(s, 5)))))
    return s

def pa_case_01():
    s = smooth_numbers()
    for i in range(0):
        s = stream_tail(s)
    pa_prefix(s, [1], False, True)
    return pa_case_ok[0]

def pa_case_02():
    s = smooth_numbers()
    for i in range(0):
        s = stream_tail(s)
    pa_prefix(s, [1, 2, 3, 4, 5, 6, 8, 9, 10, 12], False, True)
    return pa_case_ok[0]

def pa_case_03():
    s = smooth_numbers()
    for i in range(0):
        s = stream_tail(s)
    pa_prefix(s, [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36], False, True)
    return pa_case_ok[0]

def pa_case_04():
    s = smooth_numbers()
    for i in range(0):
        s = stream_tail(s)
    pa_prefix(s, [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80], False, True)
    return pa_case_ok[0]

def pa_case_05():
    s = smooth_numbers()
    for i in range(30):
        s = stream_tail(s)
    pa_prefix(s, [81, 90, 96, 100, 108, 120, 125, 128, 135, 144], False, True)
    return pa_case_ok[0]

def pa_case_06():
    s = smooth_numbers()
    for i in range(40):
        s = stream_tail(s)
    pa_prefix(s, [150, 160, 162, 180, 192, 200, 216, 225, 240, 243], False, True)
    return pa_case_ok[0]

def pa_case_07():
    s = smooth_numbers()
    for i in range(60):
        s = stream_tail(s)
    pa_prefix(s, [400, 405, 432, 450, 480, 486, 500, 512, 540, 576], False, True)
    return pa_case_ok[0]

def pa_case_08():
    s = smooth_numbers()
    for i in range(90):
        s = stream_tail(s)
    pa_prefix(s, [1200, 1215, 1250, 1280, 1296, 1350, 1440, 1458, 1500, 1536], False, True)
    return pa_case_ok[0]

def pa_case_09():
    s = smooth_numbers()
    for i in range(120):
        s = stream_tail(s)
    pa_prefix(s, [2880, 2916, 3000, 3072, 3125, 3200, 3240, 3375, 3456, 3600], False, True)
    return pa_case_ok[0]

def pa_case_10():
    s = smooth_numbers()
    for i in range(150):
        s = stream_tail(s)
    pa_prefix(s, [6000, 6075, 6144, 6250, 6400, 6480, 6561, 6750, 6912, 7200], False, True)
    return pa_case_ok[0]

def pa_case_11():
    s = smooth_numbers()
    for i in range(200):
        s = stream_tail(s)
    pa_prefix(s, [16384, 16875, 17280, 17496, 18000, 18225, 18432, 18750, 19200, 19440], False, True)
    return pa_case_ok[0]

def pa_case_12():
    s = smooth_numbers()
    for i in range(250):
        s = stream_tail(s)
    pa_prefix(s, [39366, 40000, 40500, 40960, 41472, 43200, 43740, 45000, 46080, 46656], False, True)
    return pa_case_ok[0]

def pa_case_13():
    s = smooth_numbers()
    for i in range(300):
        s = stream_tail(s)
    pa_prefix(s, [84375, 86400, 87480, 90000, 91125, 92160, 93312, 93750, 96000, 97200], False, True)
    return pa_case_ok[0]

def pa_case_14():
    s = smooth_numbers()
    for i in range(400):
        s = stream_tail(s)
    pa_prefix(s, [312500, 314928, 320000, 324000, 327680, 328050, 331776, 337500, 345600, 349920], False, True)
    return pa_case_ok[0]

def pa_case_15():
    s = smooth_numbers()
    for i in range(500):
        s = stream_tail(s)
    pa_prefix(s, [944784, 960000, 972000, 983040, 984150, 995328, 1000000, 1012500, 1024000, 1036800], False, True)
    return pa_case_ok[0]

def pa_case_16():
    s = smooth_numbers()
    for i in range(600):
        s = stream_tail(s)
    pa_prefix(s, [2488320, 2500000, 2519424, 2531250, 2560000, 2592000, 2621440, 2624400, 2654208, 2657205], False, True)
    return pa_case_ok[0]

def pa_case_17():
    s = smooth_numbers()
    for i in range(700):
        s = stream_tail(s)
    pa_prefix(s, [5904900, 5971968, 6000000, 6075000, 6144000, 6220800, 6250000, 6291456, 6298560, 6328125], False, True)
    return pa_case_ok[0]

def pa_case_18():
    s = smooth_numbers()
    for i in range(800):
        s = stream_tail(s)
    pa_prefix(s, [12800000, 12960000, 13107200, 13122000, 13271040, 13286025, 13436928, 13500000, 13668750, 13824000], False, True)
    return pa_case_ok[0]

def pa_case_19():
    s = smooth_numbers()
    for i in range(900):
        s = stream_tail(s)
    pa_prefix(s, [26542080, 26572050, 26873856, 27000000, 27337500, 27648000, 27993600, 28125000, 28311552, 28343520], False, True)
    return pa_case_ok[0]

def pa_case_20():
    s = smooth_numbers()
    for i in range(990):
        s = stream_tail(s)
    pa_prefix(s, [48828125, 49152000, 49207500, 49766400, 50000000, 50331648, 50388480, 50625000, 51018336, 51200000], False, True)
    return pa_case_ok[0]

def pa_case_21():
    s = smooth_numbers()
    for i in range(1):
        s = stream_tail(s)
    first = stream_tail(s)
    second = stream_tail(s)
    pa_check(first is second, "Tail not shared")
    pa_prefix(first, [3, 4, 5, 6, 8], False, True)
    return pa_case_ok[0]

def pa_case_22():
    s = smooth_numbers()
    for i in range(25):
        s = stream_tail(s)
    first = stream_tail(s)
    second = stream_tail(s)
    pa_check(first is second, "Tail not shared")
    pa_prefix(first, [64, 72, 75, 80, 81], False, True)
    return pa_case_ok[0]

def pa_case_23():
    s = smooth_numbers()
    for i in range(100):
        s = stream_tail(s)
    first = stream_tail(s)
    second = stream_tail(s)
    pa_check(first is second, "Tail not shared")
    pa_prefix(first, [1620, 1728, 1800, 1875, 1920], False, True)
    return pa_case_ok[0]

def pa_case_24():
    a = smooth_numbers()
    b = smooth_numbers()
    pa_prefix(a, [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 81, 90, 96, 100, 108, 120, 125, 128, 135, 144], False, True)
    pa_prefix(b, [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24, 25, 27, 30, 32, 36, 40, 45, 48, 50, 54, 60, 64, 72, 75, 80, 81, 90, 96, 100, 108, 120, 125, 128, 135, 144], False, True)
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Smooth positions 1–1', 'Smooth positions 1–10', 'Smooth positions 1–20', 'Smooth positions 1–30', 'Smooth positions 31–40', 'Smooth positions 41–50', 'Smooth positions 61–70', 'Smooth positions 91–100', 'Smooth positions 121–130', 'Smooth positions 151–160', 'Smooth positions 201–210', 'Smooth positions 251–260', 'Smooth positions 301–310', 'Smooth positions 401–410', 'Smooth positions 501–510', 'Smooth positions 601–610', 'Smooth positions 701–710', 'Smooth positions 801–810', 'Smooth positions 901–910', 'Smooth positions 991–1000', 'Replay shared tail at depth 1', 'Replay shared tail at depth 25', 'Replay shared tail at depth 100', 'Independent stream construction']
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
print("D30 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
