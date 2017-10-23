import yaml

from app import db
from app.eve_models import EveType, EveMarketGroup, EveGroup, EveCategory, EveAttribute, EveTypeAttribute
from sqlalchemy.sql import text

def parse_categories(file):
    print(".... loading categories")
    data = yaml.load(file, Loader=yaml.CLoader)
    for key in data:
        print(key, data[key]['name'].get('en','N/A'))
        item = EveCategory.query.get(key)
        if not item:
            item = EveCategory(id=key)
        item.icon_id = data[key].get('iconID',None)
        item.published = data[key]['published']
        item.name = data[key]['name']['en']
        db.session.add(item)
        db.session.commit()

def parse_groups(file):
    print(".... loadinggroups")
    data = yaml.load(file, Loader=yaml.CLoader)
    for key in data:
        print(key, data[key]['name'].get('en','N/A'))
        item = EveGroup.query.get(key)
        if not item:
            item = EveGroup(id=key)
        item.category_id = data[key]['categoryID']
        item.icon_id = data[key].get('iconID',None)
        item.published = data[key]['published']
        item.name = data[key]['name']['en']
        db.session.add(item)
        db.session.commit()


def parse_market_groups(file):
    print(".... loading market groups")
    data = yaml.load(file, Loader=yaml.CLoader)
    for record in data:
        key = record['marketGroupID']
        # print(key, record['marketGroupName'])
        item = EveMarketGroup.query.get(key)
        if not item:
            item = EveMarketGroup(id=key)
        item.name = record['marketGroupName']
        item.description = record.get('description','N/A')
        item.has_types = record['hasTypes']
        item.icon_id = record.get('iconID',None)
        item.parent_id = record.get('parentGroupID',None)
        db.session.add(item)
        db.session.commit()


def parse_type_ids(file):
    print(".... loading type IDs")
    data = yaml.load(file, Loader=yaml.CLoader)
    for key in data:
        print(key, data[key]['name'].get('en','N/A'))
        item = EveType.query.get(key)
        if not item:
            item = EveType(id=key)
        item.group_id = data[key].get('groupID',None)
        item.market_group_id = data[key].get('marketGroupID',None)
        item.volume = data[key].get('volume',None)
        item.name = data[key]['name'].get('en','N/A')
        item.portion_size = data[key]['portionSize']
        item.published = data[key]['published']
        db.session.add(item)
        db.session.commit()

def parse_numbers(fileValues, fileAttrs):
    print(".... loading numbers")
    sql = text("SELECT t.id, t.name"
        "           from eve_types t,"
        "                eve_groups g"
        "           where g.category_id=65"
        "             and g.published=1"
        "             and t.group_id = g.id"
        "             and t.published=1"
    )
    citadel_ids = db.session.execute(sql).fetchall()
    citadels = {}
    for record in citadel_ids:
        citadels[record[0]] = record[1]

    attrsRaw = yaml.load(fileAttrs, Loader=yaml.CLoader)
    attrs = {}
    for record in attrsRaw:
        attrs[record['attributeID']] = {
            'name': record['attributeName'],
            'description': record['description'],
        }

    data = yaml.load(fileValues, Loader=yaml.CLoader)
    for record in data:
        id = record['typeID']
        if id in citadels and record['attributeID'] in [2600,2601,2602]:
            print(citadels[id], attrs[record['attributeID']]['name'], record)
    # Sotiyo strEngMatBonus {'attributeID': 2600, 'typeID': 35827, 'valueFloat': 0.99}
    # Sotiyo strEngCostBonus {'attributeID': 2601, 'typeID': 35827, 'valueFloat': 0.95}
    # Sotiyo strEngTimeBonus {'attributeID': 2602, 'typeID': 35827, 'valueFloat': 0.7}


def parse_attrs(file):
    print(".... loading attributes")
    data = yaml.load(file, Loader=yaml.CLoader)
    for record in data:
        key = record['attributeID']
        print(key, record['attributeName'])
        item = EveAttribute.query.get(key)
        if not item:
            item = EveAttribute(id=key)

        item.code = record['attributeName']
        item.name = record.get('displayName','N/A')
        item.category_id = record.get('categoryID',None)
        item.default_value = record['defaultValue']
        item.description = record['description']
        item.icon_id = record.get('iconID',None)
        item.unit_id = record.get('unitID',None)
        item.published = record['published']
        item.stackable = record['stackable']
        item.high_is_good = record['highIsGood']

        db.session.add(item)
        db.session.commit()


def parse_type_attrs(file):
    print(".... loading attribute values for types")
    data = yaml.load(file, Loader=yaml.CLoader)
    for record in data:
        print(record)

        type_id = record['typeID']
        attr_id = record['attributeID']

        item = EveTypeAttribute.query.filter(EveTypeAttribute.type_id == type_id, EveTypeAttribute.attribute_id == attr_id).first()
        if not item:
            item = EveTypeAttribute(type_id=type_id, attribute_id = attr_id)

        if 'valueInt' in record:
            item.value = record['valueInt']
        elif 'valueFloat' in record:
            item.value = record['valueFloat']
        else:
            item.value = None

        db.session.add(item)
        db.session.commit()