import yaml

from app import db
from app.eve_models import EveType, EveMarketGroup


def parse_market_groups(file):
    print(".... loading market groups")
    data = yaml.load(file, Loader=yaml.CLoader)
    for record in data:
        key = record['marketGroupID']
        print(key, record['marketGroupName'])
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