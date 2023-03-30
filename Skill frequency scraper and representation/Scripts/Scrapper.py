from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from matplotlib import pyplot as plt      # Remove if pie plot not wanted , Pie plot will still not shown untill user gives 1 as inpur after entering designation


def scrap(url, file, load_time,pie):
    # Specify the path of chromedriver.exe
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(load_time)
    soup = BeautifulSoup(driver.page_source, 'html5lib')


    driver.close()
    entries = 256  # Number of Job entries you want to fetch,set 256 by default to just have a limit.
    pages = 20  # Number of pages you want to fetch ,set 20 by default as specified in assignment pdf.
    results = soup.find(class_='list')
    jobs = results.find_all('article', class_='jobTuple bgWhite br4 mb-8')


    # Code variables declaration and initiation
    count = 0
    skillslist = []
    skillcount = {}
    keycol=[]
    value=[]


    # DataFrame initiation
    df = pd.DataFrame(columns=['Company', 'Description', 'Experience', 'Locality', 'Salary', 'Skills'])
    print("____________________________________PLEASE WAIT______________________________________-")
    for i in range(0, pages):
        if count < 20 and count != 0:
            time.sleep(3)
        if count > entries - 1:  # Limit number of entries to integer entries
            break
        for job in jobs:
            if count > entries - 1:  # Limit number of entries to integer entries
                break


            # Company Name
            company = job.find('a', class_='subTitle ellipsis fleft')

            # Job Description
            des = job.find("div", class_="job-description fs12 grey-text")
            if des is None:
                continue
            else:
                description = des.text


            # Experience in Years
            exp_l = job.find('li', class_='fleft grey-text br2 placeHolderLi experience')
            if exp_l is not None:
                exp = exp_l.find('span', class_='ellipsis fleft fs12 lh16')
            else:
                continue
            if exp is None:
                continue
            else:
                experience = exp.text


            # Locality
            loc_l = job.find('li', class_='fleft grey-text br2 placeHolderLi location')
            if loc_l is None:
                continue
            else:
                loc = loc_l.find('span', class_='ellipsis fleft fs12 lh16')
            if loc is None:
                continue
            else:
                location = loc.text


            # Salary
            sal_l = job.find('li', class_='fleft grey-text br2 placeHolderLi salary')
            if sal_l is None:
                continue
            else:
                sal = sal_l.find('span', class_='ellipsis fleft fs12 lh16')
            if sal is None:
                continue
            else:
                salary = sal.text


            # Skills
            skills = []
            skillSet = job.find('ul', class_='tags has-description')
            for skill in skillSet.find_all('li', class_='fleft fs12 grey-text lh16 dot'):
                key = skill.text
                skills.append(key)

                # Skill frequency list
                if skillcount.get(key) is not None:
                    skillcount[key] = skillcount[key] + 1
                else:
                    skillcount[key] = 1
                skillslist.append(skills)


            #  Insert values in dataframe
            df = df.append(
                {'Company': company.text, 'Description': description,
                 'Experience': experience, 'Locality': location, 'Salary': salary, 'Skills': skills}, ignore_index=True)
            count += 1


    # print(df.head(20))
    if df.empty:
        print("Data cannot be fetch Try again.")
        scrap(url, file, 10)
    else:
        df.to_excel(file + "Excel Files/data.xlsx", index=False)
        print("Success")
        print("job profiles and their Key-Skill data saved in data.xlsx")


    sorted_dict = dict(sorted(skillcount.items(), key=lambda item: item[1], reverse=True))
    df2 = pd.DataFrame(columns=['Skill', 'Frequency'])
    for key in sorted_dict:
        keycol.append(key)
        value.append(sorted_dict[key])


    freq = pd.DataFrame({'Skill': keycol, 'Frequency' : value})
    # print(freq)

    #___________________________________Add below code and above import 'matplotlib' to excecute pie plot_______________________________
    if pie:
        plt.pie(value[0: 9: 1], explode = (0.1, 0, 0, 0, 0, 0, 0, 0, 0), labels = keycol[0: 9: 1],autopct = "%0.1f %% ", shadow = True)
        plt.savefig('Skill_Frequency_pie.png')
        plt.show()
    
    #___________________________________pie plot code ends here_________________________________________________________________________________________


    
    freq.to_excel(file + "Excel Files/Skill Frequency.xlsx")
    print("Success")
    print("Key-Skill frequency saved in Skill Frequency.xlsx")
    time.sleep(2)

    # Use this line for xls file. Warning : xls is no longer supported by python except pandas.
    # df.to_excel("C:/Users/Anand/OneDrive/Desktop/Git/Web Scrapper/" +data.xls, index=False)
