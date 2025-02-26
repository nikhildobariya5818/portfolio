import requests
import json
import csv
import time

# Define headers for the API request
headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,gu;q=0.8',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik16aERRMFExTURFeVJqSTNRa0k0TTBGRVJUZzFNekUzTWtOQ09UTXhNREZDTVVZM1JURkNNZyJ9.eyJodHRwOi8vcmFwYXBvcnQuY29tL3VzZXIiOnsiYWNjb3VudElkIjoxMjk4MTEsImNvbnRhY3RJZCI6NTEyODUsInNmTWFzdGVyQWNjb3VudE51bWJlciI6IkExNTU1NjMiLCJzZk1hc3RlckNvbnRhY3ROdW1iZXIiOiJDMTA5NDEzIn0sImh0dHA6Ly9yYXBhcG9ydC5jb20vZGV2aWNlSWQiOiIwMWU4YTcwMS02ZDIwLWNiMjEtNWFhYS05YTRkYmEyODhjMmQiLCJodHRwOi8vcmFwYXBvcnQuY29tL3Blcm1pc3Npb25zIjp7InJhcG5ldCI6WyJtZW1iZXJEaXJlY3RvcnkiLCJzZWFyY2giLCJpbnN0YW50SW52ZW50b3J5U2V0dXAiLCJtYW5hZ2VMaXN0aW5nc0ZpbGUiLCJidXlSZXF1ZXN0c0FkZCIsIml0ZW1TaGFyZWQiLCJ0cmFkZUNlbnRlciIsIm15Q29udGFjdHMiLCJtZW1iZXJSYXRpbmciLCJnZW1zIiwiY2hhdCIsIm1hbmFnZUxpc3RpbmdzIiwicHJpY2VMaXN0V2Vla2x5IiwicHJpY2VMaXN0TW9udGhseSIsInJhcG5ldFByaWNlTGlzdFdlZWtseSIsImJhc2ljIiwicmFwbmV0UHJpY2VMaXN0TW9udGhseSIsInJhcG5ldEpld2VsZXIiLCJsZWFkcyIsImFkbWluIiwiYnV5UmVxdWVzdHMiXX0sImlzcyI6Imh0dHBzOi8vbG9naW4ucmFwbmV0LmNvbS8iLCJzdWIiOiJhdXRoMHw2NzQ1YmE1NzE3ZDA1ZjA4ZGEwYzIwMTkiLCJhdWQiOlsiaHR0cHM6Ly9hcGkucmFwbmV0LmNvbS8iLCJodHRwczovL3JhcGFwb3J0LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MzUxODk2MDYsImV4cCI6MTczNTE5NjgwNiwic2NvcGUiOiJvcGVuaWQiLCJhenAiOiJnRENQbjIxajJLVnFhMmdzTUZ3aTBTdGtZQWU0c1lWUiJ9.AnUKOOFA_uumaSnh5AgJ5_Nyy9KfWdtb7NyVqGQ8XW_9Z_Sut0Q2s4dQQs4BfikanjXYUqIPgNZ6h88TxatoAATWxnBmorUUqbp0mU5P9ebo2dD-L5rJw3TAE5VsvYdHjO8LFwWmL9F5bURFGFX9ivnTZYjYNSUALi4oY7QS7if9U9Q_Tn2VlXnTj9xoaxEVh96oFTx5IbMDOG3kzBDcvXp4U-ZGABLzMF4x9pKfBi38qGTN8wauUa8ozGD3SA6h_vNNPxud6U5rUtL6MyFb_1XpJRodoFzD1iVDjOdR9ug-l1lPaXKuZUF3os_ddPCBucqli-6i7jcWgDIijDZEmg',
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
params = {
    'di': '01e8a701-6d20-cb21-5aaa-9a4dba288c2d',
    'version': 'production_version_2024-12-23_10-53',
}
# Read diamond IDs from a JSON file
with open('diamonds_ids_by_fency.json', 'r', encoding="utf-8") as file:
    diamond_ids = json.load(file)

# Split diamond IDs into chunks of 250
chunk_size = 250
chunks = [diamond_ids[i:i + chunk_size] for i in range(0, len(diamond_ids), chunk_size)]

# CSV headers
csv_headers = [
    "Diamond ID", "GIA Report number", "Shape", "Size", "Color", "Clarity", "Cut", "Polish",
    "Symmetry", "Fluorescence", "Lab", "Ratio", "Depth", "Table", "Measurements", "Girdle",
    "Culet", "Treatment", "Star Length", "Pavilion", "Crown", "Shade", "Inclusion", "Brand",
    "Rap Spec", "Key To Symbols", "Lab Comment", "Member Comment", "Vendor Stock number",
    "$/ct", "%Rap", "Total", "Cash: $/ct", "Cash: %Rap", "Cash: Total", "Seller ID",
    "Seller", "City", "State", "Country", "Notes", "Last Updated", "Location", "Item Page",
    "Rating", "Availability", "Diamond Type","videoLink","imageURL","certificateURL"
]

