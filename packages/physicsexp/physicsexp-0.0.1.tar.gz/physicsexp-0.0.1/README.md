# PhysicsExp
### USTC Physics Experiments Data Processing Tools

### 大物实验数据+数据处理工具

#### Comes with NO WARRENTY

最终目的是建造一套用于自动化处理大物实验数据、绘制图像、生成可打印文档、将文档提交到在线打印系统的工具；针对常用数据处理需求实现简化和自动化，只要简单的几行代码，就能完成通用的绘图、拟合、不确定度计算等大物实验常用任务。
理想与现实差距还很大，目前仅仅包装了一些matplotlib绘图库和文件输入简化重复劳动。

### A Simple Guide

Assuming you are using Windows. 

**Build**

```
python setup.py sdist bdist_wheel
```

Then the packaged wheel file can be found at `./dist/physicsexp-0.0.1-py3-none-any.whl`(Name may be different)

**Install**

**This package haven't been tested as it should and I don't know what will happen after installation.**

**Use a virtualenv is recommended. **

Create a virtualenv

```
python -m venv test-env
```

Activate it

```
./test-env/Scripts/activate.bat
```

Install the wheel (Use USTC mirror to accelerate, for it will download and install other packages)

```
pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple path\to\physicsexp-0.0.1-py3-none-any.whl
```

Wait a moment and installation will finish.

**Use**

Launch python in your venv

```
python
```

Import the package (`from xxx import *` may be bad, don't imitate me)

```
>>> from physicsexp.mainfunc import *
>>> from physicsexp.gendocx import *
>>>
```

Enjoy. 

Wanna know how to use? Read source code yourself, see examples at `Experiments/`(Most of them are already outdated and cannot be run), or contact developer.

But most of the time neither of these works. 

And can using these tools boost your efficiency? I don't know, but likely can't. 