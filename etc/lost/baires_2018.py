def is_match(s):
    opens = '([{'
    closes = ')]}'
    last_opened = []
    for i in s:
        # print(i, last_opened)
        if i in opens:
            last_opened.append(i)
        elif i in closes:
            c_index = closes.index(i)
            if opens[c_index] not in last_opened:
                # closing something no opened
                return False
            index = last_opened.index(opens[c_index])

            if index == -1:
                # also closing something not opened
                return False
            elif last_opened[index] != last_opened[-1]:
                # closing a previous open (not the last guy)
                return False
            elif last_opened[index] == last_opened[-1]:
                # closing ok
                last_opened.pop()

    # if there is someone left here
    # it's not balanced
    return len(last_opened) == 0


print(is_match('(a[0]+b[2c[6]]) {24 + 53}'))
print(is_match('f(e(d))'))
print(is_match('[()]{}([])'))
print(not is_match('((b)'))
print(not is_match('(c]'))
print(not is_match('{(a[])'))
print(not is_match('([)]'))
print(not is_match('[({{}})'))
print(not is_match(')('))
