from sys import argv
import zipfile
import yaml

def parse_type_ids(file):
    print(".... loading type IDs")
    data = yaml.load(file)
    for key in data:
        print( data[key]['groupID'] )


script, path = argv
print("Importing SDE dump from %s" % path)

src = open(path, "rb")
zf = zipfile.ZipFile(src)
with zf.open('sde/fsd/typeIDs.yaml') as datafile:
    parse_type_ids(datafile)

zf.close()
src.close()