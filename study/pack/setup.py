from setuptools import setup, find_packages


def read_file(file):
    with open(file, "rt") as f:
        return f.read()


setup(
    name='mylib',
    version='1.0',
    author='Sunny',
    author_email='morningtest@126.com',
    description='Time Decorator',
    packages=find_packages(exclude=[]),  # ['my_pack']
    # 依赖包，自动安装
    install_requires=[i for i in read_file("requirements.txt").strip().splitlines() if i != ''],
    # 使MANIFEST.in生效
    include_package_data=True,
    # 仅在测试时需要使用的依赖，在正常发布的代码中是没有用的。
    # 在执行python setup.py test时，可以自动安装这三个库，确保测试的正常运行。
    tests_require=[
        'pytest>=3.3.1',
        'pytest-cov>=2.5.1',
    ],
)
