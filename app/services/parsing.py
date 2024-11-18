import re
from .static import Static


def parse_name_qty(text):
    lines = text.splitlines()

    temp = {}

    for line in lines:
        success, type_id, qty, me, te = name_qty_line(line)
        if success:
            key = "%d-%d-%d" % (type_id,me,te)
            if key in temp:
                temp[key]['qty'] += qty
            else:
                temp[key] = {'type_id': type_id, 'qty': qty, 'me': me, 'te': te}

    return temp.values()


def name_qty_line(line):
    line = line.replace('[','')
    line = line.replace(']','')

    raw_parts = re.split("\s|,",line)
    parts = []
    for part in raw_parts:
        if part != '':
            parts.append(part)

    result_type_id = -1
    result_qty = 1
    result_me = 10
    result_te = 20

    index = 0
    last = len(parts)-1
    type_is_found = False
    last_result_index = -1
    while index <= last:
        possible = ' '.join([x.lower() for x in parts[0:index+1]])
        next_possible = ' '.join([x.lower() for x in parts[0:index+2]])
        if Static.type_hash_to_id(possible) and (index == last or not Static.type_hash_to_id(next_possible)):
            type_is_found = True
            result_type_id = Static.type_hash_to_id(possible)
            last_result_index = index + 1
        index += 1

    if last_result_index>-1:
        index = last_result_index

    qty_is_found = False
    if index <= last and type_is_found:
        ifrom = index
        while index <= last and not qty_is_found:
            if re.match('x{0,1}\d*$',parts[index]) and (index == last or not re.match('x{0,1}\d*$',parts[index+1])):
                qty_is_found = True
                num_parts = []
                for n in parts[ifrom:index+1]:
                    if re.match('x{0,1}\d*$',n):
                        num_parts.append(n.lower())
                pre_int = ''.join(num_parts)
                pre_int = pre_int.replace('x','')
                result_qty = int( pre_int )
            index += 1

    if index <= last and type_is_found:
        for part in parts[index:]:
            groups = re.match('ME\d*$',part)
            if groups:
                temp = int(groups[0][2:])
                if 0 <= temp <= 10:
                    result_me = temp

    if index <= last and type_is_found:
        for part in parts[index:]:
            groups = re.match('TE\d*$',part)
            if groups:
                temp = int(groups[0][2:])
                if 0 <= temp <= 20:
                    result_te = temp

    return type_is_found, result_type_id, result_qty, result_me, result_te
