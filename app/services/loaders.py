from sqlalchemy.sql import text
from app import db


def load_citadels():
    sql = text(
        "SELECT t.id, t.name"
        "  from eve_types t,"
        "       eve_groups g"
        "  where g.category_id=65"
        "    and g.published=1"
        "    and t.group_id = g.id"
        "    and t.published=1"
        "  order by t.name"
    )
    citadel_raws = db.session.execute(sql).fetchall()
    citadels = []
    for record in citadel_raws:
        citadels.append({'id': record[0], 'name': record[1]})
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
