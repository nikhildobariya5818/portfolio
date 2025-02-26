import json,csv,os

def json_to_csv():
    # Load JSON data
    with open('product_details.json', 'r',encoding='utf-8') as file:
        data = json.load(file)

    # Prepare the CSV file
    csv_file = 'outpt.csv'

    # Extract dynamic attribute keys
    attribute_keys = set()
    for item in data:
        attribute_keys.update(set(item.keys()) - {"title", "SKU", "category", "price", "List Price", "images", "description"})

    attribute_keys = sorted(attribute_keys)

    # Define CSV headers
    headers = [
        "ID", "Type", "SKU", "Name", "Published", "Is featured?", "Visibility in catalog",
        "Short description", "Description", "Date sale price starts", "Date sale price ends", "Tax status",
        "Tax class", "In stock?", "Stock", "Low stock amount", "Backorders allowed?", "Sold individually?",
        "Weight (kg)", "Length (cm)", "Width (cm)", "Height (cm)", "Allow customer reviews?", "Purchase note",
        "Sale price", "Regular price", "Categories", "Tags", "Shipping class", "Images",
        "Download limit", "Download expiry days", "Parent", "Grouped products", "Upsells", "Cross-sells",
        "External URL", "Button text", "Position"
    ]

    # Add dynamic attributes to headers
    for i, attribute in enumerate(attribute_keys, start=1):
        headers.extend([
            f"Attribute {i} name",
            f"Attribute {i} value(s)",
            f"Attribute {i} visible",
            f"Attribute {i} global",
        ])

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for idx, item in enumerate(data, start=1):
            row = [
                idx, "Simple", item.get("SKU", ""), item.get("title", ""), "Yes", "No", "Visible",
                "", item.get("description", ""), "", "", "Taxable", "", "In stock", "", "", "No",
                "No", "", item.get("Length", ""), "", "", "Yes", "", item.get("Regular price", ""), item.get("List Price", ""),
                item.get("category", ""), "", "", ", ".join(item.get("images", [])), "", "", "", "", "", "", "", "", ""
            ]

            # Append dynamic attributes
            for attribute in attribute_keys:
                row.extend([
                    attribute,
                    item.get(attribute, ""),
                    "Yes" if attribute in item else "No",
                    "Yes"
                ])

            writer.writerow(row)

    print(f"CSV file '{csv_file}' created successfully.")


def split_csv():
    # Ensure the output folder exists
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Read the CSV file
    with open('outpt.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)
        rows = list(reader)

    # Split the CSV file based on categories
    categories = set(row[headers.index("Categories")] for row in rows)
    print(len(categories))
    for category in categories:
        # Create a CSV file for each category inside the output folder
        category_file = os.path.join(output_folder, f"{category}.csv")
        with open(category_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)

            for row in rows:
                if row[headers.index("Categories")] == category:
                    writer.writerow(row)

        print(f"CSV file '{category_file}' created successfully.")


if __name__ == "__main__":
    json_to_csv()
    split_csv()
    # pass