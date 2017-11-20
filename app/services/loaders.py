from sqlalchemy.sql import text
from app import db


def load_citadels():
    sql = text(
        "SELECT t.id, t.name, ta.value as rig_size"
        "  from eve_types t,"
        "       eve_groups g,"
        "       eve_type_attributes ta,"
        "       eve_attributes a"
        "  where g.category_id=65"
        "    and g.published=1"
        "    and t.group_id = g.id"
        "    and t.published=1"
        "    and ta.type_id=t.id"
        "    and a.id=ta.attribute_id"
        "    and a.id in (1547)"
        "  order by t.name"
    )
    citadel_raws = db.session.execute(sql).fetchall()
    citadels = []
    for record in citadel_raws:
        citadels.append({'id': record[0], 'name': record[1], 'rig_size': int(record[2])})
    return citadels


def load_repr_implants():
    sql = text(
        "SELECT t.id, t.name, ta.value"
        "  FROM eve_types t,"
        "       eve_groups g,"
        "       eve_type_attributes ta,"
        "       eve_attributes a"
        "  where ta.type_id=t.id"
        "    and t.published=1"
        "    and a.id=ta.attribute_id"
        "    and a.id=379"
        "    and g.id=t.group_id"
        "    and g.category_id=20"
        "  order by t.name"
    )
    implant_raws = db.session.execute(sql).fetchall()
    implants = [{'id': -1, 'name': '-None-', 'value': 0}]
    for record in implant_raws:
        implants.append({'id': record[0], 'name': record[1], 'value': record[2]})
    return implants


REPR_RIGS_SQL = text(
    "SELECT t.id, t.name,"
    "       ta.value,"
    "       ta2.value as rig_size,"
    "       taH.value as rig_H,"
    "       taL.value as rig_L,"
    "       taZ.value as rig_Z"
    " FROM eve_types t,"
    "      eve_groups g,"
    "      eve_type_attributes ta,"
    "      eve_attributes a,"
    "      eve_type_attributes ta2,"
    "      eve_attributes a2,"
    "      eve_type_attributes taH,"
    "      eve_attributes aH,"
    "      eve_type_attributes taL,"
    "      eve_attributes aL,"
    "      eve_type_attributes taZ,"
    "      eve_attributes aZ"
    " where t.published=1"
    "   and g.id=t.group_id"
    "   and g.category_id = 66"
    "   and t.market_group_id in (2341,2342,2343)"
    "   and ta.type_id=t.id"
    "   and a.id=ta.attribute_id"
    "   and a.id in (717)"
    "   and ta2.type_id=t.id"
    "   and a2.id=ta2.attribute_id"
    "   and a2.id in (1547)"
    "   and taH.type_id=t.id"
    "   and aH.id=taH.attribute_id"
    "   and aH.id in (2355)"
    "   and taL.type_id=t.id"
    "   and aL.id=taL.attribute_id"
    "   and aL.id in (2356)"
    "   and taZ.type_id=t.id"
    "   and aZ.id=taZ.attribute_id"
    "   and aZ.id in (2357)"
    " order by t.name  "
)

def get_metas(record):
    if record[3]>2:
        return ['ore','ice','moon']
    elif record[3] == 2 and "Asteroid Ore" in record[1]:
        return ['ore']
    elif record[3] == 2 and "Ice" in record[1]:
        return ['ice']
    elif record[3] == 2 and "Moon Ore" in record[1]:
        return ['moon']

def load_repr_rigs():
    rig_raws = db.session.execute(REPR_RIGS_SQL).fetchall()
    rigs = {
        2: [{'id': -1, 'name': '-None-', 'value': 0.5, 'h': 1, 'l': 1, 'z': 1, 'metas': ['ore','ice','moon']}],
        3: [{'id': -1, 'name': '-None-', 'value': 0.5, 'h': 1, 'l': 1, 'z': 1, 'metas': ['ore','ice','moon']}],
        4: [{'id': -1, 'name': '-None-', 'value': 0.5, 'h': 1, 'l': 1, 'z': 1, 'metas': ['ore','ice','moon']}],
    }
    for record in rig_raws:
        temp = {
            'id': record[0],
            'name': record[1],
            'value': record[2],
            'size': record[3],
            'h': record[4],
            'l': record[5],
            'z': record[6],
        }
        temp['metas'] = get_metas(record)

        rigs[int(record[3])].append(temp)

    return rigs


