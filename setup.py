from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='siwat_light_control_protocol',
    version='3.15',
    license='Apache 2.0',
    author="Siwat Sirichai",
    author_email='siwat@siwatinc.com',
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/SiwatINC/siwat-light-control-protocol',
    keywords='light mqtt serial raspberry-pi-pico',
    install_requires=[
          'pyserial',
          'paho-mqtt',
          'wheel',
          'numpy',
          'scipy'
      ],

)