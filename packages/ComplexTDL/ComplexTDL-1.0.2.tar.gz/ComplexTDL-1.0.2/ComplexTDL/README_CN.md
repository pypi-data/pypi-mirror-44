# ComplexTDL 复杂清单

一个基于 Python 的 to do list 工具，你可以用它：

* 梳理自己某段时间内的任务
* 生成工作周报、月报
* 做一些简单的团队任务管理


## 主要特点包括

* 支持任务标题、任务状态、任务时间等基本信息
* 支持多种高级设置：
  * 支持多个模块（清单）
  * 支持跨天的任务
  * 支持优先级自定义
  * 支持子任务及相关逻辑
  * 支持分配人配置
* 便捷操作
  * 键盘操作，无需鼠标
  * 支持任务的批量操作
* 支持任务清单导出及报表生成
  * 支持自定义任务过滤
  * 自定义时间段
  * 支持多种导出格式，包括 markdown 格式的列表或表格，excel 表格等
* 基于 TinyDB，无需安装额外数据库

这个项目暂时没有提供图形界面，建议使用方法：

* 结合 alfred 等效率工具使用
* 放在 Django 上运行
* 命令行直接使用
* 自己做一个图形化界面

## 快速使用

项目提供了命令行工具，支持命令行直接使用.
你需要安装以下依赖库

```shell
pip install openpyxl, pyperclip, tinydb
```

```shell
# 完成一些配置
$ tdl_set -h # 查看相关配置的相关帮助

# 添加或编辑任务
$ tdl_modify -h # 查看添加或编辑任务的相关帮助

# 查看任务或生成报表
$ tdl_report -h # 查看查看任务或生成报表的相关帮助
```

## API 说明

您也可以通过引入库并自行编写自己的应用，可以直接参考源文件

### ComplexTDL.Settings 模块

用于程序的一些设置。

|函数|说明|
|---|---|
|`ShowJobModules()`|显示当前的模块（清单）信息|
|`SetTaskNumber(number)`|设置任务清单的起始编号|

### ComplexTDL.Task 模块

用于插入、更新、删除任务。

|函数|说明|
|---|---|
|`DeleteRecord(formData)`|删除某个任务及其子任务，formData 是一个字典，formData['no'] 即待删除的任务编号|
|UpdateData(formDataF)|插入或更新某个任务，formDataF 是一个字典，可以参考下方对任务结构的分析|

'''
the structure of task

no 任务编号
mo 模块 / 清单 / 分组
ti 任务标题
de 描述、详情
st 开始时间
en 结束时间
ra 完成度，-1 表示暂停
pa 父任务的任务编码
pe 任务的分配人
pr 优先级
'''

### ComplexTDL.Report 模块

用于生成任务清单、生成报表

|函数|说明|
|---|---|
|Report(period = 'this week', range = 'todo', person = 'me', deadline = False, conditions = None, detail = 'some', sort = 'module')|生成特定的报表，可以参考源文件的帮助信息|
|Search(args)|自定义条件来进行任务过滤、查询，具体预发参见源文件中的帮助信息|
|GenerateMD(taskList, format = 'md list')|根据 taskList 生成 markdown 的报表并复制到剪切板，format 可以为 'md list'（列表），'md list no'（带有任务编号的列表），'md table'（表格）|
|GenerateExcel(taskList, filePath=os.curdir, fileName='report', showParent=False)|生成 excel 表格，filePath 为存放路径，fileName 为文件名，showParent 来确定是否显示父任务编号|