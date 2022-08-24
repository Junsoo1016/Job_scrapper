from requests import get
from bs4 import BeautifulSoup

def get_page_count(keyword):
    base_url = "https://www.indeed.com/jobs?q="
    response = get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request page")
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        pagination = soup.find('ul', class_="pagination-list")
        if pagination == None:
            return 1
        pages= pagination.find_all('li', recursive=False)
        count = len(pages)
        if count >= 5:
            return 5
        else:
            return count


def extract_indeed_jobs(keyword):

    pages = get_page_count(keyword)
    print("Found", pages, "pages")
    results = []
    for page in range(pages):
        base_url = "https://www.indeed.com/jobs?q="
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        print("requesting", final_url)
        response = get(final_url)

        if response.status_code != 200:
            print("Can't request page")
        else:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_list = soup.find("ul", class_="jobsearch-ResultsList")
            jobs = job_list.find_all('li', recursive=False)
            for job in jobs:
                zone = job.find('div', class_='mosaic-zone')
                if zone == None:
                    h2 = job.find('h2', class_="jobTitle")
                    anchor = job.select_one("h2 a")
                    title = anchor['aria-label']
                    link = anchor['href']
                    company = job.find("span", class_='companyName')
                    location = job.find('div', class_='companyLocation')
                    job_data = {
                        'link': f'https://indeed.com{link}',
                        'company': company.string.replace(",", " "),
                        'location': location.string.replace(",", " "),
                        'position': title.replace(",", " ")
                    }
                    print(job_data)
                    results.append(job_data)
    return results
