from setuptools import setup, find_packages

setup(
    name='siwat_light_control_protocol',
    version='1.0',
    license='Apache 2.0',
    author="Siwat Sirichai",
    author_email='siwat@siwatinc.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/SiwatINC/siwat-light-control-protocol',
    keywords='light mqtt serial raspberry-pi-pico',
    install_requires=[
          'pyserial',
      ],

)