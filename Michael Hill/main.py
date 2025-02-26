import requests, json,csv,os
from helper_class import *
from bs4 import BeautifulSoup

class Michelhill:

    def __init__(self):
        self.base_url = "https://ac.cnstrc.com/browse/group_id/jewellery_shop-all"
        self.helper = Helper()
        self.params = {
            "c": "ciojs-client-2.42.3",
            "key": "key_lQlKc8rcUNV25zEo",
            "i": "d10692fa-6e87-40b1-8e4a-e96dde3b268f",
            "s": 4,
            "us": "guest",
            "num_results_per_page": 24,  # Start with 24 per page
            "_dt": "1735117673078",
        }
        self.offset = 0  # Initialize offset
        self.increment = 22  # Initial increment
        self.output_file = "products_url.json"  # File to store URLs


    def get_products_url(self):
        products_list = []

        # Initialize JSON file
        with open(self.output_file, "w") as file:
            json.dump([], file)  # Start with an empty list

        while True:
            # Update dynamic parameters
            self.params["offset"] = self.offset
            response = requests.get(self.base_url, params=self.params)

            # Check response status
            if response.status_code != 200:
                print(
                    f"Failed to fetch data at offset {self.offset}. Status code: {response.status_code}"
                )
                break

            data = response.json()
            results = data["response"].get("results", [])

            # Break the loop if no more results are returned
            if not results:
                print("No more products found. Stopping pagination.")
                break

            # Collect product URLs
            page_urls = [
                "https://www.michaelhill.com.au" + result["data"]["url"]
                for result in results
            ]
            products_list.extend(page_urls)

            # Append new URLs to the JSON file
            with open(self.output_file, "r+") as file:
                current_data = json.load(file)  # Load existing data
                current_data.extend(page_urls)  # Add new URLs
                file.seek(0)  # Reset file pointer to the start
                json.dump(current_data, file, indent=4)  # Write updated data

            # Print current progress
            print(
                f"Fetched {len(results)} products at offset {self.offset}. Total: {len(products_list)}"
            )

            # Increment offset for next page
            self.offset += self.increment

            # Update increment pattern (22 then 24)
            self.increment = 24 if self.increment == 22 else 22

        print(f"Total products fetched: {len(products_list)}")
        return products_list


    def get_product_details(self, url):
        print(f"Fetching data from {url}")
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
            return
        
        product = {}
        soup = BeautifulSoup(response.content, "lxml")

        # product["url"] = url
        # Extract product title
        product["title"] = self.helper.get_text_from_tag(soup.find('h1', {'class': 'product-detail-page__title'}))

        product["SKU"] = self.helper.get_text_from_tag(soup.find('div', {'class': 'product-detail-page__sku'})).replace("SKU: ", "")

        # Extract category information
        category_items = soup.find_all("li", {'class': 'breadcrumbs__link'})
        if len(category_items) > 2:  # Ensure there are at least 3 items in the breadcrumbs
            product["category"] = self.helper.get_text_from_tag(category_items[2].find("span"))

        # Extract price
        try:
            product["price"] = self.helper.get_text_from_tag(soup.find('span', {'class': 'base-pricing__retailOnly base-pricing__retail'}))
        except Exception as e:
            product["price"] = self.helper.get_text_from_tag(soup.find('span', {'class': 'base-pricing__doubleAndRetail base-pricing__double'}))

        try:
            product["List Price"] = self.helper.get_text_from_tag(soup.find('span', {'class': 'base-pricing__doubleAndRetail--strike'}))
        except Exception as e:
            product["List Price"] = None

        # Extract images
        images_divs = soup.find_all("div", {"class": "product-images__grid-wrapper relative"})
        product["images"] = []

        for div in images_divs:
            images = div.find_all("img")
            for img in images:
                if img.get("src"):
                    clean_url = img["src"].split('?')[0]  # Remove query parameters
                    product["images"].append(clean_url)
                elif img.get("srcset"):
                    srcset_urls = [url.split('?')[0] for url in img["srcset"].split(",")]
                    product["images"].append(srcset_urls[-1])

        # Extract product description
        product["description"] = self.helper.get_text_from_tag(soup.find('div', {'class': 'pdp-details__description'}))

        # Extract product specifications
        table = soup.find('div', {'class': 'product-detail-table__table'})

        # Iterate over rows in the table
        for row in table.find_all('tr'):
            # Find the key and value elements
            key_div = row.find('div', {'data-v-0ced7c33': ''})
            value_label = row.find('label', {'class': 'table-cell__value'})

            if key_div and value_label:
                # Get the key and value
                key = key_div.get_text(strip=True)
                value = value_label.get_text(strip=True)
                if value in key:
                    key = key.replace(value, "")
                product[key] = value

        self.store_product_in_csv(product)

    def store_product_in_csv(self,product):
        # Define the CSV file path
        csv_file = "product.csv"

        # Check if the file exists to write the headers only once
        file_exists = os.path.isfile(csv_file)

        # Open the file in append mode
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Write headers if the file is new
            if not file_exists:
                headers = ["URL", "Title", "SKU", "Category", "Price", "List Price", "Description", "Images"]
                # Add dynamic attribute columns
                for i in range(1, 21):  # Assuming up to 20 attributes
                    headers.append(f"Attribute {i} Name")
                    headers.append(f"Attribute {i} Value")
                writer.writerow(headers)

            # Prepare the row data
            row = [
                product.get("title", ""),
                product.get("SKU", ""),
                product.get("category", ""),
                product.get("price", ""),
                product.get("List Price", ""),
                product.get("description", ""),
                "|".join(product.get("images", []))  # Store images as a pipe-separated string
            ]

            # Add attributes to the row dynamically
            attributes = [key for key in product if key not in ["url", "title", "SKU", "category", "price", "List Price", "description", "images"]]
            for i, attribute in enumerate(attributes):
                row.append(attribute)  # Attribute name
                row.append(product[attribute])  # Attribute value

            # Fill remaining columns if attributes are less than the predefined number
            while len(row) < 8 + 2 * 20:  # Fixed header + 20 attribute pairs
                row.append("")

            # Write the row to the file
            writer.writerow(row)
        print(f"Product data written to {csv_file}")   

 
    def store_product_in_json(self, product_data):
        # Read existing data to avoid overwriting
        try:
            with open('product_details.json', 'r+', encoding='utf-8') as json_file:
                current_data = json.load(json_file)
        except FileNotFoundError:
            current_data = []  # If the file doesn't exist, create an empty list

        # Append new product data
        current_data.append(product_data)

        # Write the updated data back to the file
        with open('product_details.json', 'w', encoding='utf-8') as json_file:
            json.dump(current_data, json_file, ensure_ascii=False, indent=4)


    def run_multiThread(self, function, max_workers, args):
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(function, args)


    def scraper(self):
        with open ('products_url.json','r') as json_file:
            listing = json.load(json_file)
        self.run_multiThread(
            self.get_product_details,
            1,
            listing
        )




if __name__ == "__main__":
    scraper = Michelhill()
    # scraper.get_products_url()
    # scraper.get_product_details("https://www.michaelhill.com.au//p/55cm-22-oval-belcher-chain-10kt-yellow-gold-C1438974025.html")
    scraper.scraper()
    