from time import sleep
import pandas as pd
import numpy as np
import requests
from datetime import timedelta
from datetime import datetime
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from itertools import product
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from io import BytesIO


df = pd.DataFrame()
# Function to start a new WebDriver session
def start_webdriver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver

driver = start_webdriver()

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

# Define the function to scrape the minimum price for a given city and dates with retry mechanism
def scrape_min_price(city, departure_date, return_date, max_retries=10):
    url = f"https://www.kayak.ie/flights/PRG-{city}/{departure_date}/{return_date}?sort=bestflight_a"
    attempts = 0
    flight_prices = []

    # Start WebDriver
    driver = start_webdriver()

    while attempts < max_retries:
        try:
            driver.get(url)
            sleep(20)  # Adjust the sleep time as necessary for the page to load
            
            # Close any popups that may appear
            try:
                popwindow = driver.find_element(By.XPATH, '//*[@id="portal-container"]/div/div[2]/div/div/div[1]/div/span[2]/button/div/div')
                popwindow.click()
            except Exception:
                pass  # Ignore if no popup appears

            # Find all flight rows
            flight_rows = driver.find_elements(By.XPATH, '//div[@class="nrc6-inner"]')

            # If no flight rows are found, retry by reloading the page and restarting WebDriver
            if not flight_rows:
                print(f"No flight rows found, restarting WebDriver... attempt {attempts + 1} of {max_retries}")
                close_webdriver(driver)  # Close the current WebDriver session
                driver = start_webdriver()  # Start a fresh WebDriver session
                attempts += 1
                continue  # Retry with a fresh session

            # Scrape flight prices from each row
            for row in flight_rows:
                elementHTML = row.get_attribute('outerHTML')
                elementSoup = BeautifulSoup(elementHTML, 'html.parser')

                price = elementSoup.find("div", {"class": "f8F1-price-text"})
                if price:
                    # Clean and append price (removing currency symbols)
                    price_text = price.text.replace('€', '').replace(',', '').strip()
                    try:
                        flight_prices.append(float(price_text))  # Convert to float
                    except ValueError:
                        pass  # Skip if conversion fails

            # If we have successfully scraped prices, break out of the retry loop
            if flight_prices:
                break
            else:
                print(f"Retrying scrape... attempt {attempts + 1} of {max_retries}")
                attempts += 1

        except Exception as e:
            print(f"An error occurred: {e}. Retrying... attempt {attempts + 1} of {max_retries}")
            close_webdriver(driver)  # Restart WebDriver in case of an error
            driver = start_webdriver()
            attempts += 1

    # Close WebDriver after all attempts or after successful scrape
    close_webdriver(driver)

    # Return the minimum price if available, otherwise return None
    return min(flight_prices) if flight_prices else None

# Loop through each row in the DataFrame
min_prices = []
for index, row in df.iterrows():
    city = row['flight.Code']  
    departure_date = row['date'].strftime('%Y-%m-%d') 

    # Calculate the return date as departure date + 2 days
    return_date = (row['date'] + timedelta(days=2)).strftime('%Y-%m-%d')
    
    min_price = scrape_min_price(city, departure_date, return_date)
    
    # Append the minimum price to the list
    min_prices.append(min_price)

    print(min_price)

# Add the minimum price as a new column in the original DataFrame
df['Min Price'] = min_prices

driver.quit()
