# D19 | Source Academy Python §3

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

def reachable(maze, r, c):
    if r < 0 or r >= len(maze) or c < 0 or (c >= len(maze[0])):
        return False
    if maze[r][c] == '#':
        return False
    if maze[r][c] == 'G':
        return True
    old = maze[r][c]
    maze[r][c] = '#'
    result = (
        reachable(maze, r - 1, c) or reachable(maze, r + 1, c) or reachable(maze, r, c -
        1) or reachable(maze, r, c + 1)
    )
    maze[r][c] = old
    return result

def pa_case_01():
    maze = [['G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['G']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['G']], rows)
    return pa_case_ok[0]

def pa_case_02():
    maze = [['.', 'G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G']], rows)
    return pa_case_ok[0]

def pa_case_03():
    maze = [['.', '#', 'G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == False, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '#', 'G']], rows)
    pa_check(reachable(maze, 0, 0) == False, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '#', 'G']], rows)
    return pa_case_ok[0]

def pa_case_04():
    maze = [['.', '.'], ['.', 'G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '.'], ['.', 'G']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '.'], ['.', 'G']], rows)
    return pa_case_ok[0]

def pa_case_05():
    maze = [['G', '.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 2) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['G', '.', '.']], rows)
    pa_check(reachable(maze, 0, 2) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['G', '.', '.']], rows)
    return pa_case_ok[0]

def pa_case_06():
    maze = [['.'], ['.'], ['G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.'], ['.'], ['G']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.'], ['.'], ['G']], rows)
    return pa_case_ok[0]

def pa_case_07():
    maze = [['.', '#', 'G'], ['.', '.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '#', 'G'], ['.', '.', '.']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '#', 'G'], ['.', '.', '.']], rows)
    return pa_case_ok[0]

def pa_case_08():
    maze = [['.', '.', '.'], ['.', '#', '.'], ['.', '.', 'G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '.', '.'], ['.', '#', '.'], ['.', '.', 'G']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '.', '.'], ['.', '#', '.'], ['.', '.', 'G']], rows)
    return pa_case_ok[0]

def pa_case_09():
    maze = [['.', '#', '#'], ['.', '.', 'G']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '#', '#'], ['.', '.', 'G']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '#', '#'], ['.', '.', 'G']], rows)
    return pa_case_ok[0]

def pa_case_10():
    maze = [['.', 'G'], ['.', '.'], ['#', '#']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G'], ['.', '.'], ['#', '#']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G'], ['.', '.'], ['#', '#']], rows)
    return pa_case_ok[0]

def pa_case_11():
    maze = [['.', 'G', '.'], ['#', '#', '.'], ['.', '.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G', '.'], ['#', '#', '.'], ['.', '.', '.']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G', '.'], ['#', '#', '.'], ['.', '.', '.']], rows)
    return pa_case_ok[0]

def pa_case_12():
    maze = [['.', '.', '.', 'G', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 2) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '.', '.', 'G', '.']], rows)
    pa_check(reachable(maze, 0, 2) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '.', '.', 'G', '.']], rows)
    return pa_case_ok[0]

def pa_case_13():
    maze = [['G', '.', '.'], ['.', '#', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 1) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['G', '.', '.'], ['.', '#', '.']], rows)
    pa_check(reachable(maze, 0, 1) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['G', '.', '.'], ['.', '#', '.']], rows)
    return pa_case_ok[0]

def pa_case_14():
    maze = [['.', '#'], ['#', 'G'], ['#', '#']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 1, 1) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '#'], ['#', 'G'], ['#', '#']], rows)
    pa_check(reachable(maze, 1, 1) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '#'], ['#', 'G'], ['#', '#']], rows)
    return pa_case_ok[0]

def pa_case_15():
    maze = [['G', '.', '.'], ['#', '.', '#'], ['.', '.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 2) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['G', '.', '.'], ['#', '.', '#'], ['.', '.', '.']], rows)
    pa_check(reachable(maze, 0, 2) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['G', '.', '.'], ['#', '.', '#'], ['.', '.', '.']], rows)
    return pa_case_ok[0]

def pa_case_16():
    maze = [['.', 'G', '.', '.', '#']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 2) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G', '.', '.', '#']], rows)
    pa_check(reachable(maze, 0, 2) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G', '.', '.', '#']], rows)
    return pa_case_ok[0]

def pa_case_17():
    maze = [['.', '.', '.'], ['G', '.', '#']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 2) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '.', '.'], ['G', '.', '#']], rows)
    pa_check(reachable(maze, 0, 2) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '.', '.'], ['G', '.', '#']], rows)
    return pa_case_ok[0]

