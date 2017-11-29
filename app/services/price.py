from app import db, preston
from app.models import Price, EveType
from sqlalchemy import text
from datetime import datetime


class PriceService:

    def esi(self, type_ids = []):
        db_types = EveType.query.from_statement(
            text(
                'select eve_types.* '
                '  from eve_types'
                '         left join prices on prices.type_id = eve_types.id and prices.source=:source'
                '  where eve_types.id in :ids '
                '    and (now()-cast(updated_at as datetime)>3600 or prices.id is null)'
            )
        ).params(source='esi', ids=type_ids).all()

        if len(db_types)>0:

            all_prices = preston.markets.prices()
            all_prices_hash = {}
            for r in all_prices:
                all_prices_hash[r['type_id']] = r['adjusted_price']

            ts = datetime.now().isoformat()

            for db_type in db_types:
                db_price = Price.query.filter(Price.source=='esi', Price.type_id==db_type.id).first()
                if not db_price:
                    db_price = Price(source='esi', type_id=db_type.id)
                db_price.value = all_prices_hash[db_price.type_id]
                db_price.updated_at = ts
                db.session.add(db_price)

            db.session.commit()



