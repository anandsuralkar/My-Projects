
###################################        local installation       ####################################
Chrome browser must be installed as chromedriver is used in the script

For global installation of dependencies use following method:-
first open the project folder directory and then type cmd into adress bar to open command prompt in current directory or just use cd command to get into current directory
Then run following command:-

pip install -r requirements.txt

After that add local path to chromedriver root folder in path environment variable
refer link provided at the end if needed.

To start the script run "main.py"
Enter the job designation you want to fetch Key-Skills for and press enter.
The fetched Key-Skills data will be stored in data.xlsx.


###################################       Setting up project in pycharm       ####################################
If chromedriver has issues
Use pycharm IDE because webdriver has bug where it asks for chromedriver.exe and doesnt accept it even if u give path with local environment,so in that case pycharm is recommended.
in pycharm go to file->settings->Project->Python Interpreter  click "+" button to add following modules.

install following modules:-

pandas
time
selenium
bs4
chromedriver
matplotlib (optional for pie plot only)

if any of above modules doesn't work just install them using command promt and pip install method.

For global installation of dependencies use following method:-
first open the project folder directory and then type cmd into adress bar to open command prompt in current directory or just use cd command to get into current directory

Then run following command:-

pip install -r requrements.txt
Its recommended to use pycharm IDE because webdriver has problems with local environment.

After that add local path to chromedriver root folder in path environment variable
refer link provided at the end if needed.

###################################       Running script       ####################################
To start the script run "main.py"
Enter the job designation you want to fetch Key-Skills for and press enter.
The fetched Key-Skills data will be stored in data.xlsx.

Furthermore, frequency of each Key-Skill is stored in Skill Frequency.xlsx in the descending order ie. most frequent Key-Skill at the top and least one at the bottom.



###################################       Support and contact       ####################################
For queries email me at anandsuralkar36@gmail.com.
Or contact me on 8668237882
Whatsapp :- 8668237882
Github :- https://github.com/anandsuralkar/Computer-science.git.
For this webscrapper project files open Web Scrapper folder in my git repository.

If issues occur regarding webdriver refer this.
Some versions of webdriver are not compatible with most pandas version and also
https://cppsecrets.com/users/11429798104105115104101107117115104119971049754494864103109971051084699111109/Python-chromedriver-executable-needs-to-be-in-PATH.php


###################################      Code Structure       ####################################
Working logic:-

Selenium webdriver and beautiful soup are used for data scrapping from Naukri.com job searching website.
the data is then processed accordingly and manages/saved into data.xlsx for all provided(defalault 20) number of job profiles including 'Company', 'Description', 'Experience', 'Locality', 'Salary', 'Skills'.
The frequency count of each Key-Skill is saved in SKill Frequency.xlsx

for detailed information refer to main.py and Scrapper.py files comments are given for necessary detailed information.


There are three python script made specailly for more readability and code management.
main.py is the starup script it will call function from Format.py script to make properly formatted URL according to the designation keywords.

In Format.py format_designation function will return URL .
main function will then call scrap function in Scrapper.py script
Scrapper will Scrap the Key-Skill and other required data from Top 20 job results from the designation provided by user.
Scrap function will run by default 5 number or pages but will stop as soon as 20 entries collected, both pages number and entries number can be edited in scrap function itself .

In Scrapper Script Remove import matplotlib as plt and at the Delete or comment out pie plot code to get rid of pie plot

###################################      Alternative method and comments      ####################################
I actucally made the whole project using 'requests' module and did all fetching data myself but unfortunately 'requests' module doesn't support scrapping javascript embeded data in page instead it just fetches the raw html data only.
Thus it was not possible to get most of the data because it was inside javascript file and not HTML itself.
So I had to scrap the whole project and start again using selenium and chromedriver which was buggy but finally ran  successfully but setting up was lengthy process.
Although if required I can provide the 'request' module based which doesnt actually work on naukri.com because of separate javascript files and data embedded in them, but I will implement it in any other job website .
I have also tried glassdoor ,Indeed.com but those websites dont have Key-Skills requrement given, so those were not usable for this project but for any other data scrapping data like job description, job posting date etc. those sites could be scrapped and using 'request' only because they dont have Javascript files embedded data inside it but data is available on HTML itself.