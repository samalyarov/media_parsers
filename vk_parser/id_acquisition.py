# Importing libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl
import re
import time

driver = webdriver.Chrome()

driver.get('https://regvk.com/id/')

groups_excel = pd.read_excel('vk_groups.xlsx')
groups_links = groups_excel['Full link'].tolist()
groups_ids = []

for group in groups_links:
    elem = driver.find_element(By.ID, 'enter')
    button = driver.find_element(By.XPATH, '/html/body/div[1]/div/form/div[2]/p/button')

    elem.click()
    elem.send_keys(group)

    button.click()
    try:
        result = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/table/tbody/tr[2]/td')
        text = result.text
        group_id = re.sub('\D', '', text)
        groups_ids.append(group_id) 
    except:
        groups_ids.append('ERROR!')
    

driver.close()

workbook = openpyxl.load_workbook('vk_groups.xlsx')
worksheet = workbook.get_sheet_by_name('Sheet1')

# Start with this cell:
row = 2
column = 3

for i in range(len(groups_ids)):
    current_cell = worksheet.cell(row=row, column=column)
    current_cell.value = groups_ids[i]
    row += 1

workbook.save('vk_groups_final.xlsx')
