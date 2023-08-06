from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='mailtransfer',
    version='1.0',
    author='Alexander Makeenkov',
    author_email='whoami.tut@gmail.com',
    url='https://github.com/amakeenk/mailtransfer',
    description='Simple linux tool for transfer mails from one mailserver to another mailserver',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=['colorama', 'configobj', 'emails', 'imap_tools'],
    include_package_data=True,
    entry_points={
        'console_scripts':
            ['mailtransfer = mailtransfer.main:main']
        }
)
