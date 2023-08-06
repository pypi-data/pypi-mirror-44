Power BI refresher manualy
======
Script for automation of refreshing Power BI workbooks.  Built on Python 3.6 and pywinauto.

Installation
------
Install using `pip`

```
pip install powerbirefreshmanual
pip install pypiwin32
```

Usage
-----
```
powerbirefreshmanual <WORKBOOK> [-workspace <WORKSPACE>]

where <WORKBOOK> is path to .pbix file
      <WORKSPACE> is name of online Power BI service work space to publish in. Default is My workspace
```

Scheduling in Windows Task Scheduler
-----
Please keep in mind that this script uses GUI of Power BI Desktop and it needs that a user is logged in Windows session. You should also deactivate lock screen time. Ideally you should schedule the script on a computer where the GUI is not used to not interfere the scripting, for example dedicated Virtual Machine.

1. Open Task Scheduler
2. Click Create Basic Task
3. Fill a Name and click Next
4. Set a trigger and click Next
5. Pick Start a program as an action and click Next
6. in Program/script type absolute path to powerbirefreshmanual.exe in your scripts folder in Python installation path (for example "C:\ProgramData\Anaconda3\Scripts\powerbirefreshmanual.exe")
   in Arguments type file name of the workbook (for example "sample.pbix")   
   in Start in type absolute path workbook (for example "C:\workbooks\")
7. Confirm and Finish