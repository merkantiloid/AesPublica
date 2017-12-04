#!aes-env/bin/python3
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(url='mysql://aes:aes@localhost/aes?charset=utf8', repository='./migrations', debug='False')
