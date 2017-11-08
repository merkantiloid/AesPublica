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


def load_repr_rigs():
    sql = text(
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
    rig_raws = db.session.execute(sql).fetchall()
    rigs = {
        2: [{'id': -1, 'name': '-None-', 'value': 0.5, 'kh': 1, 'kl': 1, 'kz': 1}],
        3: [{'id': -1, 'name': '-None-', 'value': 0.5, 'kh': 1, 'kl': 1, 'kz': 1}],
        4: [{'id': -1, 'name': '-None-', 'value': 0.5, 'kh': 1, 'kl': 1, 'kz': 1}],
    }
    for record in rig_raws:
        rigs[int(record[3])].append({
            'id': record[0],
            'name': record[1],
            'value': record[2],
            'kh': record[4],
            'kl': record[5],
            'kz': record[6],
        })
    return rigs