def pa_case_18():
    maze = [['#', 'G'], ['.', '.'], ['.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 2, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['#', 'G'], ['.', '.'], ['.', '.']], rows)
    pa_check(reachable(maze, 2, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['#', 'G'], ['.', '.'], ['.', '.']], rows)
    return pa_case_ok[0]

def pa_case_19():
    maze = [['.', '.', '.'], ['G', '.', '.'], ['.', '.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 1, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '.', '.'], ['G', '.', '.'], ['.', '.', '.']], rows)
    pa_check(reachable(maze, 1, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '.', '.'], ['G', '.', '.'], ['.', '.', '.']], rows)
    return pa_case_ok[0]

def pa_case_20():
    maze = [['.', '#', '.', 'G', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 3) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '#', '.', 'G', '.']], rows)
    pa_check(reachable(maze, 0, 3) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '#', '.', 'G', '.']], rows)
    return pa_case_ok[0]

def pa_case_21():
    maze = [['.', 'G', '.'], ['#', '#', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G', '.'], ['#', '#', '.']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G', '.'], ['#', '#', '.']], rows)
    return pa_case_ok[0]

def pa_case_22():
    maze = [['.', '.'], ['G', '.'], ['#', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', '.'], ['G', '.'], ['#', '.']], rows)
    pa_check(reachable(maze, 0, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', '.'], ['G', '.'], ['#', '.']], rows)
    return pa_case_ok[0]

def pa_case_23():
    maze = [['.', 'G', '.'], ['.', '#', '.'], ['.', '.', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 1, 0) == True, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G', '.'], ['.', '#', '.'], ['.', '.', '.']], rows)
    pa_check(reachable(maze, 1, 0) == True, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G', '.'], ['.', '#', '.'], ['.', '.', '.']], rows)
    return pa_case_ok[0]

def pa_case_24():
    maze = [['.', 'G', '.', '#', '.']]
    rows = pa_copy_rows(maze)
    pa_check(reachable(maze, 0, 4) == False, 'Unexpected result')
    pa_matrix_unchanged(maze, [['.', 'G', '.', '#', '.']], rows)
    pa_check(reachable(maze, 0, 4) == False, 'Repeated call differs')
    pa_matrix_unchanged(maze, [['.', 'G', '.', '#', '.']], rows)
    return pa_case_ok[0]

pa_cases = [pa_case_01, pa_case_02, pa_case_03, pa_case_04, pa_case_05, pa_case_06, pa_case_07, pa_case_08, pa_case_09, pa_case_10, pa_case_11, pa_case_12, pa_case_13, pa_case_14, pa_case_15, pa_case_16, pa_case_17, pa_case_18, pa_case_19, pa_case_20, pa_case_21, pa_case_22, pa_case_23, pa_case_24]
pa_titles = ['Reachability layout 1', 'Reachability layout 2', 'Reachability layout 3', 'Reachability layout 4', 'Reachability layout 5', 'Reachability layout 6', 'Reachability layout 7', 'Reachability layout 8', 'Reachability layout 9', 'Reachability layout 10', 'Reachability layout 11', 'Reachability layout 12', 'Reachability layout 13', 'Reachability layout 14', 'Reachability layout 15', 'Reachability layout 16', 'Reachability layout 17', 'Reachability layout 18', 'Reachability layout 19', 'Reachability layout 20', 'Reachability layout 21', 'Reachability layout 22', 'Reachability layout 23', 'Reachability layout 24']
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
print("D19 passed", pa_passed, "out of", len(pa_cases), "cases")
print("Public cases passed", pa_public_passed, "out of", min(4, len(pa_cases)))
if len(pa_cases) > 4:
    print("Additional cases passed", pa_extra_passed, "out of", len(pa_cases) - 4)
