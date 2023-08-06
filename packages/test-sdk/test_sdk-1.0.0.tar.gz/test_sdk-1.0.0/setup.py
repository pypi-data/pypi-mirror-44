from setuptools import setup, find_packages

def filter_pkg(x):
    return '_keras' not in x
pkgs = list(filter(filter_pkg, find_packages()))
print(pkgs)
setup(name='test_sdk',
      version='1.0.0',
      description='sdk',
      url='',
      packages=pkgs,
      install_requires=[]
     )