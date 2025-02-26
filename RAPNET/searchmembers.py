from datetime import datetime
import csv
import requests
import concurrent.futures

class SearMember():

    def __init__(self):  
        self.headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16aERRMFExTURFeVJqSTNRa0k0TTBGRVJUZzFNekUzTWtOQ09UTXhNREZDTVVZM1JURkNNZyJ9.eyJodHRwOi8vcmFwYXBvcnQuY29tL3VzZXIiOnsiYWNjb3VudElkIjoxMjk4MTEsImNvbnRhY3RJZCI6NTEyODUsInNmTWFzdGVyQWNjb3VudE51bWJlciI6IkExNTU1NjMiLCJzZk1hc3RlckNvbnRhY3ROdW1iZXIiOiJDMTA5NDEzIn0sImh0dHA6Ly9yYXBhcG9ydC5jb20vZGV2aWNlSWQiOiIwMWU4YTcwMS02ZDIwLWNiMjEtNWFhYS05YTRkYmEyODhjMmQiLCJodHRwOi8vcmFwYXBvcnQuY29tL3Blcm1pc3Npb25zIjp7InJhcG5ldCI6WyJtZW1iZXJEaXJlY3RvcnkiLCJzZWFyY2giLCJpbnN0YW50SW52ZW50b3J5U2V0dXAiLCJtYW5hZ2VMaXN0aW5nc0ZpbGUiLCJidXlSZXF1ZXN0c0FkZCIsIml0ZW1TaGFyZWQiLCJ0cmFkZUNlbnRlciIsIm15Q29udGFjdHMiLCJtZW1iZXJSYXRpbmciLCJnZW1zIiwiY2hhdCIsIm1hbmFnZUxpc3RpbmdzIiwicHJpY2VMaXN0V2Vla2x5IiwicHJpY2VMaXN0TW9udGhseSIsInJhcG5ldFByaWNlTGlzdFdlZWtseSIsImJhc2ljIiwicmFwbmV0UHJpY2VMaXN0TW9udGhseSIsInJhcG5ldEpld2VsZXIiLCJsZWFkcyIsImFkbWluIiwiYnV5UmVxdWVzdHMiXX0sImlzcyI6Imh0dHBzOi8vbG9naW4ucmFwbmV0LmNvbS8iLCJzdWIiOiJhdXRoMHw2NzQ1YmE1NzE3ZDA1ZjA4ZGEwYzIwMTkiLCJhdWQiOlsiaHR0cHM6Ly9hcGkucmFwbmV0LmNvbS8iLCJodHRwczovL3JhcGFwb3J0LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MzUwMzQxMTgsImV4cCI6MTczNTA0MTMxOCwic2NvcGUiOiJvcGVuaWQiLCJhenAiOiJnRENQbjIxajJLVnFhMmdzTUZ3aTBTdGtZQWU0c1lWUiJ9.NpZvF007WIwAQ4QVn9XqKiRWeK9iL5qHTADT8egIFRZtGI-5rTaSN4FI_mANMoNAigpdyUt3cxEKjVFE-L5uY13BwFWX4xrg21zx3onoJqg2vn7Yxljfw1-iXkXnhu4VBxDUbj2fUTeNWEiYD6P8MQ65_0bBZOsnBeVZOoIKj21xwPavslHGM_-oGagYWxwaARNS_pPmVmRzkYlo903Pf1jTPbWitCBLWYe_K_0cKLiow8N6PukLFe7QDdHN_LSv4OylN_fPtUlUD9FFCR9ouSuPfqIfF37IOC5n87YX2wlWOemsTpE_kCt9oHStzZmB--iQ-BIYoOQqxbpAYtGKCQ',
    'content-type': 'application/json',
    'origin': 'https://trade.rapnet.com',
    'priority': 'u=1, i',
    'referer': 'https://trade.rapnet.com/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

        self.params = {
            'di': '01e8a701-6d20-cb21-5aaa-9a4dba288c2d',
            'version': 'production_version_2024-12-23_10-53',
        }

        self.current_year = datetime.now().year

    # Function to fetch and transform the data
    def fetch_and_transform_data(self, page_number):
        json_data = {
            'freeSearchName': '',
            'freeSearchLocation': None,
            'primarySuppliersOnly': False,
            'sortName': '',
            'sortDesc': False,
            'pageNumber': page_number,
            'recordsPerPage': 25,
        }

        # Make the POST request
        response = requests.post(
            'https://api.rapnet.com/api/MemberDirectory/SearchMembers/Quick',
            params=self.params,
            headers=self.headers,
            json=json_data,
        )

        if response.status_code != 200:
            print(f"Request failed with status code {response.status_code}")
            return []

        data = response.json()

        # Check if there is data to process
        if "data" in data and "searchMembersList" in data["data"]:
            MembersList = data["data"]["searchMembersList"]
            transformed_data = []

            if not MembersList:  # Break if no more data
                return transformed_data

            # Transform and store the data
            for company in MembersList:
                rapNetMemberSince = company.get("rapNetMemberSince")
                if rapNetMemberSince and isinstance(rapNetMemberSince, str):
                    member_since = datetime.fromisoformat(rapNetMemberSince)
                    years_since_joining = self.current_year - member_since.year
                else:
                    member_since = None
                    years_since_joining = "Unknown"

                transformed_data.append({
                    "companyName": company["companyName"],
                    "accountID": company["accountID"],
                    "country": company["location"]["country"],
                    "city": company["location"]["city"],
                    "state": company["location"]["state"],
                    "companyType": company["companyType"],
                    "rapNetMemberSince": rapNetMemberSince or "Unknown",
                    "totalRating": company["totalRating"],
                    "yearsSinceJoining": "Less than 1 year" if isinstance(years_since_joining, int) and years_since_joining < 1 else years_since_joining
                })

            return transformed_data
        else:
            print(f"No 'searchMembersList' found in the response.")
            return []

    # Function to save data to a CSV file
    def save_to_csv(self, data, filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "companyName", "accountID", "country", "city", "state", 
                "companyType", "rapNetMemberSince", "totalRating", "yearsSinceJoining"
            ])
            writer.writeheader()
            writer.writerows(data)

    # Function to fetch data concurrently
    def fetch_all_data_concurrently(self, num_pages):
        transformed_data = []

        # Using ThreadPoolExecutor to fetch multiple pages concurrently
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Fetch data for each page concurrently
            futures = [executor.submit(self.fetch_and_transform_data, page_number) for page_number in range(1, num_pages + 1)]
            
            for future in concurrent.futures.as_completed(futures):
                page_data = future.result()
                transformed_data.extend(page_data)
                print(f"Fetched data from a page")

        return transformed_data

    def main(self, num_pages):
        return self.fetch_all_data_concurrently(num_pages)

if __name__ == "__main__":
    Member = SearMember()
    num_pages = 500  # Adjust the number of pages to fetch

    # Fetch all data concurrently
    transformed_data = Member.main(num_pages)

    # Save the transformed data to a CSV file
    if transformed_data:
        Member.save_to_csv(transformed_data, 'Members_data.csv')
        print(f"Data has been saved to 'transformed_data.csv'. Total records: {len(transformed_data)}")
    else:
        print("No data was fetched or transformed.")
