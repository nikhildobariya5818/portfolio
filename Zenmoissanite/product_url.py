import os
import json
import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url, output_dir="listings"):
        self.url = url
        self.output_dir = output_dir

        # Ensure the output directory exists
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

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

    def get_shape_data(self):
        """Fetch shape URLs."""
        try:
            response = requests.get(self.url, cookies=self.cookies, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            Shape_urls = list(map(lambda tag: "https://zenmoissanite.com" + tag['href'], 
                                  soup.find_all('a', {'class': 'collection-card__link text-button'})))
            return Shape_urls
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def get_product_links(self):
        """Fetches all product links and organizes them by category."""
        all_product_links = {}
        Shape_urls = self.get_shape_data()

        for shapelink in Shape_urls:
            page = 1
            category_name = shapelink.split('/')[-1]  # Extract category name from URL
            all_product_links[category_name] = []

            while True:
                try:
                    paginated_url = f"{shapelink}?page={page}"
                    print(f"Fetching: {paginated_url}")
                    shape_response = requests.get(paginated_url, cookies=self.cookies, headers=self.headers)
                    shape_response.raise_for_status()
                    shape_soup = BeautifulSoup(shape_response.content, 'lxml')

                    links_grid = shape_soup.find(
                        'ul', {'class': 'products collection row small-up-2 medium-up-3 pagination--paginated'}
                    )

                    if not links_grid:  # If no products are found, exit the loop
                        break

                    product_links = [
                        "https://zenmoissanite.com" + tag['href']
                        for tag in links_grid.find_all(
                            'a', {'class': 'product-featured-image-link aspect-ratio aspect-ratio--portrait'}
                        )
                    ]

                    if not product_links:  # If no links are found, stop paginating
                        break

                    all_product_links[category_name].extend(product_links)
                    page += 1  # Increment page number to fetch the next page

                except requests.exceptions.RequestException as e:
                    print(f"An error occurred while fetching products from {paginated_url}: {e}")
                    break

        return all_product_links

    def save_to_json(self, category_name, product_links):
        """Save product links to a JSON file."""
        file_path = os.path.join(self.output_dir, f"{category_name}.json")
        with open(file_path, 'w') as file:
            json.dump(product_links, file, indent=4)
        print(f"Saved {len(product_links)} links to {file_path}")

    def scrape_and_save(self):
        """Main function to scrape data and save JSON files."""
        product_data = self.get_product_links()
        for category, links in product_data.items():
            self.save_to_json(category, links)


# Example usage
if __name__ == "__main__":
    scraper = WebScraper('https://zenmoissanite.com/')
    scraper.scrape_and_save()
