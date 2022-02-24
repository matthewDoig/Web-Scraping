from bs4 import BeautifulSoup
import time
import requests
def find_jobs():
    html_text = requests.get('https://uk.indeed.com/jobs?q=python&l=Bonnyrigg&sort=date&vjk=79b56b0a7deea1aa').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('a', class_=lambda value: value and value.startswith("tapItem fs-unmask result"))
    for index, job in enumerate(jobs):
        publish_date = job.find('span', class_ = 'date').text.replace('Posted', '')
        if 'Just posted' in publish_date:
            company_name = job.find('span', class_ = 'companyName').text
            description = job.find( class_ = 'job-snippet').text
            if 1 == 1:
                with open(f'posts/{index}.txt','w') as f:
                    f.write(f'Company Name : {company_name}\n')
                    f.write(f'Description : {description.strip()}\n')
                print(f'File saved : {index }')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 1)

find_jobs()