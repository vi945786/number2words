from decimal import Decimal, getcontext
from number2words import _fix_pronunciation, _get_place_rule, _PLACE_SPECIALS, _PLACE_UNITS, _PLACE_TENS, _PLACE_HUNDREDS, _PLACE_BIGS, _PLACE_ILLION
getcontext().prec = 3100

def fix(parts):
    _fix_pronunciation(parts)
    try:
        return [len("".join(parts)), parts[0][-1] in "aeiou", parts[-1][-1] in "aeiou"]
    except:
        pass

lengths = []
lengths += [fix([name]) for name in _PLACE_SPECIALS if len(name) != 0]
lengths += [fix([name]) for name in _PLACE_TENS if len(name) != 0]
lengths += [fix([unit + _get_place_rule(i, j, 0), ten]) for i, unit in enumerate(_PLACE_UNITS) for j, ten in enumerate(_PLACE_TENS) if len(unit) != 0 and len(ten) != 0]
lengths += [fix([name]) for name in _PLACE_HUNDREDS if len(name) != 0]
lengths += [fix([unit + _get_place_rule(i, 0, j), hundred]) for i, unit in enumerate(_PLACE_UNITS) for j, hundred in enumerate(_PLACE_HUNDREDS) if len(unit) != 0 and len(hundred) != 0]
lengths += [fix([ten, hundred]) for i, ten in enumerate(_PLACE_TENS) for j, hundred in enumerate(_PLACE_HUNDREDS) if len(ten) != 0 and len(hundred) != 0]
lengths += [fix([unit + _get_place_rule(i, j, k), ten, hundred]) for i, unit in enumerate(_PLACE_UNITS) for j, ten in enumerate(_PLACE_TENS) for k, hundred in enumerate(_PLACE_HUNDREDS) if len(unit) != 0 and len(ten) != 0 and len(hundred) != 0]


summed_lengths = 0
starts_with = 0
ends_with = 0
elements = Decimal(len(lengths))

for l in lengths:
    summed_lengths += l[0]
    starts_with += l[1]
    ends_with += l[2]

for i in range(1, len(_PLACE_BIGS)):
    average_len = summed_lengths / elements
    remove_from_start_of_next = starts_with if _PLACE_BIGS[i][-1] in "aeiou" else 0
    remove_from_end_of_prev = ends_with if _PLACE_BIGS[i][0] in "aeiou" else 0
    new_average_len = average_len + len(_PLACE_BIGS[i]) + average_len
    added_elements = (elements**2) -elements

    summed_lengths += new_average_len * added_elements - remove_from_start_of_next - remove_from_end_of_prev
    starts_with += added_elements * (starts_with / elements)
    ends_with += added_elements * (ends_with / elements)
    elements += added_elements

    summed_lengths += len(_PLACE_BIGS[i])
    starts_with += 1 if _PLACE_BIGS[i][0] in "aeiou" else 0
    ends_with += 1 if _PLACE_BIGS[i][-1] in "aeiou" else 0
    elements += 1

summed_lengths += (len(_PLACE_ILLION) * elements) - ends_with

summed_lengths += 8
elements += 1

summed_lengths += (elements * len("nine hundred and ninety nine , ")) - 2
summed_lengths *= 2
summed_lengths += len(" point ")

print(summed_lengths.to_integral_exact())