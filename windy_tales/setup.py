from setuptools import setup, find_packages

requires = [
    'pycparser',
    'cloudy_tales',
    'watchdog'
]

setup(name='windy_tales',
      version='0.0',
      description='windy_tales',
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="windy_tales",
      entry_points="""\
      [paste.app_factory]
      main = windy_tales:main
      """,
      )
