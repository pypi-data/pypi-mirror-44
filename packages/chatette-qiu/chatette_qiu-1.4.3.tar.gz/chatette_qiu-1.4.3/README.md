# Chatette-qiu
Chatito是用于创建聊天机器人训练数据集的自然语言生成工具
原始代码是参考https://github.com/SimGus/Chatette实现

## Intent of this project
这个项目的目的和初衷，是为了更好的适配自己的需求。
比如：input的时候只能传一个文件，不支持传目录



## Quick Install
```
pip install chatette_qiu
生成训练数据命令：
        python -m chatete_qiu input_file_or_folder -o output_path


        input_file_or_folder  输入的chatette模板文件路劲或者文件夹
        output_path           结果输出目录