
# Practice helpers, defined here; these are not extra built-ins.
def pa_check(condition, message):
    if not condition:
        return error(message)
    return True

def pa_values(xs, expected):
    current = xs
    for i in range(len(expected)):
        pa_check(not is_none(current), "Linked result ended early")
        pa_check(head(current) == expected[i], "Unexpected linked value")
        current = tail(current)
    return pa_check(is_none(current), "Unexpected extra linked values")

def pa_snapshot(xs):
    saved = [None] * length(xs)
    for i in range(len(saved)):
        saved[i] = [xs, head(xs), tail(xs)]
        xs = tail(xs)
    return saved

def pa_unchanged(saved):
    for i in range(len(saved)):
        node = saved[i][0]
        pa_check(head(node) == saved[i][1], "An input head changed")
        pa_check(tail(node) is saved[i][2], "An input tail changed")
    return True

def pa_prefix(s, expected):
    current = s
    for i in range(len(expected)):
        pa_check(not is_none(current), "Stream ended early")
        pa_check(head(current) == expected[i], "Unexpected stream value")
        if i + 1 < len(expected):
            current = stream_tail(current)
    return True

def shortest_one_break(maze, r, c):
    rows = len(maze)
    cols = len(maze[0])
    seen = [None] * rows
    for i in range(rows):
        seen[i] = [None] * cols
        for j in range(cols):
            seen[i][j] = [False, False]

    def visit(r, c, used):
        if r < 0 or r >= rows or c < 0 or (c >= cols):
            return math_inf
        if maze[r][c] == '#':
            if used:
                return math_inf
            used = True
        state = 1 if used else 0
        if seen[r][c][state]:
            return math_inf
        if maze[r][c] == 'G':
            return 0
        seen[r][c][state] = True
        best = (
            min(visit(r - 1, c, used), visit(r + 1, c, used), visit(r, c - 1, used),
            visit(r, c + 1, used))
        )
        seen[r][c][state] = False
        return 1 + best
    return visit(r, c, False)

pa_check(shortest_one_break([['.', '#', 'G']], 0, 0) == 2, "One break")
(
    pa_check(shortest_one_break([['.', '#', '#', 'G']], 0, 0) == math_inf,
    "Cannot break twice")
)
pa_check(shortest_one_break([['.', '.', 'G']], 0, 0) == 2, "Break optional")
pa_check(shortest_one_break([['G']], 0, 0) == 0, "Start at goal")
print("D23: all supplied checks passed")
