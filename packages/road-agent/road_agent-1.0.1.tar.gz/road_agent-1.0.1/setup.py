from setuptools import setup, find_packages

def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='road_agent',
      version='1.0.1',
      description='Object-oriented framework for modeling of mobile agents.',
      long_description=readme(),
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering',
      ],
      url='http://gitlab.com/rgarcia-herrera/road-agent',
      author='Rodrigo Garcia',
      author_email='rgarcia@iecologia.unam.mx',
      license='GPLv3',
      packages=find_packages(),
      install_requires=[ 'LatLon', 'requests', 'sklearn', 'osmnx'],
      include_package_data=True,
      zip_safe=False)
