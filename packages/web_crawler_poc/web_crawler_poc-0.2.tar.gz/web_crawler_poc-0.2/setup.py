from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='web_crawler_poc',
      version='0.2',
      description='Crawler to print web links',
      url='http://github.com/storborg/funniest',
      author='Aneesh Nair',
      author_email='aneeshrnair@gmail.com',
      license='MIT',
      packages=['web_crawler'],
      install_requires=[
          'lxml',
          'beautifulsoup4',
          'requests'
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
