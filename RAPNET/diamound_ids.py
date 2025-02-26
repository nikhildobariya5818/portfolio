import requests
import json
import time

# Configuration
OUTPUT_FILE = "diamonds_ids_by_fency.json"
MAX_ATTEMPTS = 5
PAGE_SIZE = 250

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
# Initialize or load existing data
def load_existing_data(file_path):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

def save_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(list(data), file, indent=4)

def fetch_diamonds(page_number, start):
    json_data = {
    'filter': {
        'selectionID': None,
        'selectionName': None,
        'selectionGroup': None,
        'selectionGroupDescription': None,
        'shape': {
            'isAdvancedShape': False,
            'shapes': [
                'Round',
                'Pear',
                'Oval',
                'Marquise',
                'Heart',
                'Radiant',
                'Princess',
                'Emerald',
                'Asscher',
                'Sq. Emerald',
                'Asscher & Sq. Emerald',
                'Square Radiant',
                'Cushion (All)',
                'Cushion Brilliant',
                'Cushion Modified',
                'Baguette',
                'European Cut',
                'Old Miner',
                'Briolette',
                'Bullets',
                'Calf',
                'Circular Brilliant',
                'Epaulette',
                'Flanders',
                'Half Moon',
                'Hexagonal',
                'Kite',
                'Lozenge',
                'Octagonal',
                'Pentagonal',
                'Rose',
                'Shield',
                'Square',
                'Star',
                'Tapered Baguette',
                'Tapered Bullet',
                'Trapezoid',
                'Triangular',
                'Trilliant',
                'Other',
            ],
            'labShapes': [],
        },
        'size': {
            'isSpecificSize': True,
            'sizeFrom': '.30',
            'sizeTo': '20',
            'sizeGrids': [],
        },
        'color': {
            'isWhiteColor': True,
            'colorFrom': 'D',
            'colorTo': 'M',
            'fancyColors': [],
            'fancyColorOvertones': [],
            'fancyColorIntensityFrom': None,
            'fancyColorIntensityTo': None,
        },
        'clarity': {
            'clarityFrom': 'FL',
            'clarityTo': 'SI2',
        },
        'inclusions': {
            'eyeCleans': [],
            'openInclusions': [],
            'whiteInclusions': [],
            'blackInclusions': [],
            'milkyFrom': None,
            'milkyTo': None,
        },
        'includedShade': {
            'shades': [],
            'noBGM': False,
            'include': False,
        },
        'finish': {
            'isSpecificFinish': True,
            'finishGroup': '',
            'cutFrom': None,
            'cutTo': None,
            'polishFrom': None,
            'polishTo': None,
            'symmetryFrom': None,
            'symmetryTo': None,
        },
        'fluorescence': {
            'fluorescenceColors': [],
            'fluorescenceIntensities': [
                'None',
                'Very Slight',
                'Faint / Slight',
                'Medium',
                'Strong',
                'Very Strong',
            ],
            'fluorescenceIntensityFrom': None,
            'fluorescenceIntensityTo': None,
        },
        'labs': [
            'GIA',
            'HRD',
            'IGI',
        ],
        'location': {
            'state': None,
            'cities': [],
            'countries': [],
            'locations': [],
            'flexibleDelivery': False,
            'isExcluded': False,
        },
        'rapQualities': [],
        'price': {
            'pricePerCaratFrom': None,
            'pricePerCaratTo': None,
            'totalPriceFrom': None,
            'totalPriceTo': None,
            'priceRapListPercentFrom': None,
            'priceRapListPercentTo': None,
            'includeCashPrice': False,
        },
        'showOnly': {
            'primarySupplierBadge': False,
            'guaranteedAvailable': False,
            'rapTrade': False,
            'latestListings': False,
            'matchedPairs': False,
            'rapNetVerified': False,
            'crystalType': False,
            'greenStar': False,
            'tradeShow': None,
            'tradeShowName': None,
        },
        'media': {
            'withPhoto': False,
            'withVideo': False,
            'withLabReport': False,
            'withSarinLoupe': False,
        },
        'depth': {
            'depthPercentFrom': None,
            'depthPercentTo': None,
        },
        'table': {
            'tablePercentFrom': None,
            'tablePercentTo': None,
        },
        'ratio': {
            'ratioFrom': None,
            'ratioTo': None,
        },
        'measurement': {
            'widthFrom': None,
            'widthTo': None,
            'lengthFrom': None,
            'lengthTo': None,
            'depthFrom': None,
            'depthTo': None,
        },
        'crown': {
            'crownHeightFrom': None,
            'crownHeightTo': None,
            'crownAngleFrom': None,
            'crownAngleTo': None,
        },
        'pavilion': {
            'pavilionDepthFrom': None,
            'pavilionDepthTo': None,
            'pavilionAngleFrom': None,
            'pavilionAngleTo': None,
        },
        'girdle': {
            'girdleSizeFrom': None,
            'girdleSizeTo': None,
            'girdleConditions': [],
        },
        'culet': {
            'culetSizeFrom': None,
            'culetSizeTo': None,
            'culetConditions': [],
        },
        'rapCode': None,
        'treatment': {
            'showTreated': False,
            'showOnlyTreated': False,
            'isHPHT': False,
            'isLaserDrilled': False,
            'isIrradiated': False,
            'isClarityEnhanced': False,
            'isColorEnhanced': False,
            'isOtherTreatment': False,
            'noTreatments': True,
        },
        'totalSize': {
            'totalSizeFrom': None,
            'totalSizeTo': None,
        },
        'keyToSymbol': {
            'keyToSymbols': [],
            'isContainKeyToSymbols': False,
            'keyToSymbolOptions': 'Contains',
        },
        'brands': [],
        'seller': {
            'isSpecificGroupsSellers': True,
            'sellers': [],
            'groupsSellers': [],
            'vendorStockNumbers': [],
            'rating': 0,
        },
        'diamondIDs': [],
        'noteTypes': [],
        'accessCode': None,
        'userAccessCode': {
            'name': None,
            'markUp': 0,
            'additionalMarkUp': 0,
        },
        'labReportNumbers': [],
        'socialResponsibility': {
            'isSR': False,
            'attributes': [],
        },
        'stockOrDiamondIDs': [],
        'source': [],
        'sourceProvider': [],
        'hasGreenStar': False,
        'memberComment': '',
        'certComment': '',
    },
    'additionalFilter': {
        'pageNumber': page_number,
        'recordsPerPage': PAGE_SIZE,
        'searchType': None,
        'sortOptions': [],
        'notification': {
            'notificationID': None,
            'sendNotifications': False,
            'notificationType': 'Match Diamonds',
            'sendDaily': True,
            'sendImmediate': False,
            'isSendImmediate': False,
        },
        'myListings': {
            'cashPriceOnly': False,
            'showImages': None,
            'showCertImages': None,
            'showAutoAddedCerts': None,
            'showQuotaExceededOnly': False,
            'showPotentialInvestmentGradeOnly': False,
            'showIIOwnStockOnly': False,
            'blockedOnly': False,
            'stockNumber': '',
        },
        'savedSearch': {
            'savedID': None,
            'dateCreated': None,
            'dateUpdated': None,
        },
        'trackDiamonds': {
            'trackDiamondsID': None,
            'comment': None,
            'dateCreated': None,
            'dateUpdated': None,
        },
        'tradeScreen': {
            'rapSpecAll': None,
            'lowestPricePercentile': None,
            'lowestPriceSliceDiamonds': None,
            'isAveragePriceDiamond': False,
            'saveID': None,
        },
        'buyRequest': {
            'buyRequestID': None,
            'comment': None,
            'dateExpires': '2024-12-27T05:03:05.604Z',
            'dateCreatedFrom': None,
            'dateCreatedTo': None,
            'dateExpiresFrom': None,
            'dateExpiresTo': None,
            'includeExpired': False,
            'type': 'Public',
            'withNotification': False,
            'notificationFrequency': None,
            'showMyRequests': False,
            'showExpiredRequests': False,
            'showActiveOnly': False,
            'withMyResponse': False,
            'withMyInventoryMatches': False,
            'withSellerResponses': False,
            'withoutSellerResponses': False,
            'buyRequestIDs': [],
            'suggestionSources': [],
        },
        'parcelSearch': {
            'pieces': {
                'piecesPerCaratFrom': None,
                'piecesPerCaratTo': None,
            },
            'parcelTypes': [],
            'sieve': {
                'sieveFrom': None,
                'sieveTo': None,
            },
        },
        'instantInventory': {
            'isFilled': False,
            'onlyWithMedia': False,
        },
        'projection': {
            'include': [
                'Diamond ID',
                'Availability',
                'Seller',
                'Rating',
                'Location',
                'Shape',
                'Size',
                'Color',
                'Clarity',
                'Cut',
                'Polish',
                'Symmetry',
                'Fluorescence',
                'Lab',
                '$/ct',
                '%Rap',
                'Total',
                'Media',
                'Ratio',
                'Depth',
                'Table',
                'Measurements',
                'Diamond Type',
            ],
            'displayMode': 'display',
        },
        'isBuyNowSearch': False,
    },
    'searchType': 'Search',
}
    params = {
        'Start': str(start),
        'Size': str(PAGE_SIZE),
        'di': '01e8a701-6d20-cb21-5aaa-9a4dba288c2d',
        'version': 'production_version_2024-12-23_10-53',
    }

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.post(
                'https://diamondsearch.gwapi.rapnet.com/diamondsearch/api/Diamonds/search',
                headers=headers,
                params=params,
                json=json_data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{MAX_ATTEMPTS} failed: {e}")
            if attempt == MAX_ATTEMPTS - 1:
                raise
            time.sleep(5)

def main():
    all_diamonds = load_existing_data(OUTPUT_FILE)
    start = 1
    page_number = 1

    while True:
        print(f"Fetching page {page_number}...")
        try:
            data = fetch_diamonds(page_number, start)
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            break

        parcels = data.get("data", {}).get("diamonds", [])
        if not parcels:
            print(f"No more diamonds found. Ending at page {page_number}.")
            break

        new_diamonds = {parcel.get('diamondID') for parcel in parcels}
        all_diamonds.update(new_diamonds)

        print(f"Page {page_number} processed. Diamonds fetched: {len(new_diamonds)}. Total: {len(all_diamonds)}.")
        page_number += 1
        start += PAGE_SIZE

    save_data(OUTPUT_FILE, all_diamonds)
    print(f"Total diamonds saved: {len(all_diamonds)}.")

if __name__ == "__main__":
    main()
