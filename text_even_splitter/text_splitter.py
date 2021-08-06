TEXT = """The Andromeda Galaxy (IPA: /ænˈdrɒmɪdə/), also known as Messier 31, M31, or NGC 224 and originally the Andromeda Nebula (see below), is a barred spiral galaxy approximately 2.5 million light-years (770 kiloparsecs) from Earth and the nearest major galaxy to the Milky Way.[6] The galaxy's name stems from the area of Earth's sky in which it appears, the constellation of Andromeda, which itself is named after the Ethiopian (or Phoenician) princess who was the wife of Perseus in Greek mythology.

The virial mass of the Andromeda Galaxy is of the same order of magnitude as that of the Milky Way, at 1 trillion solar masses (2.0×1042 kilograms). The mass of either galaxy is difficult to estimate with any accuracy, but it was long thought that the Andromeda Galaxy is more massive than the Milky Way by a margin of some 25% to 50%. This has been called into question by a 2018 study that cited a lower estimate on the mass of the Andromeda Galaxy,[10] combined with preliminary reports on a 2019 study estimating a higher mass of the Milky Way.[11][12] The Andromeda Galaxy has a diameter of about 220,000 ly (67 kpc), making it the largest member of the Local Group in terms of extension."""

MAX_WIDTH = 80

EXAMPLE = """
    The SIZE argument is an integer and 
        optional unit (example: 10K     is
    10*1024).   Units  are  K,M,G,T,P,E,Z,Y  (powers  of 1024) or KB,MB,...
    (powers                          of                              1000).

    Using color to distinguish file types is disabled bo
    th by  default  and
    with  --color=never.  With --color=auto, ls emits color codes only when
    standard output is connected to a terminal.  The LS_COLORS  environment
    variable can change the settings.  Use the dircolors command to set it.
"""


t2 = """
as d a sd a sd
"""


def f(s: str, max_width: int) -> str:
    r = []

    while len(s) > 0:
        new_max_width = max_width
        if len(s) <= max_width:
            r.append(s)
        else:
            c = s[:max_width]
            if max_width + 1 >= len(s):
                # print('1', c)
                r.append(c)
            elif s[max_width].isspace():
                # print('2', c)
                r.append(c)
            else:
                i = max_width - 1
                while not c[i].isspace():
                    i -= 1
                new_max_width = i
                c = s[:new_max_width]
                # print('3', c)
                r.append(c)

        t = new_max_width
        if len(s) < max_width:
            t = len(s)
        s = s[t:]
        # print('t', s)

    # print(r)
    rr = ""
    for c in r:
        if rr != "":
            rr += "\n"
        if len(c) == max_width:
            rr += c
            continue
        spaces = max_width - len(c)
        ind = c.index(' ')
        rr += c[:ind] + ' ' * spaces + c[ind:]

    return rr


print(MAX_WIDTH * 'a')
print(f(TEXT, MAX_WIDTH))
# print(f(t2, 3))
