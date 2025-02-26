import time
import json
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.support.ui import Select
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helpers.helper_class import *
from Helpers.selenium_driver import *

class MAIN:

    def __init__(self):
        self.helper = Helper()
        self.selenium_driver = selenium_with_proxy()
        self.cookies = {
            "secure_customer_sig": "",
            "localization": "IN",
            "cart_currency": "INR",
            "_tracking_consent": "%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%2C%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%2C%22consent_id%22%3A%225FE9D8BB-009c-4D09-bd95-b8f24238996d%22%7D",
            "_shopify_y": "e1b49196-1e70-4352-a7a6-17ab876af84d",
            "_orig_referrer": "",
            "_landing_page": "%2F",
            "tracker_device_is_opt_in": "true",
            "optiMonkClientId": "6bfc0406-3a83-0df7-bf28-b07b0ba11ecc",
            "po_visitor": "zbIZ0YiakQni",
            "AMP_MKTG_16a5c84b5b": "JTdCJTdE",
            "Fera.geo": "JTdCJTIyY291bnRyeV9jb2RlJTIyJTNBJTIySU4lMjIlN0Q=",
            "cart": "Z2NwLWFzaWEtc291dGhlYXN0MTowMUpGSjZGQzlLNTFaQVpISDNYWjlQRTZYNg%3Fkey%3D7c444425cd7f1f966412295a2ccb8805",
            "_ps_session": "YEH73NZegNSmz-8BPXiAN",
            "_ruid": "eyJ1dWlkIjoiZTk5Y2ZiZDgtY2ViNC00ZWJhLTg4ZWEtMmNkMzU2ZDg1YjM1In0%3D",
            "_tt_enable_cookie": "1",
            "_ttp": "3z4_1VBydXp9WQQVKx2VEppWvT5.tt.1",
            "optiMonkSession": "1734755550",
            "locale_bar_accepted": "1",
            "cart_sig": "8bb5440f889872822aeb1c353cb3d098",
            "_shopify_s": "c0aa0eb3-518a-4c09-951d-c080830024a2",
            "_shopify_sa_t": "2024-12-22T05%3A42%3A51.891Z",
            "_shopify_sa_p": "",
            "optiMonkClient": "N4IgTAzArGAcCcIBcoDGBDZwC+AaEAZgG7ICMA7BACzkAMEspAbPgDYlIXWxVNcB0EUlXwA7APYAHDuSbZsQA===",
            "keep_alive": "ccb229b1-da59-489c-a3aa-167ab7e5872b",
            "shopify_pay_redirect": "pending",
            "discount_code": "%20",
            "AMP_16a5c84b5b": "JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1ZmQyNzE4Zi0wMGZkLTQ1NmUtODcwYS00OWZlZTNiOGE4OTElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0ODQ2MTc1NTQ1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDg0NjE3NzgwOSU3RA==",
            "_rsession": "ce461f54b7562216",
            "cart_ts": "1734846185",
        }
        self.headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9,gu;q=0.8",
            "cache-control": "max-age=0",
            # 'cookie': 'secure_customer_sig=; localization=IN; cart_currency=INR; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INGJ%22%2C%22reg%22%3A%22%22%2C%22purposes%22%3A%7B%22a%22%3Atrue%2C%22p%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%2C%22consent_id%22%3A%225FE9D8BB-009c-4D09-bd95-b8f24238996d%22%7D; _shopify_y=e1b49196-1e70-4352-a7a6-17ab876af84d; _orig_referrer=; _landing_page=%2F; tracker_device_is_opt_in=true; optiMonkClientId=6bfc0406-3a83-0df7-bf28-b07b0ba11ecc; po_visitor=zbIZ0YiakQni; AMP_MKTG_16a5c84b5b=JTdCJTdE; Fera.geo=JTdCJTIyY291bnRyeV9jb2RlJTIyJTNBJTIySU4lMjIlN0Q=; cart=Z2NwLWFzaWEtc291dGhlYXN0MTowMUpGSjZGQzlLNTFaQVpISDNYWjlQRTZYNg%3Fkey%3D7c444425cd7f1f966412295a2ccb8805; _ps_session=YEH73NZegNSmz-8BPXiAN; _ruid=eyJ1dWlkIjoiZTk5Y2ZiZDgtY2ViNC00ZWJhLTg4ZWEtMmNkMzU2ZDg1YjM1In0%3D; _tt_enable_cookie=1; _ttp=3z4_1VBydXp9WQQVKx2VEppWvT5.tt.1; optiMonkSession=1734755550; locale_bar_accepted=1; cart_sig=8bb5440f889872822aeb1c353cb3d098; _shopify_s=c0aa0eb3-518a-4c09-951d-c080830024a2; _shopify_sa_t=2024-12-22T05%3A42%3A51.891Z; _shopify_sa_p=; optiMonkClient=N4IgTAzArGAcCcIBcoDGBDZwC+AaEAZgG7ICMA7BACzkAMEspAbPgDYlIXWxVNcB0EUlXwA7APYAHDuSbZsQA===; keep_alive=ccb229b1-da59-489c-a3aa-167ab7e5872b; shopify_pay_redirect=pending; discount_code=%20; AMP_16a5c84b5b=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1ZmQyNzE4Zi0wMGZkLTQ1NmUtODcwYS00OWZlZTNiOGE4OTElMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzM0ODQ2MTc1NTQ1JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTczNDg0NjE3NzgwOSU3RA==; _rsession=ce461f54b7562216; cart_ts=1734846185',
            "if-none-match": '"cacheable:5b20f5f87f41a96ac9f92d3c58ea19a1"',
            "priority": "u=0, i",
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

    def select_dropdown_option(self, driver, dropdown_id, option_text):
        try:
            dropdown = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.ID, dropdown_id))
            )
            dropdown.click()

            option = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//div[text()='{option_text}']"))
            )
            option.click()
        except Exception as e:
            print(f"Failed to select {option_text} from dropdown {dropdown_id}: {e}")

    def extract_category(self, url):
        # Split the URL into parts
        parts = url.split("/")
        # Find the 'collections' keyword and get the next part as the category
        if "collections" in parts:
            return parts[parts.index("collections") + 1].replace("-", " ")
        return "No category found"

    def get_data(self, driver, url,output_csv):
        try:
            time.sleep(10)  # Adjust this to use WebDriverWait for better reliability
            print("Start scraping...")

            product_category = self.extract_category(url)

            # Scraping data
            images = driver.find_elements(By.CSS_SELECTOR, ".product-images__slide img")
            product_image = [img.get_attribute("src").split("?")[0] for img in images]

            try:
                video_element = driver.find_element(
                    By.CSS_SELECTOR, ".product-single__media video source"
                )
                video_src = video_element.get_attribute("src")
                if not video_src:
                    video_src = (
                        ""  # Handle cases where 'src' attribute exists but is blank
                    )
            except Exception as e:
                video_src = ""
            try:
                product_title = driver.find_element(
                    By.XPATH,
                    '//*[@id="ProductInfo-template--18415108456668__main-product"]/div[1]/h1',
                ).text
            except Exception as e:
                product_title = driver.find_element(
                    By.XPATH,
                    '//*[@id="ProductInfo-template--18415108423900__main-product"]/div[1]/h1',
                ).text

            try:
                product_price = driver.find_element(
                    By.XPATH,
                    '//*[@id="price-template--18415108456668__main-product"]/span/span/ins/span',
                ).text
            except Exception as e:
                product_price = driver.find_element(
                    By.XPATH,
                    '//*[@id="price-template--18415108423900__main-product"]/span/span/ins/span',
                ).text


            try:
                prongs_container = driver.find_element(
                    By.XPATH, '//*[@id="option-box-11tem1"]/div[2]'
                )
                prongs_inputs = prongs_container.find_elements(By.TAG_NAME, "input")
                facet_Pattern = [
                    input_elem.get_attribute("value") for input_elem in prongs_inputs
                ]
            except Exception as e:
                try:
                    prongs_container = driver.find_element(
                    By.XPATH, '//*[@id="option-box-23tem1"]/div[2]'
                )
                    prongs_inputs = prongs_container.find_elements(By.TAG_NAME, "input")
                    facet_Pattern = [
                        input_elem.get_attribute("value") for input_elem in prongs_inputs
                    ]
                    # print(prongs_values)

                except Exception as e:
                    try:
                        prongs_container = driver.find_element(
                        By.XPATH, '//*[@id="option-box-13tem1"]/div[2]'
                    )
                        prongs_inputs = prongs_container.find_elements(By.TAG_NAME, "input")
                        facet_Pattern = [
                            input_elem.get_attribute("value") for input_elem in prongs_inputs
                        ]
                    except Exception as e:
                        facet_Pattern = ""
            try:
                Metal_container = driver.find_element(
                    By.XPATH, '//*[@id="option-box-4tem1"]/div[2]'
                )
                Metal_inputs = Metal_container.find_elements(By.TAG_NAME, "input")
                Metal_values = [
                    input_elem.get_attribute("value") for input_elem in Metal_inputs
                ]
            except Exception as e:
                try:
                    Metal_container = driver.find_element(
                        By.XPATH, '//*[@id="option-box-573tem7"]/div[2]'
                    )
                    Metal_inputs = Metal_container.find_elements(By.TAG_NAME, "input")
                    Metal_values = [
                        input_elem.get_attribute("value") for input_elem in Metal_inputs
                    ]
                except Exception as e:
                    Metal_values = ""

            try:
                Bands = driver.find_element(
                    By.XPATH, '//*[@id="option-box-576tem11"]/div[2]'
                )
                Bands_inputs = Bands.find_elements(By.TAG_NAME, "input")
                Bands_values = [
                    band_elem.get_attribute("value") for band_elem in Bands_inputs
                ]
            except Exception as e:
                try:
                    Bands = driver.find_element(
                    By.XPATH, '//*[@id="option-box-573tem11"]/div[2]'
                )
                    Bands_inputs = Bands.find_elements(By.TAG_NAME, "input")
                    Bands_values = [
                        band_elem.get_attribute("value") for band_elem in Bands_inputs
                    ]
                except Exception as e:
                    Bands_values = ""

            try:
                select_element = driver.find_element(
                    By.XPATH, '//*[@id="ymq-attrib-ymq-variant-0"]'
                )
                select = Select(select_element)
                options = select.options
                Size_option_values = [option.get_attribute("value") for option in options]
            except Exception as e:
                try:
                    select_element = driver.find_element(
                        By.XPATH, '//*[@id="ymq-attrib-573tem6"]'
                    )
                    select = Select(select_element)
                    options = select.options
                    Size_option_values = [option.get_attribute("value") for option in options]
                except Exception as e:
                    Size_option_values = ""

            try:
                Dimensions_select_element = driver.find_element(
                    By.XPATH, '//*[@id="ymq-attrib-ymq-variant-0"]'
                )
                select = Select(Dimensions_select_element)
                options = select.options
                Dimensions_option_values = [option.get_attribute("value") for option in options]
            except Exception as e:
                try:
                    Dimensions_select_element = driver.find_element(
                        By.XPATH, '//*[@id="ymq-attrib-578tem6"]'
                    )
                    select = Select(Dimensions_select_element)
                    options = select.options
                    Dimensions_option_values = [option.get_attribute("value") for option in options]
                except Exception as e:
                    Dimensions_option_values = ""

                    
            response = requests.get(url, cookies=self.cookies, headers=self.headers)
            soup = BeautifulSoup(response.content, "lxml")

            Details = soup.find_all(
                "span", {"class": "metafield-multi_line_text_field"}
            )

            if len(Details) > 0:
                # Process the first span (Stone Size, Metal, and Ring Size)
                Pictured = Details[0]
                if Pictured:
                    lines = Pictured.get_text(separator="\n").split("\n")
                    lines = [line.strip() for line in lines if line.strip()]

                    images_Stone_size = lines[0] if len(lines) > 0 else None
                    image_metal = lines[1] if len(lines) > 1 else None
                    image_Finger_Ring_Size = lines[2] if len(lines) > 2 else None

                # Process the second span (Specifications)
                Specifications = Details[1]
                if Specifications:
                    lines = Specifications.get_text(separator="\n").split("\n")
                    lines = [line.strip() for line in lines if line.strip()]

                    material = None
                    cut = None
                    clarity = None
                    color = None
                    additional_features = []

                    for line in lines:
                        if line.startswith("Material:"):
                            material = line.replace("Material:", "").strip()
                        elif line.startswith("Cut:"):
                            cut = line.replace("Cut:", "").strip()
                        elif line.startswith("Clarity:"):
                            clarity = line.replace("Clarity:", "").strip()
                        elif line.startswith("Color:"):
                            color = line.replace("Color:", "").strip()
                        else:
                            additional_features.append(line)
            else:
                print("No matching spans found.")

            # Prepare data for CSV
            data = {
                "URL": url,
                "category": product_category,
                "Product Title": product_title,
                "Price": product_price,
                "Images": ", ".join(
                    product_image
                ),  # Join multiple images with a separator
                "Video Source": video_src,
                "Facet Pattern": ", ".join(facet_Pattern),
                "Dimensions": ", ".join(Dimensions_option_values),
                "Metal": ", ".join(Metal_values),  
                "Band": ", ".join(Bands_values),
                # "Size": ", ".join(Size_option_values),  
                # "images_Stone_size": images_Stone_size,
                # "image_metal": image_metal,
                # "image_Finger_Ring_Size": image_Finger_Ring_Size,
                # "Material": material,
                # "Cut": cut,
                # "Clarity": clarity,
                # "Color": color,
                # "Additional Fatures": "".join(additional_features),
            }

            # Write data to CSV
            with open(output_csv, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                if file.tell() == 0:  # Write header only if the file is new
                    writer.writeheader()
                writer.writerow(data)

            print(f"Data successfully written to {output_csv}.")

        except Exception as e:
            print(f"An error occurred: {e}")



    def scrape_from_json_files(self,output_folder):
        driver = self.selenium_driver.get_driver()
        driver.maximize_window()
        
        output_csv = os.path.join(output_folder, f"{os.path.splitext("loose-stones")[0]}.csv")

        # Read JSON file
        try:
            with open("loose-stones.json", "r", encoding="utf-8") as file:
                urls = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {"loose-stones.json"} was not found.")
            driver.quit()
            return
        except json.JSONDecodeError:
            print(f"Error: The file {"loose-stones.json"} is not a valid JSON.")
            driver.quit()
            return

        for url in urls:
            try:
                driver.get(url)
                print(f"Scraping URL: {url}")
                self.get_data(driver, url, output_csv)
            except Exception as e:
                print(f"Error while scraping {url}: {e}")

        driver.quit()



if __name__ == "__main__":
    output_folder = "Output"
    os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

    scraper = MAIN()
    scraper.scrape_from_json_files(output_folder)
    