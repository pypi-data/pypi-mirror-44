from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='logs-analyzer',
      version='0.5.2',
      description='Logs-analyzer is a library containing functions that can help you extract usable data from logs.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/ddalu5/logs-analyzer',
      author='Salah OSFOR',
      author_email='osfor.salah@gmail.com',
      license='Apache V2',
      packages=find_packages(exclude=['docs', 'tests']),
      test_suite='tests',
      tests_require=['unittest'],
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Information Technology',
          'Topic :: System :: Logging',
          'Topic :: System :: Monitoring',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
      ],
      zip_safe=False)
