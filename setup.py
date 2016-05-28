from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name="pydraw",
      version="0.1.2",
      description="Python GUI application demo for fun",
      long_description=readme() + '\n\n',
      author="Tong Zhang",
      author_email='zhangtong@sinap.ac.cn',
      platforms=["Linux"],
      license='GPL',
      packages=find_packages(),
      scripts=['scripts/pydraw'], )
