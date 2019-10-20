from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver


def link_func():
    browser = webdriver.Chrome(executable_path='C:/Python37/chromedriver.exe')
    browser.get('https://bombayhighcourt.nic.in/case_query.php')
    from_date = browser.find_elements_by_id('demo1')
    to_date = browser.find_elements_by_id('demo2')
    browser.execute_script("document.getElementById('demo1').value='18-10-2018';", from_date);
    browser.execute_script("document.getElementById('demo2').value='18-10-2019';", to_date);

    list_case_by_type = browser.find_element_by_name('submit11')
    list_case_by_type.click()
    page_o = browser.page_source
    page_soup = soup(page_o, "html.parser")
    browser.quit()
    return page_soup
link_func()


arr = []
page_s = link_func()
containers = page_s.findAll("font", {"color": "green"})
for p in range(0, len(containers)):
    link = "https://bombayhighcourt.nic.in/" + containers[p].find("a")["href"]
    x = requests.get(link)
    if x == "https://bombayhighcourt.nic.in/index.html":
        s = link_func()
        containers = s.findAll("font", {"color": "green"})
        p = p - 1
    else:
        arr.append(containers[p].text[1:])
        name = ""
        for a in containers[p].text[1:].split('/'):
            name += str(a) + "_"
        file_name = name + ".html"
        f = open(file_name, "w+")
        f.write(str(x.content))
        f.close()