from sys import platform
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

exec(open('space_machines/version.py').read())

setup(
    name='space_machines',
    version=__version__,
    author='Brian Vesperman',
    author_email='bvesperman@gmail.com',
    url='https://github.com/bvesperman/Sector67RaspberryPiAccessControl',
    scripts=['bin/external-dependencies.sh'],
    packages=['space_machines'],
    license='MIT',
    description='Controlling or interfacing with simple machines from a Raspberry Pi.',
    long_description=open('README.md').read(),
    install_requires=[
        'RPi.GPIO' if platform=='linux2' else '',
        'rpi_ws281x' if platform=='linux2' else '',
        'expiringdict',
        'suds',
        'python_vlc',
        'gTTS'
    ],
    #test_suite='nose.collector',
    #tests_require=['nose'],
    classifiers=[
          'License :: OSI Approved :: MIT License',
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python :: 2.7',
    ],
)
