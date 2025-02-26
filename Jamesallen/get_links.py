import requests
from bs4 import BeautifulSoup
import json
from helper_class import *

class GetLinks:

    def __init__(self):    
        self.base_url = "https://www.jamesallen.com/fine-jewelry/all-jewels"
        self.links = []
        self.helper = Helper()
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

    def get_links(self):
        page = 1
        while True:
            url = f"{self.base_url}?page={page}"
            response = requests.get(url, headers=self.headers, cookies=self.cookies)
            if response.status_code != 200:
                print(f"Failed to fetch page {page}, status code: {response.status_code}")
                break

            soup = BeautifulSoup(response.content, "lxml")
            product_container = soup.find('div', {'id': 'data-page-container'})
            product_links = [
                'https://www.jamesallen.com' + self.helper.get_url_from_tag(product)
                for product in product_container.find_all('a', {'class': 'itemMediaWrapper--o9crtD_Gsoixk_Kb0zHp'})
            ]

            if not product_container:  # Break the loop if no links are found
                print(f"No more links found. Stopping at page {page}.")
                break

            self.links.extend(product_links)

            # Save links to JSON file
            with open("get_links.json", "w") as f:
                json.dump(self.links, f, indent=4)

            print(f"Page {page}: {len(product_links)} links found.")
            page += 1

        print(f"Total links collected: {len(self.links)}")
        return self.links

if __name__ == "__main__":
    links = GetLinks()
    all_links = links.get_links()
    print(all_links)
