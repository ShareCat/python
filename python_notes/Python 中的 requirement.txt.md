### Python 中的 requirement.txt

#### Python 中的依赖
Python 需要维护项目相关的依赖包。通常我们会在项目的根目录下放置一个 requirement.txt 文件，用于记录所有依赖包和它的确切版本号。

requirement.txt 的内容长这样：
```text
alembic==1.0.10
appnope==0.1.0
astroid==2.2.5
attrs==19.1.0
backcall==0.1.0
bcrypt==3.1.6
bleach==3.1.0
cffi==1.12.3
Click==7.0
decorator==4.4.0
defusedxml==0.6.0
entrypoints==0.3
...
```

#### 如何使用？
那么 requirement.txt 究竟如何使用呢？

当我们拿到一个项目时，首先要在项目运行环境安装 requirement.txt 所包含的依赖：
```shell
pip install -r requirement.txt
```

当我们要把环境中的依赖写入 requirement.txt 中时，可以借助 freeze 命令：
```shell
pip freeze >requirements.txt
```

#### 环境混用怎么办？
在导出依赖到 requirement.txt 文件时会有一种尴尬的情况。

你的本地环境不仅包含项目 A 所需要的依赖，也包含着项目 B 所需要的依赖。此时我们要如何做到只把项目 A 的依赖导出呢？

pipreqs 可以通过扫描项目目录，帮助我们仅生成当前项目的依赖清单。

通过以下命令安装：
```shell
pip install pipreqs
```

运行：
```shell
pipreqs ./
```

#### 命令不识别
```shell
user@user-virtual-machine:~/.local/bin$ pipreqs ./
pipreqs: command not found
```

原因是，pipreqs没有纳入环境变量，可以通过"pip3 show -f pipreqs",找到python的Scripts目录
```shell
user@user-virtual-machine:~/.local/bin$ pip3 show -f pipreqs
Name: pipreqs
Version: 0.4.11
Summary: Pip requirements.txt generator based on imports in project
Home-page: https://github.com/bndr/pipreqs
Author: Vadim Kravcenko
Author-email: vadim.kravcenko@gmail.com
License: Apache License
Location: /home/user/.local/lib/python3.8/site-packages
Requires: docopt, yarg
Required-by: 
Files:
  ../../../bin/pipreqs
  pipreqs-0.4.11.dist-info/AUTHORS.rst
  pipreqs-0.4.11.dist-info/INSTALLER
  pipreqs-0.4.11.dist-info/LICENSE
  pipreqs-0.4.11.dist-info/METADATA
  pipreqs-0.4.11.dist-info/RECORD
  pipreqs-0.4.11.dist-info/WHEEL
  pipreqs-0.4.11.dist-info/entry_points.txt
  pipreqs-0.4.11.dist-info/top_level.txt
  pipreqs/__init__.py
  pipreqs/__pycache__/__init__.cpython-38.pyc
  pipreqs/__pycache__/pipreqs.cpython-38.pyc
  pipreqs/mapping
  pipreqs/pipreqs.py
  pipreqs/stdlib

```

根据 /home/user/.local/lib/python3.8/site-packages 和 ../../../bin/pipreqs 知道pipreqs的路径为：/home/user/.local/bin

手动添加环境变量解决，打开.bashrc文件，在最后一行添加：
```shell
export PATH=/home/user/.local/bin:$PATH
```

需要立即生效，运行：
```shell
source .bashrc
```
