from tkinter.tix import Select
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select

from os import listdir
import os.path
import shutil
import time

def get_export_files(path: str):

    os.chdir(path)
    dir_path = os.path.join(path, 'export_data')

    # create folder to save all downloaded text files
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    files = [ file for file in listdir(path) if os.path.isfile(os.path.join(path, file)) ]

    # open the export trading page
    url = 'https://www.trademap.org/Country_SelProduct.aspx?nvpm=1%7c%7c%7c%7c%7cTOTAL%7c%7c%7c2%7c1%7c1%7c2%7c1%7c1%7c2%7c1%7c1%7c1'
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    
    xpath_country_dropdown = '//*[@id="ctl00_NavigationControl_DropDownList_Country"]'
    country_dropdown = Select(WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, xpath_country_dropdown))))
    options = [ opt.text for opt in country_dropdown.options ]

    # go through all elements in country dropdown list
    for option in options:

        # select new option from dropdown list
        country_dropdown = Select(WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, xpath_country_dropdown))))
        country_dropdown.select_by_visible_text(option)

        # download current text file (Hong Kong does not have download button)
        try:
            xpath_download_button = '//*[@id="ctl00_PageContent_GridViewPanelControl_ImageButton_Text"]'
            download_button = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, xpath_download_button)))
            download_button.click()
        except:
            continue

        # wait for file to be downloaded
        time.sleep(0.5)

        # rename and move downloaded file with right name in created folder
        tmp_files = [ file for file in listdir(path) if os.path.isfile(os.path.join(path, file)) ]
        file_name = list(set(tmp_files) - set(files))[0]
        shutil.move(os.path.join(path, file_name), os.path.join(dir_path, option + '.txt'))

    time.sleep(2)
    driver.close()