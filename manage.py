#!probleme/bin/python3
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='mysql://eow:eow@localhost/evecalc_dev?charset=utf8', repository='./migrations', debug='False')
