from setuptools import setup

setup(name='minervaboto',
      description='A renewal tool for Acervo Minerva',
      # long_description=long_description,
      version='1.0.6',
      url='https://github.com/erickpires/minervaboto',
      author='Erick Pires',
      author_email='rckkas@gmail.com',
      license='MIT',
      packages=['minervaboto'],
      install_requires=[
          'appdirs',
          'beautifulsoup4',
          'configparser',
          'requests'
      ],
      entry_points={
          'console_scripts': [
              'minervaboto=minervaboto.__main__:main'
          ]
      }
)
