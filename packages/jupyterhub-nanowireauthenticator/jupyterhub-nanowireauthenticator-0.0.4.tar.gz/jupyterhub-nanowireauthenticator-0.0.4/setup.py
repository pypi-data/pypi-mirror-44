from setuptools import setup

setup(
    name='jupyterhub-nanowireauthenticator',
    version='0.0.4',
    description='Nanowire Authenticator for JupyterHub',
    url='https://github.com/spotlightdata/jupyterhub-nanowireauthenticator',
    author='Jonathan Balls',
    author_email='jonathan@spotlightdata.co.uk',
    license='3 Clause BSD',
    packages=['nanowireauthenticator'],
    install_requires = ['requests'],
)
