import sys
from typing import Tuple, List

_NORMAL_UNITS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine")
_NORMAL_TENS = ("", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety")
_NORMAL_SPECIALS = ("ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen")
_NORMAL_HUNDRED = "hundred"

_FRACTION_AND = "and"

_PLACE_THOUSAND = "thousand"
_PLACE_SPECIALS = ("m", "b", "tr", "quadr", "quint", "sext", "sept", "oct", "non")
_PLACE_UNITS = ("", "un", "duo", "tre", "quattuor", "quin", "se", "septe", "octo", "nove")
_PLACE_UNITS_RULES = ("", "", "", "", "", "", "sx", "mn", "", "mn")
_PLACE_TENS = ("", "deci", "viginti", "triginta", "quadraginta", "quinquaginta", "sexaginta", "septuaginta", "octoginta", "nonaginta")
_PLACE_TENS_RULES = ("", "n", "ms", "ns", "ns", "ns", "n", "n", "mx", "")
_PLACE_HUNDREDS = ("", "centi", "ducenti", "trecenti", "quadringenti", "quingenti", "sescenti", "septingenti", "octingenti", "nongenti")
_PLACE_HUNDREDS_RULES = ("", "nx", "n", "ns", "ns", "ns", "n", "n", "mx", "")
_PLACE_BIGS = ("", "mill", "micro", "nano", "pico", "femto", "atto", "zepto", "yocto", "ronto", "quecto")
_PLACE_ILLION = "illion"

def _split_number(num: int) -> Tuple[int, int, int]:
    return num // 100 % 10, num // 10 % 10, num % 10

def _get_groups(num: int) -> List[Tuple[int, int, int]]:
    groups = []
    while num > 0:
        groups.append(_split_number(num))
        num //= 1000
    return groups

def _is_number_str(s: str) -> bool:
    if s == "-" or s[0] not in "0123456789-" or s.count(".") > 1:
        return False
    for c in s[1:]:
        if not (c.isdigit() or c == '.'):
            return False
    return True

def _get_normal_fraction(num: str) -> Tuple[str, str]:
    if "." in num:
        normal, fraction = num.split(".")
        return normal, fraction
    else:
        return num, "0"

def _count_leading_zeros(num: str) -> int:
    return len(num) - len(num.lstrip('0'))

def get_number_name(num: str) -> str:
    num = num.strip()

    if not _is_number_str(num):
        raise ValueError()

    normal, fraction = _get_normal_fraction(num)

    name = _get_normal_name(abs(int(normal)))

    if len(fraction.strip("0")) != 0:
        if name == "zero":
            name = ""
        else:
            name += f" {_FRACTION_AND} "
        name += _get_fraction_name(fraction.rstrip('0'))

    if num[0] == "-" and name != "zero":
        name = f"negative {name}"

    return name

def _get_place_amount(amount):
    match amount:
        case 0:
            return ""
        case 1:
            return _NORMAL_TENS[1]
        case 2:
            return _NORMAL_HUNDRED

def _get_fraction_name(fraction: str):
    power = len(fraction) // 3
    amount = len(fraction) % 3
    num = int(fraction)

    amount_name = ""
    if power == 0:
        denominator = _get_place_amount(amount)
    else:
        denominator = _get_place_name(power)
        amount_name = _get_place_amount(amount)

    name = f"{_get_normal_name(num)} "
    if amount_name:
        name += f"{amount_name}-"
    name += denominator + "th"
    if num != 1:
        name += "s"
    return name

def _get_normal_name(num: int) -> str:
    groups = _get_groups(num)

    if len(groups) == 0:
        return _NORMAL_UNITS[0]

    name = ""
    for i, group in [*enumerate(groups)][::-1]:
        if group[0] != 0:
            hundreds = group[0]
            name += f"{_NORMAL_UNITS[hundreds]} {_NORMAL_HUNDRED} "

        if group[1] + group[2] != 0:
            if 1 <= group[1] < 2:
                name += f"{_NORMAL_SPECIALS[group[2]]} "
            else:
                if group[1] != 0:
                    name += f"{_NORMAL_TENS[group[1]]}"
                    name += "-" if group[2] != 0 else " "
                if group[2] != 0:
                    name += f"{_NORMAL_UNITS[group[2]]} "

        if i > 0 and sum(group) != 0:
            name += f"{_get_place_name(i)}, "

    name = name.strip()
    if name.endswith(","):
        name = name[:-1]

    return name

def _get_place_rule(units, tens, hundreds):
    if tens != 0:
        next_add = _PLACE_TENS_RULES[tens]
    else:
        if hundreds != 0:
            next_add = _PLACE_HUNDREDS_RULES[hundreds]
        else:
            next_add = None

    for rule in _PLACE_UNITS_RULES[units]:
        if next_add is not None and rule in next_add:
            return rule

    return ""

def _fix_pronunciation(parts):
    for i in range(len(parts)-1):
        if parts[i] and parts[i+1]:
            if parts[i][-1] in "aeiou" and parts[i+1][0] in "aeiou":
                parts[i] = parts[i][:-1]

def _get_place_name(power: int) -> str:
    power -= 1

    if power == 0:
        return _PLACE_THOUSAND

    if power >= 10**33:
        raise ValueError("unnamed number")

    parts = []
    groups = _get_groups(power)

    for i, group in [*enumerate(groups)][::-1]:
        group_parts = []

        if i != 0 and group != 0:
            group_parts.append(_PLACE_BIGS[i])
            group = _split_number(group[0]*100 + group[1]*10 + group[2] - 1)

        if sum(group[:2]) == 0:
            group_parts.append(_PLACE_SPECIALS[group[2]-1])
        else:
            if group[0] > 0:
                group_parts.append(_PLACE_HUNDREDS[group[0]])
            if group[1] > 0:
                group_parts.append(_PLACE_TENS[group[1]])
            if group[2] > 0:
                group_parts.append(_PLACE_UNITS[group[2]] + _get_place_rule(*group))

        parts += group_parts[::-1]

    parts.append(_PLACE_ILLION)
    _fix_pronunciation(parts)

    return "".join(parts)

def test():
    assert get_number_name("0.123") == "one hundred twenty-three thousandths"
    assert get_number_name("0.001") == "one thousandth"
    assert get_number_name("12345678.0") == "twelve million, three hundred forty-five thousand, six hundred seventy-eight"
    assert get_number_name("0.01") == "one hundredth"
    assert get_number_name("0") == "zero"
    assert get_number_name("-0") == "zero"
    assert get_number_name("-0.1") == "negative one tenth"
    assert get_number_name("-0.1000000000000") == "negative one tenth"
    assert get_number_name("-123456.00005") == "negative one hundred twenty-three thousand, four hundred fifty-six and five hundred-thousandths"

if __name__ == '__main__':
    if len(sys.argv) == 1:
        while True:
            print(get_number_name(input("enter a number: "))) # any number between 10^10^33 and -10^10^33 which have more than 500 time more digits than the mass of the sun in kilograms
    else:
        globals()[sys.argv[1]]()
