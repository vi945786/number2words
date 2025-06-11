def get_number_name(num: int) -> str:
    units_place = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
    tens_place = ("", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")
    specials = (*units_place, "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
    hundred = "hundred"

    name = ""

    if num < 0:
        name = "negative "
        num *= -1

    groups = []
    while num > 0:
        groups.append((num // 100 % 10, num % 100))
        num //= 1000
    groups = groups

    if len(groups) == 0:
        return units_place[0]

    for i, group in [*enumerate(groups)][::-1]:
        if group[0] != 0:
            hundreds = group[0]
            name += f"{units_place[hundreds]} {hundred} "
            if group[1] != 0:
                name += "and "

        if group[1] != 0:
            tens_ones = group[1]
            if tens_ones < 20:
                name += f"{specials[tens_ones]} "
            else:
                if (ten := group[1] // 10 % 10) != 0:
                    name += f"{tens_place[ten]} "
                if (one := group[1] % 10) != 0:
                    name += f"{units_place[one]} "

        if i > 0 and group != (0, 0):
            name += f"{_get_place_name(i-1)} "

    return name

def _get_place_name(num: int) -> str:
    special_names = ("thousand", "million", "billion", "trillion", "quadrillion", "quintillion", "sextillion", "septillion", "octillion", "nonillion")
    units = ("", "un", "duo", "tre", "quattuor", "quin", "se", "septe", "octo", "nove")
    units_add = ("", "", "", "", "", "", "sx", "mn", "", "mn")
    tens = ("", "deci", "viginti", "triginta", "quadraginta", "quinquaginta", "sexaginta", "septuaginta", "octoginta", "nonaginta")
    tens_add = ("", "n", "ms", "ns", "ns", "ns", "n", "n", "mx", "")
    hundreds = ("", "centi", "ducenti", "trecenti", "quadringenti", "quingenti", "sescenti", "septingenti", "octingenti", "nongenti")
    hundreds_add = ("", "nx", "n", "ns", "ns", "ns", "n", "n", "mx", "")
    nexts = ("", "mill", "micro", "nano", "pico", "femto", "atto", "zepto", "yocto", "ronto", "quecto")

    if num == 0:
        return special_names[0]

    if num >= 10**33:
        raise ValueError("unnamed number")

    parts = []

    groups = []
    while num > 0:
        groups.append(num % 1000)
        num //= 1000
    groups = groups

    for i, group in [*enumerate(groups)][::-1]:
        if i != 0 and group != 0:
            parts.append(nexts[i])
            if group != 0:
                group -= 1

        if 0 < group < 10:
            parts.append(special_names[group])
            continue

        unit = group % 10
        ten = (group // 10) % 10
        hundred = (group // 100) % 10

        if unit > 0:
            next_add = None if ten == 0 and hundred == 0 else hundreds_add[hundred] if ten == 0 else tens_add[ten]
            parts.append(next((units[unit] + c for c in units_add[unit] if c in next_add), units[unit]))
        if ten > 0:
            parts.append(tens[ten])
        if hundred > 0:
            parts.append(hundreds[hundred])

    if len(parts) == 0:
        print(num)

    if not parts[-1].endswith("illion"):
        parts.append("illion")

    for i in range(len(parts)-1):
        if parts[i] and parts[i+1]:
            if parts[i][-1] in "aeiou" and parts[i+1][0] in "aeiou":
                parts[i] = parts[i][:-1]

    return "".join(parts)

print(get_number_name(int(input("enter a number: ")))) # any number up until 10^10^33 which has more digits than the mass of the sun in kilograms times 500