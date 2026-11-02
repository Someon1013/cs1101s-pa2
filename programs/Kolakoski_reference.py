# Source Academy Python section 3 - worked reference (spoiler)
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

def kolakoski():
    def runs(lengths, symbol):
        return emit(symbol, head(lengths), lengths)
    def emit(symbol, left, lengths):
        def later():
            if left > 1:
                return emit(symbol, left - 1, lengths)
            return runs(stream_tail(lengths), 3 - symbol)
        return pair(symbol, memo_fun(later))
    def after_seed():
        return runs(stream_tail(stream_tail(sequence)), 1)
    sequence = pair(1, memo_fun(lambda: pair(2, memo_fun(
        lambda: pair(2, memo_fun(after_seed))))))
    return sequence

def check(condition, message):
    if not condition:
        return error(message)
    return True

sequence = kolakoski()
values = [0] * 1000
current = sequence
for i in range(1000):
    values[i] = head(current)
    check(values[i] == 1 or values[i] == 2, 'Alphabet')
    if i < 999:
        current = stream_tail(current)
expected = [1,2,2,1,1,2,1,2,2,1,2,2,1,1,2,1,1,2,2,1]
for i in range(len(expected)):
    check(values[i] == expected[i], '20-value prefix')
start = 0
run = 0
while start < 1000:
    end = start + 1
    while end < 1000 and values[end] == values[start]:
        end = end + 1
    if end < 1000:
        check(end - start == values[run], 'Completed run length')
    start = end
    run = run + 1
check(stream_tail(sequence) is stream_tail(sequence), 'Memoized identity')
other = kolakoski()
check(other is not sequence, 'Independent construction')
for i in range(len(expected)):
    check(head(other) == expected[i], 'Independent prefix')
    if i + 1 < len(expected):
        other = stream_tail(other)
print('Kolakoski: 1000-element and structural checks passed')
