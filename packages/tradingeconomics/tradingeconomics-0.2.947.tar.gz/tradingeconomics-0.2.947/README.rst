=====================
Trading Economics API
=====================

Install Python
===============
If you don’t have a copy of Python installed on your computer, you can get it from:

 - `https://www.python.org/downloads/ <http://>`_


It's recomended to install pip, it is a package management system used to manage software packages written in Python. 

You can find all information in: 

 - `https://packaging.python.org/installing/ <http://>`_

In Python (command line) 
========================


```python
pip install tradingeconomics
```

 - There is a possibility to install package using easy_install

```python
easy_install https://pypi.python.org/packages/4c/b4/e2e2a9668be305a42c0644b3eb5d4d1034ae062653ef737d7e80c1423d28/tradingeconomics-0.2.X.tar.gz
```
*Where 'X' type the last version number.*

 -  As alternative you can download the package from: 

`https://pypi.python.org/pypi/tradingeconomics <http://>`_ , and then follow the installation instructions for `Python 3 -https://docs.python.org/3/install/) <http://>`_
 or `Python 2 - https://docs.python.org/2/install/ <http://>`_

 -  Another method is to download the GitHub repo: `https://github.com/ieconomics/open-api/tree/master/python <http://>`_

 and place it in your Python library folder.  

Starting the package
========================

In command window type:

```python
import tradingeconomics as te
te.login('APIkey')
```

 - If you don't have APIkey just left empty space in brackets. 
 - **Note:** Without APIkey datasets will default to returning sample data.
 - Results are available in differente formats, such as : JSON, pandas.DataFrame or dictionary.

**For example:**

To get calendar data for specific country, in data frame format, just type:


```python
te.getCalendarData(country = 'Italy', output_type = 'df')
```