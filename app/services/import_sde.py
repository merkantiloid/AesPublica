import yaml

from app import db
from app.eve_models import EveType, EveMarketGroup, EveGroup, EveCategory,\
    EveAttribute, EveTypeAttribute, EveBlueprint, EveTypeMaterial


def parse_categories(file):
    print(".... loading categories")
    data = yaml.load(file, Loader=yaml.Loader)
    for key in data:
        name = data[key]['name'].get('en', 'N/A').encode("utf-8")
        print(key, name)
        item = EveCategory.query.get(key)
        if not item:
            item = EveCategory(id=key)
        item.icon_id = data[key].get('iconID', None)
        item.published = data[key]['published']
        item.name = name
        db.session.add(item)
    db.session.commit()


def parse_groups(file):
    print(".... loading groups")
    data = yaml.load(file, Loader=yaml.Loader)
    for key in data:
        name = data[key]['name'].get('en', 'N/A').encode("utf-8")
        print(key, name)
        item = EveGroup.query.get(key)
        if not item:
            item = EveGroup(id=key)
        item.category_id = data[key]['categoryID']
        item.icon_id = data[key].get('iconID', None)
        item.published = data[key]['published']
        item.name = name
        db.session.add(item)
    db.session.commit()


def parse_market_groups(file):
    print(".... loading market groups")
    data = yaml.load(file, Loader=yaml.Loader)
    for record in data:
        key = record['marketGroupID']
        # print(key, record['marketGroupName'])
        item = EveMarketGroup.query.get(key)
        if not item:
            item = EveMarketGroup(id=key)
        item.name = record['marketGroupName']
        item.description = record.get('description', 'N/A')
        item.has_types = record['hasTypes']
        item.icon_id = record.get('iconID', None)
        item.parent_id = record.get('parentGroupID', None)
        db.session.add(item)
    db.session.commit()


def parse_type_ids(file):
    print(".... loading type IDs")
    data = yaml.load(file, Loader=yaml.Loader)
    for key in data:
        name = data[key]['name'].get('en', 'N/A').encode("utf-8")
        print(key, name)
        item = EveType.query.get(key)
        if not item:
            item = EveType(id=key)
        item.group_id = data[key].get('groupID', None)
        item.market_group_id = data[key].get('marketGroupID', None)
        item.volume = data[key].get('volume', None)
        item.name = name
        item.portion_size = data[key]['portionSize']
        item.published = data[key]['published']
        db.session.add(item)
    db.session.commit()


def parse_attrs(file):
    print(".... loading attributes")
    data = yaml.load(file, Loader=yaml.Loader)
    for record in data:
        key = record['attributeID']
        print(key, record['attributeName'])
        item = EveAttribute.query.get(key)
        if not item:
            item = EveAttribute(id=key)

        item.code = record['attributeName']
        item.name = record.get('displayName', 'N/A')
        item.category_id = record.get('categoryID', None)
        item.default_value = record['defaultValue']
        item.description = record['description']
        item.icon_id = record.get('iconID', None)
        item.unit_id = record.get('unitID', None)
        item.published = record['published']
        item.stackable = record['stackable']
        item.high_is_good = record['highIsGood']

        db.session.add(item)
    db.session.commit()


def parse_type_attrs(file):
    print(".... loading attribute values for types")
    data = yaml.load(file, Loader=yaml.Loader)
    for record in data:
        print(record)

        type_id = record['typeID']
        attr_id = record['attributeID']

        item = EveTypeAttribute.query.filter(EveTypeAttribute.type_id == type_id,
                                             EveTypeAttribute.attribute_id == attr_id).first()
        if not item:
            item = EveTypeAttribute(type_id=type_id, attribute_id=attr_id)

        if 'valueInt' in record:
            item.value = record['valueInt']
        elif 'valueFloat' in record:
            item.value = record['valueFloat']
        else:
            item.value = None

        db.session.add(item)
    db.session.commit()


def parse_blueprints_attrs(file):
    print(".... loading blueprints")
    data = yaml.load(file, Loader=yaml.Loader)
    for key in data:
        print(key)
        item = EveBlueprint.query.filter(EveBlueprint.id == key).first()
        if not item:
            item = EveBlueprint(id=key)
        item.props = data[key]
        if "manufacturing" in data[key]["activities"] and "products" in data[key]["activities"]["manufacturing"]:
            item.product_id = data[key]["activities"]["manufacturing"]["products"][0]["typeID"]

        if "reaction" in data[key]["activities"] and "products" in data[key]["activities"]["reaction"]:
            item.product_id = data[key]["activities"]["reaction"]["products"][0]["typeID"]

        db.session.add(item)
    db.session.commit()


def parse_type_materials(file):
    print(".... loading type materials")
    data = yaml.load(file, Loader=yaml.Loader)
    for record in data:
        item = EveTypeMaterial.query.filter(EveTypeMaterial.type_id == record['typeID'],
                                            EveTypeMaterial.material_id == record['materialTypeID']).first()
        if not item:
            item = EveTypeMaterial(type_id=record['typeID'], material_id=record['materialTypeID'])
        item.qty = record['quantity']
        db.session.add(item)
    db.session.commit()
