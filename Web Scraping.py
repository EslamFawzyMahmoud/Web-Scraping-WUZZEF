import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

job_title=[]
company_name=[]
location_name=[]
skills=[]
links=[]
salary=[]
responsabilities=[]
date=[]
page_num=0
while True:
    try:
        # use result variable to fetch the url
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_num}")

        # save page content
        src=result.content
        # create soup object to parse content
        soup = BeautifulSoup(src,"lxml")

        page_limit = int(soup.find("strong").text)
        if page_num > page_limit//15:
            print("Page ended, terminate")
            break
        # find the element containing info we need
        # -- job title , skills, company name , location name
        job_titles = soup.find_all("h2",{"class":"css-m604qf"})
        company_names = soup.find_all("a",{"class":"css-17s97q8"})
        location_names = soup.find_all("span",{"class":"css-5wys0k"})
        job_skills = soup.find_all("div",{"class":"css-y4udm8"})
        posted_new= soup.find_all("div",{"class":"css-4c4ojb"})
        posted_old= soup.find_all("div",{"class":"css-do6t5g"})
        posted=[*posted_new,*posted_old]
        # loop over returned lists to extract needed info into other lists
        for i in range(len(job_skills)):
            job_title.append(job_titles[i].text)
            links.append(job_titles[i].find("a").attrs['href'])
            company_name.append(company_names[i].text)
            location_name.append(location_names[i].text)
            skills.append(job_skills[i].text)
            data_text=posted[i].text.strip()
            date.append(data_text)

        page_num+=1
        print(page_num,"Page Switch")
    except:
        print("Error 404 !!")
        break

for link in links:
    result=requests.get(link)
    src = result.content
    soup = BeautifulSoup(src,"lxml")
    salaries = soup.find("div",{"class":"matching-requirement-icon-container","data-toggle":"tooltip","data-placement":"top"})
    salary.append(salaries.text.strip())
    requirement=soup.find("span",{"itemprop":"responsibilities"}).ul
    respon_text = ""
    for li in requirement.find_all("li"):
        respon_text += li.text+" | "
    respon_text=respon_text[:-2]
    responsabilities.append(respon_text)

# create csv file and fill with value
file_list = [job_title , company_name,date , location_name , skills , links , salary , responsabilities]
exported = zip_longest(*file_list)
with open("F:\Wuzzed.csv","w") as myfile:
    wr=csv.writer(myfile)
    wr.writerow(["Job Title","Company Name","Date","Location","Skills","links","Salary","responsibility"])
    wr.writerows(exported)

