with open("links01.txt", "r", encoding="UTF-8") as f:
    links = f.readlines()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import json
import logging

# Disable selenium logs
logging.getLogger('selenium').setLevel(logging.ERROR)

def scrape(url):
    # Configure Chrome options
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
    
    # Set path to chromedriver executable
    chromedriver_path = "chromedriver.exe"
    
    # Set up the WebDriver
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        # Load the product page
        driver.get(url)
        
        # Wait for the page to load completely (you can increase the wait time if needed)
        driver.implicitly_wait(2)
        
        # Extract the product name
        product_name_element = driver.find_element(By.ID, "productTitle")
        product_name = product_name_element.text.strip()
        
        # Extract other details
        # Extracting the price
        price_element = driver.find_element(By.CSS_SELECTOR, "span.a-price-whole")
        price = price_element.get_attribute("textContent").strip()

        # Extracting the details
        # discount = driver.find_element(By.CSS_SELECTOR, "span.a-size-large.a-color-price.savingPriceOverride.aok-align-center.reinventPriceSavingsPercentageMargin.savingsPercentage").text.strip()
        rating = driver.find_element(By.CSS_SELECTOR, "span#acrCustomerReviewText.a-size-base").text.strip()
        star = driver.find_element(By.CSS_SELECTOR, "span.a-icon-alt").get_attribute("textContent").strip()

        # Extracting the image source
        image_element = driver.find_element(By.CSS_SELECTOR, "img.a-dynamic-image.a-stretch-horizontal")
        image_src = image_element.get_attribute("src")

        features = driver.find_elements(By.CSS_SELECTOR, "ul.a-unordered-list.a-vertical.a-spacing-mini")
        features = [feature.text.strip() for feature in features]

        # Return the extracted data as a dictionary or any other desired format
        product_details = {
            "url" : url,
            'name': product_name,
            'price': price,
            'rating': rating,
            "stars" : star,
            'image_src': image_src,
            'features': features
        }
        
        return product_details
    
    except Exception as e:
        print("Failed to scrape the product details.")
        print(e)
    
    finally:
        # Quit the WebDriver
        driver.quit()

# Example usage
# product_url = links[1] 
# product_details = scrape(product_url)
count = 0
file_name = 'data/details.json'
product_details = []

for link in links:
    try :
        details = scrape(link)
        if details is None:
            continue
        product_details.append(details)
        count += 1
        print(f"Successfully scraped {count} link(s)....")
        with open(file_name, 'w') as json_file:
            json.dump(product_details, json_file, indent=4)
        if count == 1000 :
            break
    except:
        print("Failed to scrape the product details.")




# Opening json file
# with open('data/details.json') as json_file:
#     data = json.load(json_file)