import requests
from bs4 import BeautifulSoup
from helper_class import *
from selenium_driver import *
from selenium.webdriver.common.action_chains import ActionChains


class jamesallen:

    def __init__(self):
        self.helper = Helper()
        self.selenium_driver = selenium_with_proxy()

        self.cookies = {
            "OptanonAlertBoxClosed": "2024-12-23T11:43:36.264Z",
            "yotpo_pixel": "70fdd39c-eb10-4d6d-8630-0837ad869857",
            "ASP.NET_SessionId": "ceohpbywdrancublxgkbl3ft",
            "akamaiData": "georegion=104,country_code=IN,region_code=GJ,city=AHMEDABAD,lat=23.03,long=72.62,timezone=GMT+5.50,continent=AS,throughput=vhigh,bw=5000,asnum=45916,location_id=0",
            "Currency": "%7B%22Code%22%3A%22USD%22%2C%22Rate%22%3A1%2C%22Symbol%22%3A%22%24%22%2C%22IsUserSelection%22%3Afalse%7D",
            "abDiamondStudsGallery": "1",
            "CountryCode": "",
            "gtm-event-user-clicked": "1",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Tue+Dec+24+2024+10%3A16%3A40+GMT%2B0530+(India+Standard+Time)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=IN%3BGJ",
            "forterToken": "1e7002053eac4e558d87d7f8a4256132_1735015600701_735_UAS9_21ck",
            "_sp_ses.bdd5": "*",
            "_sp_id.bdd5": "ccea4c10ce96f129.1734954342.3.1735019719.1735015021",
        }

        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,gu;q=0.8",
            "cache-control": "max-age=0",
            # 'cookie': 'OptanonAlertBoxClosed=2024-12-23T11:43:36.264Z; yotpo_pixel=70fdd39c-eb10-4d6d-8630-0837ad869857; ASP.NET_SessionId=ceohpbywdrancublxgkbl3ft; akamaiData=georegion=104,country_code=IN,region_code=GJ,city=AHMEDABAD,lat=23.03,long=72.62,timezone=GMT+5.50,continent=AS,throughput=vhigh,bw=5000,asnum=45916,location_id=0; Currency=%7B%22Code%22%3A%22USD%22%2C%22Rate%22%3A1%2C%22Symbol%22%3A%22%24%22%2C%22IsUserSelection%22%3Afalse%7D; abDiamondStudsGallery=1; CountryCode=; gtm-event-user-clicked=1; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Dec+24+2024+10%3A16%3A40+GMT%2B0530+(India+Standard+Time)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0005%3A1%2CC0004%3A1%2CC0003%3A1&AwaitingReconsent=false&geolocation=IN%3BGJ; forterToken=1e7002053eac4e558d87d7f8a4256132_1735015600701_735_UAS9_21ck; _sp_ses.bdd5=*; _sp_id.bdd5=ccea4c10ce96f129.1734954342.3.1735019719.1735015021',
            "priority": "u=0, i",
            "referer": "https://www.jamesallen.com/wedding-rings/womens-anniversary/14k-white-gold-seven-stone-emerald-cut-diamond-ring-100-ctw-h-i-si1-si2-item-111816",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        }

    def getdata(self, url):
        driver = self.selenium_driver.get_driver()
        driver.maximize_window()
        driver.get(url)
        time.sleep(10)
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait for new content to load
            time.sleep(2)  # Adjust this time as necessary

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Exit the loop if no new content is loaded
            last_height = new_height

        response = requests.get(
            url,
            cookies=self.cookies,
            headers=self.headers,
        )
        print(response.status_code)
        soup = BeautifulSoup(response.content, "lxml")

        title = self.helper.get_text_from_tag(
            soup.find(
                "h1",
                {
                    "class": "@ecommo/create-lib__sc-1byi3e7-1 glhXKn dyoItemPage-cui-purchase-title"
                },
            )
        )
        print(title)

        total_price = self.helper.get_text_from_tag(
            soup.find("div", {"class": "price--GUo2yxzV2va4P7Bqe00G"})
        )

        sell_price = self.helper.get_text_from_tag(
            soup.find("div", {"class": "salePrice--uuobw9coOVffSdAFlc3J"})
        )
        print(total_price, sell_price)

        product_slider = soup.find_all('div', {'class': 'itemWrapper--Hhxe0b4ioze2XYcUWhZX'})

        if product_slider:
            product_images = []
            for slider in product_slider:
                img = slider.find('img')
                if img:
                    product_images.append(img.get('src'))
            
            print("Product Images:", product_images)
        else:
            print("No product slider found.")

        SKU = self.helper.get_text_from_tag(soup.find('div',{'class':'skuNumber--llfcYTjTD8r3jbJndS8u'}))
        print(SKU)

        DISCLAIMER = self.helper.get_text_from_tag(soup.find('div',{'class':'disclaimerWrapper--JpFvxNtkQ_MXTjU9FZqt'}))
        
        print(DISCLAIMER)

        wait = WebDriverWait(driver, 20)

        # Find all <a> tags with the `data-qa="metal_filter_*"` attribute
        metal_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-qa^="metal_filter"]')

        # Initialize ActionChains for hovering
        actions = ActionChains(driver)

        # Create a dictionary to store metal names and prices
        metal_details = {}

        for metal in metal_elements:
            # Hover over the metal element
            actions.move_to_element(metal).perform()
            
            # Wait for the updated span with the price to appear
            try:
                updated_span = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'span[data-qa="metal_title"]')))
                metal_title = updated_span.text
            except Exception as e:
                print(f"Error while waiting for metal title: {e}")
                metal_title = 'Unknown'

            # Separate the metal name and price if combined (e.g., "14K White Gold $1908")
            if "$" in metal_title:
                metal_name, price = metal_title.rsplit(" ", 1)
            else:
                metal_name, price = metal_title, "Price not found"

            # Store the details
            metal_details[metal_name] = price

        # Print the collected data
        for metal, price in metal_details.items():
            print(f"Metal: {metal}, Price: {price}")

        # Optional: Check if you have collected all expected values
        if len(metal_details) < 6:
            print(f"Warning: Expected 6 metal values, but found {len(metal_details)}.")

        tabs = driver.find_elements(By.CSS_SELECTOR, '.tabWrapper--FOsAsXkb7e5TjCLD5gGc')

        for tab in tabs:
            tab_name = tab.text.strip()
            # print(f"Clicking tab: {tab_name}")
            
            # Hide iframe if present
            try:
                iframe = driver.find_element(By.TAG_NAME, "iframe")
                driver.execute_script("arguments[0].style.visibility='hidden';", iframe)
            except:
                pass

            # Use JavaScript click
            driver.execute_script("arguments[0].click();", tab)
            
            # Wait for content to load
            time.sleep(10)
            
            # Extract data from the description table
            try:
                description_table = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "descriptionTables--QQYHrnAIorBgzjqx9i0d")))
                rows = description_table.find_elements(By.CSS_SELECTOR, '.detailRow--EJOouSghmEkq_F8M2WZw')
                for row in rows:
                    label = row.find_element(By.CSS_SELECTOR, '.label--gTJIzaubW5ZYCaJZ1gNN').text.strip()
                    value = row.find_element(By.CSS_SELECTOR, '.textValue--YvkaqNWEsMHVyqsGTnfL').text.strip()
                    print(f"{label}: {value}")
            except Exception as e:
                print(f"Failed to extract data for tab {tab_name}: {e}")

if __name__ == "__main__":
    scrap = jamesallen()
    scrap.getdata(
        "https://www.jamesallen.com/engagement-rings/side-stones/14k-white-gold-emerald-cut-side-stone-diamond-engagement-ring-item-133676"
    )
