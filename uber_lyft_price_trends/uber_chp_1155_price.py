from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np

# Initializing Variables
uber_chp_1155_url = 'https://m.uber.com/looking?drop%5B0%5D=%7B%22latitude%22%3A41.785475%2C%22longitude%22%3A-87.597072%2C%22addressLine1%22%3A%221155%20E%2060th%20St%22%2C%22addressLine2%22%3A%22Chicago%2C%20Illinois%22%2C%22id%22%3A%228be9181e-8177-f095-05eb-14dcf7c0f522%22%2C%22provider%22%3A%22uber_places%22%7D&pickup=%7B%22latitude%22%3A41.801926%2C%22longitude%22%3A-87.5884479%2C%22addressLine1%22%3A%225105%20S%20Harper%20Ave%22%2C%22addressLine2%22%3A%22Chicago%2C%20Illinois%22%2C%22id%22%3A%222c5c63fc-abd1-dd6e-6225-4fe5dd1cf7b0%22%2C%22provider%22%3A%22uber_places%22%2C%22index%22%3A0%7D&vehicle=180'
uber_chp_1155_ride_service_lst = []
uber_chp_1155_req_time_lst = []
uber_chp_1155_dropoff_text_lst = []
uber_chp_1155_est_price_lst = []    


# 1. Launch a new Chrome Session
uber_chp_1155_browser = webdriver.Chrome(ChromeDriverManager().install())
uber_chp_1155_browser.get(uber_chp_1155_url);

# 2. Prepare the web sraping function 
def refresh_uber_and_get_ride_stats(browser, route_url, ride_service_lst, est_price_lst, dropoff_text_lst, req_time_lst):
    try:
        # Step 1: refresh the page
        browser.get(route_url)
        req_time = datetime.now() # request_time         
        time.sleep(10) # rest for 10 seconds
    
        # Step 2: retrieve the content
        page_source = browser.page_source        
        soup = BeautifulSoup(page_source, 'html.parser') # parse into beautiful soup

        LEN_RIDE_SERVICE_LST = len(ride_service_lst)
        LEN_REQ_TIME_LST = len(req_time_lst)
        LEN_DROPOFF_TEXT_LST = len(dropoff_text_lst)
        EST_PRICE_LST = len(est_price_lst)

        # Step 3: parse the content
        rides_price_soup_res = soup.body.find_all('div',class_ = '_css-dZTBoz') # find the required HTML elements
        rides_dropoff_soup_res = soup.body.find_all('p',class_ = '_css-lcvSVT') # find the required HTML elements

        # Step 4: store in list instances
        ride_service_lst.append(rides_price_soup_res[0].get_text()) # UberX
        ride_service_lst.append(rides_price_soup_res[4].get_text()) # UberXL
        ride_service_lst.append(rides_price_soup_res[14].get_text()) # Black

        est_price_lst.append(rides_price_soup_res[1].get_text()) # UberX - price
        est_price_lst.append(rides_price_soup_res[5].get_text()) # UberXL - price
        est_price_lst.append(rides_price_soup_res[15].get_text()) # Black - price

        dropoff_text_lst.append(rides_dropoff_soup_res[1].get_text().split(" ")[3]) # UberX - dropoff
        dropoff_text_lst.append(rides_dropoff_soup_res[5].get_text().split(" ")[0]) # UberXL - dropoff 
        dropoff_text_lst.append(rides_dropoff_soup_res[15].get_text().split(" ")[0]) # Black - dropoff

        req_time_lst = req_time_lst + [req_time]*(len(est_price_lst)-LEN_RIDE_SERVICE_LST) # request time

        print(f"Add {len(ride_service_lst)-LEN_RIDE_SERVICE_LST} service records to ride service list.")
        print(f"Add {len(est_price_lst)-EST_PRICE_LST} service records to price list.")
        print(f"Add {len(dropoff_text_lst)-LEN_DROPOFF_TEXT_LST} service records to ride dropoff list.")
        print(f"Add {len(req_time_lst)-LEN_REQ_TIME_LST} service records to request time list.")
        print(est_price_lst[-3:])
        print(dropoff_text_lst[-3:],'\n')
    
        return ride_service_lst, est_price_lst, dropoff_text_lst, req_time_lst 
    except Exception as e:
        print("Error Occur: ",e)
        return ride_service_lst, est_price_lst, dropoff_text_lst, req_time_lst 
    
# 3. Iteratively executes the web crawling function
i = 0   
while True:
    i = i+1
    print(f"Retrieving {i}th ride statistics from CityHydePark to 1155, at {datetime.now()}")        
    # get ride statistics
    (uber_chp_1155_ride_service_lst, 
     uber_chp_1155_est_price_lst, 
     uber_chp_1155_dropoff_text_lst, 
     uber_chp_1155_req_time_lst) = refresh_uber_and_get_ride_stats(
                                    uber_chp_1155_browser, 
                                    uber_chp_1155_url,
                                    uber_chp_1155_ride_service_lst, 
                                    uber_chp_1155_est_price_lst, 
                                    uber_chp_1155_dropoff_text_lst, 
                                    uber_chp_1155_req_time_lst)
    # rest for 20 seconds
    time.sleep(20)

    if i >= 2880:
        break


print(uber_chp_1155_ride_service_lst[-3:])
print(uber_chp_1155_est_price_lst[-3:])
print(uber_chp_1155_dropoff_text_lst[-3:])
print(uber_chp_1155_req_time_lst[-3:])

df = pd.DataFrame({
    'ride_service':uber_chp_1155_ride_service_lst,
    'est_price':uber_chp_1155_est_price_lst,
    'dropoff_text':uber_chp_1155_dropoff_text_lst,
    'request_time':uber_chp_1155_req_time_lst
})

df.to_csv("../uber_chp_1155_p2.csv")