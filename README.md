# README
# Random Word Lists Generator
## 要实现什么？
python脚本，可以实现对一定格式的txt单词文档进行解析，进行格式化输出，输出md格式文档。该md的单词是乱序的，并且按5个一组的形式进行分组，每组具有数字标号。

## 实现的md 文档是什么？
形式如下：
```
# 0
dump*  vt. 倾卸，倾倒  n. 垃圾场
manufacture  vt. 大量制造，成批生产  n. 大量制造；工业品
impede*  vt. 阻碍，妨碍
inadequate*  a. 不充分的；不适当的
rural*  a. 农村的，乡村的

# 1
megacity  n. （人口超过1000万的）大城市
moist  a. 湿润的，潮湿的
shade  n. 阴凉处；（灯）罩；暗部；色度；细微差别  vt. 遮蔽，遮光；把……涂暗
constituent  n. 成分，要素；选区内的选民  a. 组成的；有宪法制定或修改权的
pollution*  n. 污染，污染物；玷污

...

```

## txt文本格式是什么？
```
inspiring* [ɪn'spaɪərɪŋ] a. 鼓舞（或激励）人心的；启发灵感的
attendance* /əˈtendəns/ n. 到场，出席；出勤；伺候，照料
optional* [ˈɒpʃənl]    a. 可选择的，非强制的，随意的
enable*   /ɪˈneɪbl/    vt. 使能够，使成为可能

...

```

## 整个执行的过程是什么？

- 将txt文档转换我csv文档
- 然后将csv文档转换为乱序 csv文档
- 然后根据乱序csv文档 以5个一组的形式转换为 md 文档

## 当txt更新后，更新的大概流程是什么？
- 更新的txt文档 -->
- 会重新生成更新后的csv文档-->
- 更新后的乱序csv文档(旧的部分没有打乱，放在新的csv文档末尾)-->
- 更新后的md文档(新的内容也在文档末尾，考虑到文档太长，不好查看新内容，同时生成反序版的md文档)

## python环境需要什么包？
需要的python包：csv pandas
```
pip install csv pandas
```

## txt格式是什么？音标的格式是什么？
要实现上述的效果，txt 每行的格式需要固定，如下：
```
可以是这样：

inspiring* [ɪn'spaɪərɪŋ] a. 鼓舞（或激励）人心的；启发灵感的
attendance* /əˈtendəns/ n. 到场，出席；出勤；伺候，照料
optional* [ˈɒpʃənl]    a. 可选择的，非强制的，随意的
enable*   /ɪˈneɪbl/    vt. 使能够，使成为可能

也可以是这样：
frame // 框架
word [] 单词
select {} 选择，挑选

```

txt的每行分3列，第一列是单词，第二列是音标，第三列是中文意思
这3列使用中间的音标作为分割点。

**音标有哪些形式？**
以下形式：
```
1: `/***/`

2: `[***]`

3: `{****}`

4: `//` `{}` `[]`

对应正则匹配：r'/.*?/'   r'\[.*?\]'  r'{.*?}'
```

## 如何将txt文档转换为csv文档？
比如：将 my_words.txt 转换为： my_word.txt.csv

```
python process_word_list_from_txt.py my_words/my_word.txt
```
process_word_list_from_txt.py : 转换脚本
my_words/my_word.txt ： txt文档待处理文档路径

这里采用相对 `process_word_list_from_txt.py` 的路径

**输出**

在 my_words/ 路径下生成：my_word.txt.csv

## 如果txt更新了，顺序版csv如何更新？
如果 my_words.txt 更新了，如果my_word.txt.csv 也要更新
在命令行末尾 使用`--update` 或者`-update` 或者`-u`
```
python process_word_list_from_txt.py my_words/my_word.txt -u
```

## 为什么要生成csv文件，以及csv实现效果是什么？
csv 文件可以利用python库来处理，生成更有意思的文档。

csv 的格式如下：
每行4列：行号,单词,音标,中文含义

使用逗号隔开
```
行号,单词,音标,中文含义
0,apple ,//, 苹果
1,shuffle ,//, 打乱
2,test ,//, 测试
3,companion ,/kəmˈpænɪən/, n. 共事者；同伴
4,rig       ,/rɪg/,        vt. 操纵，垄断  n. 船桅（或船帆等）的装置；成套器械
5,input*    ,/ˈɪnput/,     n. 投入，输入；输入的数据  vt. 把……输入计算机
6,merely*   ,[ˈmiəli],     ad. 仅仅，只不过
7,impart    ,/ɪmˈpɑːt/,    vt. 给予，赋予；传授；告知，透露
...
```

## 乱序的csv词汇表有什么用？如何生产md文档？

它处理顺序csv词汇表后产生的中间文件，将用于生成以5个一组的md文档？

使用`get_five_words_group_from_csv.py`脚本
```
python get_five_words_group_from_csv.py my_words/my_word.txt.csv 
```

## 当txt、csv都更新了，如何更新md文档？
在命令行末尾 使用`--update` 或者`-update` 或者`-u`
```
python get_five_words_group_from_csv.py my_words/my_word.txt.csv  -u
```
最终将输出三个文件：
```
乱序版csv文档: my_words/new_shuffle_my_word.txt.csv
分组的md文档: my_words/new_shuffle_my_word.txt.csv.md
反序分组的md文档: my_words/reversed_new_shuffle_my_word.txt.csv.md
```

## 如何根据txt文档重新生成新的csv与对应的md文档？

删除所有的csv、md文件，然后重新从txt生成csv，再从乱序的csv生程md
```
rm my_words/*.csv my_words/*.md
python process_word_list_from_txt.py my_words/my_word.txt
python get_five_words_group_from_csv.py my_words/my_word.txt.csv

```
## 当txt单词表更新后，csv与md会如何改变？
- 在txt文本更新，使用更新命令，会更新已有的csv、乱序csv、md文档
- 如果是在txt末尾添加单词，那么csv文档、乱序csv、md文档也会在末尾更新。
- 如果是在txt中间添加单词，csv文档中不仅仅添加更新的单词，单词后面的所有行的行号也会更改，那么csv、乱序csv末尾会产生更新外，所有改变行号的行在csv文档中也会有所更新。
- csv、乱序csv所以的单词是唯一的，如果在txt 添加一个重复的单词，那么csv、乱序csv文档会进行去重，保留最新添加的那行，最后的md也不会包含重复的单词

## 如何获取雅思txt单词表？

https://github.com/fanhongtao/IELTS.git

## 获得了随机的5个单词，然后用来做什么？

写个程序调openapi接口将5个单词，丢给chatgpt, 让它编写故事，有助于记忆单词也能学习语境，举个例子：

提问：
```
Write a story of 60 words using the following words. Each time when a word from the following list is used, insert after the word its meaning in Chinese. I will give you an example after EG. Follow the example:

dump*  vt. 倾卸，倾倒  n. 垃圾场
manufacture  vt. 大量制造，成批生产  n. 大量制造；工业品
impede*  vt. 阻碍，妨碍
inadequate*  a. 不充分的；不适当的
rural*  a. 农村的，乡村的

EG
This sentence (句子) is an example.
```

输出：

In rural (农村的) areas, the inadequate (不充分的) access to transportation can impede (阻碍) commerce. A local entrepreneur sought to change this by manufacturing (大量制造) affordable bicycles designed for rural terrain. The bikes were a hit, and soon the entrepreneur was able to expand their operation to include other products. The dump (垃圾场) that once marred the landscape was replaced with a thriving factory.


