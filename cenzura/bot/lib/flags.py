flags = {
    "pracownik discorda": 1 << 0,
    "właściciel partnerskiego serwera": 1 << 1,
    "wydarzenia hypesquadu": 1 << 2,
    "bug hunter level 1": 1 << 3,
    "dom bravery": 1 << 6,
    "dom brilliance": 1 << 7,
    "dom balance": 1 << 8,
    "wczesny sympatyk": 1 << 9,
    "bug hunter level 2": 1 << 14,
    "developer zweryfikowanego bota": 1 << 17,
    "certyfikowany moderator": 1 << 18
}

def user_flags(_user_flags):
    _flags = []

    for flag in flags:
        if (_user_flags & flags[flag]) == flags[flag]:
            _flags.append(flag)

    return _flags