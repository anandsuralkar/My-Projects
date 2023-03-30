import Scrapper
import Format

print("Enter job designation to search jobs for : ")
designation = input()

# pie plot user input is 1 then pie plot will be shown other wise pyplot will not be shown
pie =False
if input("Press enter again to skip pie plot of Key-Skill frequency or press 1 and enter to show pie plot") ==  "1":
    pie = True
#_________________________________________________________________________________________


url = "https://www.naukri.com/" + Format.format_designation(designation, False) + "-jobs"
file = "C:/Users/Anand/OneDrive/Desktop/Git/Web Scrapper/"   # Must give path of project root directory and must end with slash'/'

Scrapper.scrap(url, file, 5, pie)  # Third parameter is load time ie. how long to wait before parsing HTML after opening link

"""
If theres no output even after retry try increasing third parameter in above function call from 5 to 10 or more,
Higher load_time is recommended for slower internet Load time for page recommended bigger value if internet is slow
Also increase same parameter in Scrapper.py line 91 if needed.

Chromedriver installation is recommended for the script to run
Use pip install chromedriver
Also make sure then chrome driver is added to the path environment variable
For help about Chromedriver setup refer this 

https://cppsecrets.com/users/11429798104105115104101107117115104119971049754494864103109971051084699111109/Python-chromedriver-executable-needs-to-be-in-PATH.php

"""