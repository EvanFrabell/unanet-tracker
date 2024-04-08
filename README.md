# Unanet Time Tracker
- Designed to log typical work days under your project code without the need to manually track your time every day.
- Script will log your work hours every workday, create a new timesheet, and submit your timesheet on the correct day.
- PTO and holidays will still need to be entered manually.

*Script hasn't been fully tested.  You will need to have a cell phone setup for multi-authentication (no token is generated at this time).*

### Setup Script

1. Download & Install Python: https://www.python.org/downloads/
2. Download or Clone repository: https://github.com/EvanFrabell/unanet-tracker
   - Click Code -> Download ZIP
   - Unzip
3. Open Command Line (CMD) & install python packages
    - Windows + r -> cmd
    - Navigate to unanet-tracker directory in CMD: 'cd downloads\unanet-tracker'
    - Enter command in CMD: 'pip install -r requirements.txt'
4. In the credentials.yaml file enter your username and password for your SharePoint login
    - Quotation marks not needed
    - username: jDoe@Sierra7.com
    - password: asdfjAEFADFas43!!
    - Save .yaml file
5. Test out the script
    - You should be able to double-click the main.py file to get it to run
    - If not, type into CMD 'python main.py'
    - You should receive a call from Microsoft (answer + press #) and hours should be clocked in Unanet after the script finishes.


### Setup Task Scheduler

1. Open scheduler.bat in a text editor (notepad)
    - In the 1st set of parentheses replace the installation path + interpreter (.exe) to Python on your pc (likely the same what is already in the .bat file)
    - In the 2nd set of parentheses replace the full path to your main.py file
2. Test scheduler by double-clicking scheduler.bat.  The script should behave the same in step 5 above (there will likely be an error when saving time sheet).
3. Checkout Unanet manually to ensure timesheet is correct still.
4. Setup Windows Task Scheduler
    - Press Windows + s, then type 'task scheduler', press enter
    - Click 'Create Task...'
    - General tab:
      - Name: UnaNetClockIn
      - Configure for: Windows 10
    - Triggers tab:
      - Click New...
      - Select Daily
      - Start: Tomorrow's date || Time you would like script to run every day
      - Select Stop task if it... Select 1 hour
    - Actions tab:
      - Click New...
      - Place full path to scheduler.bat file in unanet-tracker folder ("C:\Users\yourPCName\downloads\unanet-tracker\scheduler.bat") into Program/script: input.  Your path will be slightly different from mine.
      - Click OK

#### *You should be set from here, but feel free to message me about any bugs or confusion.*

