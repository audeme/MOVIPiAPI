from setuptools import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='movi',
    version='0.5',
    description='Raspberry Pi API for MOVI Voice Dialog Shield.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/audeme/MOVIPiAPI',
    author='Audeme',
    author_email='fractor@audeme.com',
    license=read('LICENSE'),
    packages=['movi'],
    install_requires=['pyserial']
)
