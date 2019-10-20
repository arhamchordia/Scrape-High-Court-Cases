from bs4 import BeautifulSoup as soup
import requests
from selenium import webdriver


def link_func():
    # starts webdriver
    browser = webdriver.Chrome(executable_path='C:/Python37/chromedriver.exe')
    # opens given link in chrome
    browser.get('https://bombayhighcourt.nic.in/case_query.php')
    # finds text box for start date
    from_date = browser.find_elements_by_id('demo1')
    # finds text box for end date
    to_date = browser.find_elements_by_id('demo2')
    browser.execute_script("document.getElementById('demo1').value='18-10-2018';", from_date);
    browser.execute_script("document.getElementById('demo2').value='18-10-2019';", to_date);
    # finds button to search according to the given date range
    list_case_by_type = browser.find_element_by_name('submit11')
    # clicks the button to proceed further
    list_case_by_type.click()
    # gets page's source code
    page_o = browser.page_source
    page_soup = soup(page_o, "html.parser")
    browser.quit()
    return page_soup
link_func()

# to store case tags
arr = []
page_s = link_func()
# containers contain all the case tags and their links
containers = page_s.findAll("font", {"color": "green"})
for p in range(0, len(containers)):
    # appending link to create an accessible link for requests
    # as containers contains only auth keys
    link = "https://bombayhighcourt.nic.in/" + containers[p].find("a")["href"]
    # makes request to get HTML of links
    x = requests.get(link)
    # this if condition checks if auth key has expired or not
    if x == "https://bombayhighcourt.nic.in/index.html":
        s = link_func()
        # as the auth key has expired, restart containers
        containers = s.findAll("font", {"color": "green"})
        # shifts index back to previous position as we have not accessed that case yet
        p = p - 1
    # this condition acts whenever the auth key is active
    else:
        # array is appended to store case tags
        arr.append(containers[p].text[1:])
        name = ""
        # filename is created to identify particular case's HTML
        for a in containers[p].text[1:].split('/'):
            name += str(a) + "_"
        # new HTML file is created with current page's HTML
        file_name = name + ".html"
        f = open(file_name, "w+")
        f.write(str(x.content))
        f.close()
