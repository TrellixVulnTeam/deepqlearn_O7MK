from setuptools import setup
from pip.req import parse_requirements

# parse_requirements() returns generator of pip.req.InstallRequirement objects
reqs = parse_requirements('./requirements.txt', session=False)

# reqs is a list generator of requirements
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
install_requires = [str(ir.req) for ir in reqs]
#print(install_requires)

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='deepqpong',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Flying Circus',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['deepqpong'],
      zip_safe=False)
