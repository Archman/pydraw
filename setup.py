from setuptools import setup, find_packages

setup(
        name = "pydraw",
        version = "0.1.1",
        description = "Python GUI application demo for fun",
        author = "Tong Zhang",
        author_email = 'zhangtong@sinap.ac.cn',
        platforms = ["Linux"],
        license = 'GPL',
        packages = find_packages(),
        scripts = ['scripts/pydraw'],
)


