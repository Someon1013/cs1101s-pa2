
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

def walks_exactly(maze, r, c, k):
    rows = len(maze)
    cols = len(maze[0])
    cache = [None] * (k + 1)
    for left in range(k + 1):
        cache[left] = [None] * rows
        for i in range(rows):
            cache[left][i] = [None] * cols

    def visit(r, c, left):
        if r < 0 or r >= rows or c < 0 or (c >= cols):
            return 0
        if maze[r][c] == '#':
            return 0
        if left == 0:
            return 1 if maze[r][c] == 'G' else 0
        if is_none(cache[left][r][c]):
            cache[left][r][c] = (
                visit(r - 1, c, left - 1) + visit(r + 1, c, left - 1) + visit(r, c - 1,
                left - 1) + visit(r, c + 1, left - 1)
            )
        return cache[left][r][c]
    return visit(r, c, k)

maze = [['.', 'G']]
pa_check(walks_exactly(maze, 0, 0, 3) == 1, "Revisits and early goal allowed")
pa_check(walks_exactly(maze, 0, 0, 2) == 0, "Exactly means exactly")
pa_check(walks_exactly(maze, 0, 1, 0) == 1, "Zero moves at goal")
pa_check(walks_exactly(maze, 0, 0, 0) == 0, "Zero moves away from goal")
pa_check(maze == [['.', 'G']], "Do not mark this maze")
print("D24: all supplied checks passed")
