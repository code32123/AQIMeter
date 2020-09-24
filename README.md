This file has information on my AQI program! All the source code can be found on [Github][1].
If you find a bug, reports should to [Github Issues][3]. If you need me, the best way to reach me is at [Github][4].

---

First order of business, below is recommended setup:
1.	Make a folder, wherever you want, and save the .exe file there. The exe will generate files it needs when it is run.
2.	Hold "Alt" and drag the .exe to your desktop. It should say "Create link in Desktop"\
3.	Done! The exe will generate everthing it needs wherever you put it.
Having trouble? A better guide to settings up shortcuts is here: [How To Geek][2]

---

Next:
To add a link other than those on the list of presets:
1.  First, go to [AirNow.gov](https://www.airnow.gov/)
2.  Enter your location into the textbox
3.  After the website displays an AQI for your area, copy the link (Usually somthing like www.airnow.gov/?city=&state=&country=USA)
4.  Paste this link in the text box of the AQI program, and press done. This saves the linkk as the current url to search.

---

Finally:
Here is a list of files this program will generate. As there is not an installation process, neither is their an uninstallation process.\
If you want to remove the application, you will need to remove the .exe and the following files and folders
| File or Folder | Description |
| -------------- | ----------- |
| ```./Logs``` | A folder for storing log files |
| ```./Logs/AQILogs.txt``` | A list of all measurements. Records them newest last. |
| ```./Logs/LogX.txt``` | where "X" is a number from 1 to 99. Logs of recent activity. |
| ```./settings.json``` | A list of settings like the link to read from, the foreground color, and the background color. |

[1]: https://github.com/code32123/AQIMeter
[2]: https://www.howtogeek.com/436615/how-to-create-desktop-shortcuts-on-windows-10-the-easy-way/
[3]: https://github.com/code32123/AQIMeter/issues
[4]: https://github.com/code32123
