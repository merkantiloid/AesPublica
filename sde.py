from sys import argv
import zipfile
from app.services.import_sde import parse_type_ids, parse_market_groups, parse_groups, parse_categories, \
    parse_blueprints_attrs, parse_attrs, parse_type_attrs

script, path = argv
print("Importing SDE dump from %s" % path)

src = open(path, "rb")
zf = zipfile.ZipFile(src)

with zf.open('sde/fsd/typeIDs.yaml') as datafile:
    parse_type_ids(datafile)

with zf.open('sde/bsd/invMarketGroups.yaml') as datafile:
    parse_market_groups(datafile)

with zf.open('sde/fsd/groupIDs.yaml') as datafile:
   parse_groups(datafile)

with zf.open('sde/fsd/categoryIDs.yaml') as datafile:
   parse_categories(datafile)

with zf.open('sde/fsd/categoryIDs.yaml') as datafile:
   parse_categories(datafile)

with zf.open('sde/bsd/dgmAttributeTypes.yaml') as datafile:
    parse_attrs(datafile)

with zf.open('sde/bsd/dgmTypeAttributes.yaml') as datafile:
    parse_type_attrs(datafile)

with zf.open('sde/fsd/blueprints.yaml') as datafile:
    parse_blueprints_attrs(datafile)

zf.close()
src.close()