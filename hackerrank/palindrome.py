def isAlmostPalindrome(word):
    if len(word) == 1:
        return True
    ini = word[0:len(word) / 2]
    end = word[len(word) / 2 + len(word) % 2::][::-1]
    print(ini, end)
    if ini.startswith(end):
        return True
    elif all(ini[i] != end[i] for i in range(len(ini))):
        return True
    return False


isAlmostPalindrome('abccbx')
isAlmostPalindrome('aaaaaa')
isAlmostPalindrome('bbb')
isAlmostPalindrome('quack')
