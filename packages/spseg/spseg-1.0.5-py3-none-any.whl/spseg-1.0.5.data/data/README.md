# 分词工具Python接口文档

### 一、工具安装和更新

`pip install spseg --index-url=https://pypi.python.org/simple --upgrade --user`

当前最新发布版本号为`1.0.5`。支持Python2.7.3和Python3.6.2，使用之前及时更新包。

### 二、模型词典资源

如果能ping通multimedia4.hz.163.org，可以使用wget命令下载。

`wget multimedia4.hz.163.org:7778/model.tar.gz`

### 三、简单示例

```python

import spseg
from spseg import SegmentorFactory, TaskMode

# 初始化分词工厂类实例
factory = SegmentorFactory()
#factory = SegmentorFactory("./")

# 创建分词实例
segmentor1 = factory.newInstance()
segmentor2 = factory.newInstance()

# 设置分隔符
segmentor1.setSeperator("#")
segmentor2.setSeperator("_")

# 设置工作模式
segmentor1.setMode(TaskMode.SEGMENTATION_REFERING_TO_LEXICON)
segmentor2.setMode(TaskMode.POSTAG_ACCORDING_TO_MODEL)

# 添加删除词汇
segmentor1.addUserWord("是个")
segmentor2.delUserWord("是个")

# 分词
print(segmentor1.seg("这是个测试"))
print(segmentor2.seg("这是个测试"))
```
SegmentorFactory对应创建分词工厂类实例，实例管理分词模型和词典资源，由配置文件指定资源目录。

工具在用户指定的资源目录查找`config.dat`配置文件，使用资源目录路径拼接词典和模型路径进行资源加载。

如果用户初始化SegmentorFactory实例时不指定资源目录，则在当前路径下查找`config.dat`资源配置文件。

#### 1、配置文件格式

```json
{
"default_lexicon_path":"user.lexicon.dat",
"segmentation_model_path":"people.pos.model.dat"
}
```

`default_lexicon_path`配置默认词典资源，不是必须参数。默认词典不支持增删，只能在词典资源文件中操作。

`segmentation_model_path`是必须参数，提供分词模型资源。

Segmentor对应分词实例，只由SegmentorFactory中newInstance方法创建，实例管理增删用户动态词汇、设置工作模式以及负责分词调用。

#### 2、设置工作模式

```c++
纯模型词性标注    POSTAG_ACCORDING_TO_MODEL
参考词典词性标注  POSTAG_REFERING_TO_LEXICON
纯词典词性标注    POSTAG_ACCORDING_TO_LEXICON

纯模型分词        SEGMENTATION_ACCORDING_TO_MODEL
参考词典分词      SEGMENTATION_REFERING_TO_LEXICON
纯词典分词        SEGMENTATION_ACCORDING_TO_LEXICON

纯模型全切分      FULL_SEGMENTATION_ACCORDING_TO_MODEL
参考词典全切分    FULL_SEGMENTATION_REFERING_TO_LEXICON
纯词典全切分      FULL_SEGMENTATION_ACCORDING_TO_LEXICON
```

**“参考词典（REFERING）”的解释：**保留模型结果的同时，按用户词典对模型结果进行切分和合并，避免“纯词典”模式会把非词典词拆分成单字。

用户需要注意在使用“参考词典（REFERING）”模式，当自定义词典中包含单字时，在待分文本中包含该单字且该字不能和上下文组词的情况下，会被切分成单字。

比如，使用SEGMENTATION_REFERING_TO_LEXICON模式，如下配置词典会有不同效果：

```
测试文本： 一会儿阴天，一会儿晴天，今天真是阴晴不定啊！

词典只包含“阴天”： 一会儿 阴天 ， 一会儿 晴天 ， 今天 真是 阴晴 不 定 啊 ！

词典只包含“阴天”和“阴”： 一会儿 阴天 ， 一会儿 晴天 ， 今天 真是 阴 晴 不 定 啊 ！

词典只包含“阴天”、“阴”和“阴晴不定”： 一会儿 阴天 ， 一会儿 晴天 ， 今天 真是 阴晴不定 啊 ！
```

可以看到，由于词典包含该单字，不能组词的单字被拆开，能组词的单字不受影响。

#### 3、编码格式

分词工具的seg接口，要求输入的以及输出的字符串编码格式均为utf8，使用者需要注意这点。

### 四、效率建议

#### 1. 接口使用建议

首先，SegmentorFactory每个实例之间的资源相互独立，不共用。 因此，如无必要不应创建过多的SegmentorFactory实例，避免内存浪费。

其次，相同SegmentorFactory实例通过newInstance创建的分词实例都共享该实例资源，尽量不要创建大量无必要的Segmentor实例。

最后，通过addUserWord为某个Segmentor实例添加的自定义词时，由于需要建立词索引，不建议用户分多次添加（即要在addUserWord全部完成后再调用seg，避免seg和addUserWord交叉进行）。

#### 2. 词典规模建议

测试由addUserWord添加不同规模的词汇量，可以了解相应的分词效率变化趋势。使用的测试集包含178684个字、共15863句、平均句长12字、不包含任何标点符号。

|默认词典大小|自定义词典大小|5次平均耗时(ms)|5次平均单句耗时(ms)|平均单句耗时相对增长率|
|---|---|---|---|---|
|0|0|4340|0.273|0.0%|
|0|5000|4807|0.303|10.9%|
|0|10000|4842|0.305|11.7%|
|0|20000|4828|0.304|11.3%|
|0|40000|4865|0.306|12.0%|
|0|95000|5127|0.323|18.3%|
|700000|0|5102|0.321|0.0%|
|700000|5000|5681|0.358|11.5%|
|700000|10000|5765|0.363|13.0%|
|700000|20000|5781|0.364|13.3%|
|700000|40000|5777|0.364|13.3%|
|700000|95000|6102|0.384|19.6%|

可以看到当默认词典为空时，自定义词典规模从0增长到95000，单句调用耗时增加18%；当默认词典规模为70W，自定义词典规模从0增长到95000，单句调用耗时增加19%。
