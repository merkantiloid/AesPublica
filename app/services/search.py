from app import db
from app.eve_models import EveBlueprint, EveType
from sqlalchemy.sql import text

class SearchService:

    def __init__(self, type):
        self.type = type
        self.result = []


    SEARCH_BLUEPRINT_SQL = text(
        'select t.id, t.name'
        '  from eve_blueprints b, eve_types t'
        '  where b.id=t.id'
        '    and t.published=1'
        '    and t.name like :term'
    )


    SEARCH_TYPE_SQL = text(
        'select t.id, t.name'
        '  from eve_types t'
        '  where t.published=1'
        '    and t.name like :term'
        '  order by match(name) against(:exact) desc, length(name), name'
        '  limit 10'
    )

    def search(self, term):
        print(self.type, 'blueprint')
        self.result = []
        records = []
        if self.type == 'blueprint':
            records = db.session.execute(self.SEARCH_BLUEPRINT_SQL,  params={'term': '%'+term+'%'} )
        elif self.type == 'type':
            records = db.session.execute(self.SEARCH_TYPE_SQL,  params={'exact': term, 'term': '%'+term+'%'} )

        for record in records:
            self.result.append({
                'type_id': record[0],
                'name': record[1]
            })


    def to_json(self):
        return self.result