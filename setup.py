from setuptools import setup

with open('requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='AesPublica',
    url='forest-tales.tk',
    author='SK',
    author_email='sk@sk.sk',
    version='1.0.0',
    long_description=__doc__,
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires
)
