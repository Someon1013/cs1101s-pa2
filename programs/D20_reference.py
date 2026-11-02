
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

def count_simple_paths(maze, r, c):
    if r < 0 or r >= len(maze) or c < 0 or (c >= len(maze[0])):
        return 0
    if maze[r][c] == '#':
        return 0
    if maze[r][c] == 'G':
        return 1
    old = maze[r][c]
    maze[r][c] = '#'
    result = (
        count_simple_paths(maze, r - 1, c) + count_simple_paths(maze, r + 1, c) +
        count_simple_paths(maze, r, c - 1) + count_simple_paths(maze, r, c + 1)
    )
    maze[r][c] = old
    return result

maze = [['.', '.'], ['.', 'G']]
pa_check(count_simple_paths(maze, 0, 0) == 2, "Two simple paths")
pa_check(maze == [['.', '.'], ['.', 'G']], "Restore maze")
pa_check(count_simple_paths([['G']], 0, 0) == 1, "One zero-move path")
pa_check(count_simple_paths([['.', '#', 'G']], 0, 0) == 0, "No paths")
print("D20: all supplied checks passed")
