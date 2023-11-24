import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re

file_path = './searchterms.xlsx'
df = pd.read_excel(file_path)

driver = webdriver.Chrome()  
wait = WebDriverWait(driver, 10)
url="https://www.amazon.in/"
driver.get(url)
# Function to get type value from a URL
def get_type_value(get_searchterm):
    try:
        wait.until(EC.presence_of_element_located((By.ID,'twotabsearchtextbox')))
        driver.find_element(By.ID,'twotabsearchtextbox').send_keys(get_searchterm)
        wait.until(EC.presence_of_element_located((By.ID,'nav-search-submit-button'))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH,'//span[@class="a-color-state a-text-bold" and contains(text(),"{}")]'.format(get_searchterm))))
        res=driver.find_element(By.XPATH,'//div[@class="a-section a-spacing-small a-spacing-top-small"]/span').get_attribute("innerHTML")
        pattern = re.compile(rf'(\S+)\s{re.escape("results")}')
        match_pattern= pattern.search(res)
        if match_pattern:
            clean_res = match_pattern.group(1)
        else:
            clean_res="no result"
        wait.until(EC.presence_of_element_located((By.ID,'twotabsearchtextbox'))).clear()
        return clean_res
    except Exception as e:
        print(e)
        res="page unavailable"
        return res

# Create a new column 'Type' to store the extracted information
df['Results'] = df['Searchterms'].apply(get_type_value)
df.to_excel("./Results.xlsx",index=False)

driver.quit()
print(df)
