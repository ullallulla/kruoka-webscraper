from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv


def get_field_text_if_exists(item, xpath):
    #Extracts a field by Xpath if exists.
   try:
        return item.find_element(By.XPATH, xpath).text
   except NoSuchElementException:
       return ""


URL = 'https://www.k-ruoka.fi/kauppa/tarjoushaku'

driver = webdriver.Chrome('/Users/aleksiojansivu/Downloads/chromedriver')

driver.get(URL)
wait = WebDriverWait(driver, 10)



#Click "Accept cookies"
wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="button primary rounded l accept-button"]'))).click()

#Click change stores
wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="store-and-chain-selector__switch-icon"]'))).click()

#Click All stores
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="store-selector-modal"]/ul/li[3]'))).click()

#Fill name of the store
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="store-selector-modal"]/div[3]/form/div/div/input'))).send_keys('citymarket sello')

#Click Sello
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@class="store-list-item select-store-k-citymarket-espoo-sello"]'))).click()

#wait for the page to load
wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="default-offers"]/h3[1]/a')))

#store get all pseudo-link buttons
pseudo_links = driver.find_elements_by_xpath('//span[@class="pseudo-link"]')

more_buttons = []


for pseudo_link in pseudo_links:
    more_buttons.append(pseudo_link)

#remove sign in pseudo-link buttons
more_buttons.pop(0)

for i in range(len(more_buttons)-1):
    more_buttons[i].click()

# wait for results to load
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'bundle-list-item')))

food_elems = driver.find_elements(By.CLASS_NAME, 'bundle-list-item')


all_products = []
# parse results
for food_elem in food_elems:
    name = get_field_text_if_exists(food_elem, './/div[@class="text-ellipsis text-ellipsis__2-lines product-name"]')
    price = get_field_text_if_exists(food_elem, './/div[@class="product-result-price"]').replace('\n', '')
    #name = food_elem.find_element(By.CLASS_NAME, 'product-result-name-discount').text
    #name = food_elem.find_element(By.XPATH,".//div[@class='text-ellipsis text-ellipsis__2-lines product-name']").text.strip()
    #price = food_elem.find_element(By.CLASS_NAME, 'product-result-price').text.strip()
    all_products.append({
        "name":name,
        "price": price
    })
    print(name)
    print(price)
    print()

driver.quit()

keys = all_products[0].keys()

with open('products.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_products)
