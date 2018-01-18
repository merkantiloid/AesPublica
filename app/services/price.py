from app import db, esiclient
from app.models import Price, EveType
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import requests


class PriceService:

    def jita(self, source, type_id):
        temp = Price.query.filter(Price.source == source, Price.type_id == type_id).order_by(Price.id.desc()).first()
        return {
            'buy': temp.buy,
            'sell': temp.sell,
            'updated_at': temp.updated_at,
        }

    def esi(self, type_ids = []):
        db_types = self.outdated(type_ids,'esi')
        if len(db_types)>0:
            all_prices = esiclient.markets.prices()
            all_prices_hash = {}
            for r in all_prices:
                all_prices_hash[r['type_id']] = r['adjusted_price']
            ts = datetime.now().isoformat()
            for db_type in db_types:
                db_price = Price.query.filter(Price.source=='esi', Price.type_id==db_type.id).first()
                if not db_price:
                    db_price = Price(source='esi', type_id=db_type.id)
                db_price.buy = all_prices_hash[db_price.type_id]
                db_price.sell = all_prices_hash[db_price.type_id]
                db_price.updated_at = ts
                db.session.add(db_price)
            db.session.commit()


    def evemarketer(self, type_ids = []):
        db_types = self.outdated(type_ids,'evemarketer')
        if len(db_types)>0:
            ids = ','.join([str(x.id) for x in db_types])
            all_prices = requests.get(url='https://api.evemarketer.com/ec/marketstat/json?typeid='+ids+'&regionlimit=10000002')
            all_prices_hash = {}
            for r in all_prices.json():
                type_id = r['sell']['forQuery']['types'][0]
                all_prices_hash[type_id] = r

            ts = datetime.now().isoformat()
            for db_type in db_types:
                db_price = Price.query.filter(Price.source=='evemarketer', Price.type_id==db_type.id).order_by(Price.id.desc()).first()
                if not db_price:
                    db_price = Price(source='evemarketer', type_id=db_type.id)
                db_price.buy = all_prices_hash[db_type.id]['buy']['fivePercent']
                db_price.sell = all_prices_hash[db_type.id]['sell']['fivePercent']
                db_price.updated_at = ts

                db.session.begin_nested()
                try:
                    db.session.add(db_price)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
                db.session.commit()



    def outdated(self, type_ids, source):
        if len(type_ids)==0:
            return []

        db_types = EveType.query.from_statement(
            text(
                'select eve_types.* '
                '  from eve_types'
                '         left join prices on prices.type_id = eve_types.id and prices.source=:source'
                '  where eve_types.id in :ids '
                '    and (now()-cast(updated_at as datetime)>3600 or prices.id is null)'
            )
        ).params(source=source, ids=type_ids).all()
        return db_types




