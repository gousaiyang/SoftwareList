# SoftwareList

## Introduction
This is a software listing and updating assistant for Windows, which can create 3 kinds of **software lists** based on HTML.

## Functionalities
### Full List
Usage: Run `SLGetFullSoftwareList.py`

This will list all the Win32 applications (both system-wide and user-wide) installed in the current Windows system (by reading the registry). You can use the list to track changes of software on your computer.

### Main List
Usage: Run `SLGenerateMainSoftwareList.py`

This will generate a list from `MainSoftwareList.json`, which is configured manually by the user. From the full list, you can select important software items and put them into the main list (and you can assign priority values to them). The main list will be of great help when you get a new computer and want to install software that you had on the old machine.

### Update list
Usage: Run `SLCheckUpdate.py`

This will check updates for software items in the user-configured file `CheckUpdateList.json` and generate a list of software items that needs update. Method of retrieving update information of software (i.e. URL of their official websites and parsing rules) should be configured in `SLSoftwareInfo.py`.

### Themes
The HTML-based lists support several themes which you can configure in `Config.json`:
- Green
- Blue
- Pink
- Purple
- Random (Randomly choose one of the above)

### Other Utilities
- Run `SLCreateDailyUpdateTask.py` to create a daily task for software updating.
- Run `SLDeleteDailyUpdateTask.py` to delete the update task.
- Run `SLClearOldLists.py` to clear old software list of the 3 kind, leaving only the newest ones respectively.

## Environment and Dependencies
### Environment
- OS: Windows 7 and higher versions
- Python 3, with modules: `requests`, `BeautifulSoup`

### Front-end Dependencies (Using CDN)
- Bootstrap
- Font Awesome
- jQuery
- DataTables

## Further Notes
- [Chocolatey](https://chocolatey.org/) is a package manager for Windows, which can facilitate automation of software updates. But not all applications are published on Chocolatey currently.
- UWP applications are automatically updated by Microsoft Store, but many of the applications we use are still legacy Win32 applications. In the future, more applications may become UWPs, but those who need a flexible command of system resources, including some tools for developers, may remain Win32-based.