def load_repr_rigs_hash():
    rig_raws = db.session.execute(REPR_RIGS_SQL).fetchall()
    rigs = {"-1": {'value': 0, 'h': 1, 'l': 1, 'z': 1, 'metas': ['ore','ice','moon']}}
    for record in rig_raws:
        rigs[record[0]] = {
            'id': record[0],
            'name': record[1],
            'value': record[2],
            'size': record[3],
            'h': record[4],
            'l': record[5],
            'z': record[6],
            'metas': get_metas(record),
        }

    return rigs


ALL_ORES_SQL = text(
    "select t.id," 
    "       t.name," 
    "       t.portion_size," 
    "       t.volume, "
    "       tac.value as compressed_id," 
    "       ta.value as ore_type,"
    "       case" 
    "         when mg.id = 1855 then 'ice'"
    "         when ta.value=4 then 'ore_m'"
    "         when mg.id in (512,514,521,522,525,530,517) then 'ore_z'"
    "         when mg.id in (527,528,529) then 'ore_l'"
    "         when mg.id in (523,526,516,515,519,518) then 'ore_h'"
    "         else null"
    "       end as ore_type_text"
    "  from eve_types t"
    "         inner join eve_market_groups mg on mg.id = t.market_group_id and (mg.parent_id=54 or mg.id = 1855)"
    "         inner join eve_type_attributes ta on ta.type_id = t.id and ta.attribute_id in (2699)"
    "         left join eve_type_attributes tac on tac.type_id = t.id and tac.attribute_id in (1940)"
    "  where t.published=1 "
    "  order by mg.name, t.portion_size, ta.value"
)
def load_ores():
    all_ores = db.session.execute(ALL_ORES_SQL).fetchall()
    ores = []
    for record in all_ores:
        all_ores.append(
            {
                "id": record[0],
                "name": record[1],
                "portion_size": record[2],
                "volume": record[3],
                "compressed_id": record[4],
                "ore_type": record[5],
                "ore_type_text": record[6],
            }
        )
    return ores


ALL_CHARS_SQL = text(
    "select c.id," 
    "       c.character_name,"
    "       ifnull(s3385.current_skill_level,0) as s3385,"
    "       ifnull(s3389.current_skill_level,0) as s3389,"
    "       ifnull(s12196.current_skill_level,0) as s12196"
    "  from esi_chars c"
    "         left join esi_skills s3385 on s3385.esi_char_id = c.id and s3385.skill_id = 3385" 
    "         left join esi_skills s3389 on s3389.esi_char_id = c.id and s3389.skill_id = 3389 "
    "         left join esi_skills s12196 on s12196.esi_char_id = c.id and s12196.skill_id = 12196" 
    "  where user_id=:user_id"
    "    and token_type = 'Character'"
    "  order by c.character_name "
)
def load_chars(user_id):
    records = db.session.execute(ALL_CHARS_SQL, params={'user_id': user_id}).fetchall()
    chars = []
    for record in records:
        chars.append(
            {
                "id": record[0],
                "name": record[1],
                "skills": {
                    3385: record[2],
                    3389: record[3],
                    12196: record[4],
                }
            }
        )
    return chars


CALC_IDS_SQL = text(
    "select id " 
    "  from eve_types"
    "  where group_id in (18,423)"
    "    and published=1"
)


def load_calc_ids():
    records = db.session.execute(CALC_IDS_SQL).fetchall()
    ids = []
    for record in records:
        ids.append(record[0])
    return ids