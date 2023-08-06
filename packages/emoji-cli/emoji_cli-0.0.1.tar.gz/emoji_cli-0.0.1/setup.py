import setuptools
from io import open

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="emoji_cli",
    version="0.0.1",
    keywords = ["tool","emoji", "clis", "shell", "emoji-cli", "表情emoji命令行工具"],
    author="houbb",
    author_email="houbinbin.echo@gmail.com",

    description="A emoji clis tool with python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/houbb/emoji-cli",

    # 这个参数是导入目录下的所有__init__.py包
    packages=setuptools.find_packages(),
    # 把文件打包到包里
    package_data={'db': ['emoji_cli/db/*']},
    include_package_data = True,

    # 这是一个数组，里边包含的是咱的pip项目引用到的第三方库，如果你的项目有用到第三方库，要在这里添上第三方库的包名，如果用的第三方版本不是最新版本，还要有版本号。
    install_requires=['fire'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],

    # CLI 必须指定信息
    entry_points = {
        'console_scripts': [
            'emoji_cli = emoji_cli:main'
        ]
    }
)