output_file = "diamonds_by_fency.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=csv_headers)
    writer.writeheader()

    for index, chunk in enumerate(chunks):
        print(f"Processing chunk {index + 1} of {len(chunks)}...")

        json_data = {
    'searchType': 'Search',
    'diamondIds':chunk,
    'accessCode': None,
    'userAccessCode': {
        'name': None,
        'markUp': 0,
        'additionalMarkUp': 0,
    },
    'projection': {
        'include': [
            'Availability',
            'LongAvailability',
            'Status',
            'Seller',
            'Location',
            'Shape',
            'Clarity',
            'Lab',
            'Media',
            'Diamond Type',
            'Color',
            'Size',
            'Diamond ID',
            'Cut',
            'Vendor Stock number',
            'Measurements',
            'Brand',
            'Phone',
            'Star Length',
            'Rating',
            'Fax',
            'Polish',
            'Ratio',
            'Rap Spec',
            'Shade',
            'City',
            'State',
            'Country',
            'Symmetry',
            'Member Comment',
            'Fluorescence',
            'Girdle',
            'Inscription',
            'Total',
            '$/ct',
            '%Rap',
            'Cash: Total',
            'Cash: $/ct',
            'Cash: %Rap',
            'Last Updated',
            'Depth',
            'Lab Comment',
            'Culet',
            'Pavilion',
            'Key To Symbols',
            'Table',
            'Inclusion',
            'Treatment',
            'Crown',
            'ReportCheckURL',
            'EyeClean',
            'labShape',
            'Is RapNet Verified',
            'Cert #',
            'TradeShow',
            'HasGreenStar',
            'SellerOrigin',
            'Tracr',
            'Matching Vendor Stock number',
            'IsTracking',
            'LongAvailability',
            'Use Discount',
            'CertificateDisplayStatusID',
            'LaserInscription',
            'IsMatchedPair',
            'Note',
            'NoBGM',
        ],
        'displayMode': 'all',
    },
}

        try:
            # Make API request
            response = requests.post(
                'https://diamondsearch.gwapi.rapnet.com/diamondsearch/api/Diamonds/list',
                params=params,
                headers=headers,
                json=json_data
            )

            if response.status_code == 200:
                # Parse JSON response
                data = response.json()

                if "data" in data and "diamonds" in data["data"]:
                    diamonds = data["data"]["diamonds"]

                    for diamond in diamonds:
                        # width = diamond["measurements"].get("width")
                        # length = diamond["measurements"].get("length")
                        # depth = diamond["measurements"].get("depth")
                        # if width is None or length is None or depth is None:
                        #     measurements = None  # Or you can assign a default value like 0
                        # else:
                        #     measurements = width - (length * depth)
                        row = {
                            "Diamond ID": diamond["diamondID"],
                            "GIA Report number": diamond["certificateNumber"],
                            "Shape": diamond["shape"],
                            "Size": diamond["size"],
                            "Color": diamond["color"],
                            "Clarity": diamond["clarity"],
                            "Cut": diamond["cut"],
                            "Polish": diamond["polish"],
                            "Symmetry": diamond["symmetry"],
                            "Fluorescence": diamond["fluorescence"]["longIntensity"],
                            "Lab": diamond["lab"]["lab"],
                            "Ratio": diamond["measurements"]["ratio"],
                            "Depth": diamond["depthPercent"],
                            "Table": diamond["tablePercent"],
                            "Measurements": diamond["displayMeasurments"],   
                            "Girdle": diamond["displayGirdle"],
                            "Culet": diamond["displayCulet"],
                            "Treatment": diamond["displayTreatments"],
                            "Star Length": diamond["starLength"],
                            "Pavilion": diamond["displayPavilion"],
                            "Crown": diamond["displayCrown"],
                            "Shade": diamond["shade"],
                            "Inclusion": diamond["displayInclusions"],
                            "Brand": diamond["brand"],
                            "Rap Spec": diamond["displayRapQuality"],
                            "Key To Symbols": diamond["displayKeyToSymbols"],
                            "Lab Comment": diamond["displayLabComment"],
                            "Member Comment": diamond["memberComment"],
                            "Vendor Stock number": diamond["vendorStockNumber"],
                            "$/ct": diamond["price"]["pricePerCarat"],
                            "%Rap": diamond["price"]["listDiscount"],
                            "Total": diamond["price"]["totalPrice"],
                            "Cash: $/ct": diamond["price"]["cashPricePerCarat"],
                            "Cash: %Rap": diamond["price"]["cashListDiscount"],
                            "Cash: Total": diamond["price"]["cashTotalPrice"],
                            "Seller ID": diamond["seller"]["accountID"],
                            "Seller": diamond["seller"]["companyName"],
                            "City": diamond["location"]["city"],
                            "State": diamond["location"]["state"],
                            "Country": diamond["location"]["country"],
                            "Notes": diamond["memberComment"],
                            "Last Updated": diamond["displayDateUpdated"],
                            "Location": diamond["displayLocation"],
                            "Item Page": diamond["reportCheckURL"],
                            "Rating": diamond["seller"]["ratingPercent"],
                            "Availability": diamond["availability"],
                            "videoLink":diamond["files"]["videoLink"],
                            "imageURL": diamond["files"]["imageURL"],
                            "certificateURL":diamond["files"]["certificateURL"]
                            # "Diamond Type": diamond["diamondType"],
                        }
                        writer.writerow(row)

                print(f"Chunk {index + 1} processed successfully.")
            else:
                print(f"Error: {response.status_code} - {response.text}")

        except Exception as e:
            print(f"An error occurred while processing chunk {index + 1}: {e}")

        # Wait before the next request
        time.sleep(10)

print(f"Data successfully written to {output_file}")
