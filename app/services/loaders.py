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
        "SELECT t.id, t.name, ta.value, ta2.value as rig_size"
        "  FROM eve_types t,"
        "      eve_groups g,"
        "      eve_type_attributes ta,"
        "      eve_attributes a,"
        "      eve_type_attributes ta2,"
        "      eve_attributes a2"
        "  where t.published=1"
        "    and g.id=t.group_id"
        "    and t.market_group_id in (2341,2342,2343)"
        "    and ta.type_id=t.id"
        "    and a.id=ta.attribute_id"
        "    and a.id in (717)"
        "    and ta2.type_id=t.id"
        "    and a2.id=ta2.attribute_id"
        "    and a2.id in (1547)"
        "  order by t.name  "
    )
    rig_raws = db.session.execute(sql).fetchall()
    rigs = {
        2: [{'id': -1, 'name': '-None-', 'value': 0.5}],
        3: [{'id': -1, 'name': '-None-', 'value': 0.5}],
        4: [{'id': -1, 'name': '-None-', 'value': 0.5}],
    }
    for record in rig_raws:
        rigs[int(record[3])].append({'id': record[0], 'name': record[1], 'value': record[2]})
    return rigs
