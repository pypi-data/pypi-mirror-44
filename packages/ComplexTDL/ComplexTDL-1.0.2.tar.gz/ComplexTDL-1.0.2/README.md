# ComplexTDL

中文版见 REAMD_CN.md

A Python-based to do list tool that you can use to:

* Sort out your tasks during a certain period of time
* Generating weekly and monthly work report
* Do some simple team task management

## The main features include

* Support basic information such as task title, task status, task time, etc.
* Supports a variety of advanced settings:
  * Support customizing the modules (list)
  * Supporting Tasks that is across many days
  * Support priority customization
  * Supporting subtasks and related logic
  * Support assigning the task to different people
* Convenient operation
  * Keyboard operation without mouse
  * Batch operations
* Support task list export and report generation
  * support filtering task as you wish
  * custom time
  * support many export formats, including markdown list or form, excel etc.
* Based on TinyDB, so no DB software is needed

This project does not provide a graphical interface for the time being. It is recommended to use the following methods:

* Combining efficiency tool like Alfred
* Run with Django
* Direct Use through the command line 
* Make your own graphical interface

## Install

You can use pip to install:

```shell
pip install ComplexTDL
```

Or you can clone from git, you need to install the following dependency:

```shell
pip install openpyxl, pyperclip, tinydb
```

## Quick Start

The project provides command-line tools to support direct command-line use

```shell
# Complete some configuration
tdl_set -h # View related configuration assistance

# Add or edit tasks
tdl_modify -h # View the help related to adding or editing tasks

# View tasks or generate reports
tdl_report -h # View help related to viewing tasks or generating reports
```

## API Description

You can import the libraries and writing your own applications.
You can also see the source files for reference.

### ComplexTDL.Settings Module

Some settings for ComplexTDL.

| Function | Description|
|---|---|
|`ShowJobModules()`|Display the module (list) information|
|`SetTaskNumber(number)`|Set the starting number of the task list|

### ComplexTDL.Task Module

For insert, update, delete tasks.

| Function | Description|
|---|---|
|`DeleteRecord(formData)`|formData is a dictionary; formData['no'] is the task number to be deleted|
|UpdateData(formDataF)|Insert or update a task, formDataF is a dictionary, refer to the analysis of the task structure below|

'''
the structure of task

no Number
mo Module / Group / List
ti Title
de Description and Update
st Start time
en End time or Check time
ra Completion rate, -1 for pause
pa Parent task number
pe person in charge
pr priority
'''

### ComplexTDL.Report Module

Used to generate task lists and reports

| Function | Description|
|---|---|
|Report(period = 'this week', range = 'todo', person = 'me', deadline = False, conditions = None, detail = 'some', sort = 'module')|To generate a specific report, refer to the help information in the source file|
|Search(args)|Custom conditions to filter and query the task, see the source file for help information|
|GenerateMD(taskList, format = 'md list')|Generate md and copy it to the clipboard, the format can be 'md list' (list), 'md list no' (list with task number), 'md table' (table)|
|GenerateExcel(taskList, filePath=os.curdir, fileName='report', showParent=False)|Generates excel tables, filePath for the store path, fileName for the fileName, and use showParent to determine whether to display the parent task number|