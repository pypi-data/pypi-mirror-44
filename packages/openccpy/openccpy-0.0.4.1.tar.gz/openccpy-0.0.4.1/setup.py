import setuptools
from io import open

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    # 别人搜索会用到的项目名称
    name="openccpy",
    version="0.0.4.1",
    keywords = ["tool","opencc", "opencc-py", "opencc-python", "Chinese Convert", "中文繁简体转换"],
    author="houbb",
    author_email="houbinbin.echo@gmail.com",

    description="Open Chinese Convert is an opensource project for conversion between Traditional Chinese and Simplified Chinese for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/houbb/pycc",

    # 这个参数是导入目录下的所有__init__.py包
    packages=setuptools.find_packages(),
    # 把文件打包到包里
    package_data={'db': ['openccpy/db/*']},
    include_package_data = True,

    # 这是一个数组，里边包含的是咱的pip项目引用到的第三方库，如果你的项目有用到第三方库，要在这里添上第三方库的包名，如果用的第三方版本不是最新版本，还要有版本号。
    install_requires = [],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)