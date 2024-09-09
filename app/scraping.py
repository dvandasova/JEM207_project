from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

# Function to start a new WebDriver session
def start_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

def close_webdriver(driver):
    driver.quit()

def scrape_accommodation_data(location, departure_date, return_date, max_retries=5):
    # URL to load
    url = f"https://www.kayak.com/hotels/{location}/{departure_date}/{return_date}/2adults;map?sort=rank_a"
    
    # Battling against captcha
    attempts = 0
    booking_data = []

    driver = start_webdriver()

    while attempts < max_retries:
        driver.get(url)
        sleep(10)

        # Scroll down to load more hotels
        actions = ActionChains(driver)
        for _ in range(5):
            actions.send_keys(Keys.PAGE_DOWN).perform()
            sleep(2)

        # Find hotel rows
        hotel_rows = driver.find_elements("xpath", '//div[contains(@class, "resultInner")]')

        # If no hotel rows are found, retry by reloading the page and restarting WebDriver
        if not hotel_rows:
            print(f"No hotels found, restarting WebDriver... attempt {attempts + 1} of {max_retries}")
            close_webdriver(driver)  
            driver = start_webdriver() 
            attempts += 1
            continue 

        # scrape the hotel_rows
        for row in hotel_rows:
            elementHTML = row.get_attribute('outerHTML')
            elementSoup = BeautifulSoup(elementHTML, 'html.parser')

            # Extract hotel details
            location_elem = elementSoup.find("div", {"class": "upS4 upS4-big-name"})
            location_text = location_elem.text if location_elem else "Location not found"

            name_elem = elementSoup.find("div", {"class": "FLpo-hotel-name"})
            name_text = name_elem.text if name_elem else "Name not found"

            rating_elem = elementSoup.find("div", {"class": "wdjx wdjx-positive wdjx-mod-rating-condensed"})
            rating_text = rating_elem.text[:3] if rating_elem else "0"
            rating_text = rating_text.replace(",", ".")

            price_elem = elementSoup.find("div", {"class": "c1XBO"})
            price_text = price_elem.text if price_elem else "0"

            if price_text == "0" or rating_text == "0" or name_text == "Name not found":
                continue  
            else:
                booking_data.append({
                    'Location': location_text,
                    "Name": name_text,
                    "Rating": rating_text,
                    "Price": price_text
                })

        # If we have successfully scraped data, break out of the retry loop
        if booking_data:
            break
        else:
            print(f"Retrying scrape... attempt {attempts + 1} of {max_retries}")
            attempts += 1

    close_webdriver(driver)

    if not booking_data:
        print("No data found after retries.")
        return pd.DataFrame()

    # Convert the scraped data to a DataFrame
    booking_data_df = pd.DataFrame(booking_data)

    # Data cleaning and conversion to numeric types
    booking_data_df['Rating'] = pd.to_numeric(booking_data_df['Rating'], errors='coerce')
    booking_data_df['Price_numeric'] = booking_data_df['Price'].replace({'\$': '', ',': ''}, regex=True)
    booking_data_df['Price_numeric'] = pd.to_numeric(booking_data_df['Price_numeric'], errors='coerce')

    return booking_data_df