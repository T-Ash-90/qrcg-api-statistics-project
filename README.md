# QR Code Generator - Bulk QR Code Statistics

A Python script that allows you to fetch, analyze, and export QR code data from the [QR Code Generator API](https://www.qr-code-generator.com/) using your access token. This tool can retrieve static and dynamic QR codes, display detailed statistics, and export the data to a CSV file.

## Features

- Fetches all QR codes (static and dynamic) from the QR Code Generator API.
- Filters QR codes by creation date (optional).
- Displays QR code details, including title, short URL, target URL, total scans, and unique scans.
- Optionally exports the fetched QR code data to a CSV file.

## Requirements

- Python 3.6 or higher
- The following Python packages:
  - `requests`
  - `rich`

---

## Setup & Usage

1. Clone the repository or download the script.

2. Ensure you have your **QR Code Generator API access token**. You can get it from your paid QRCG account [QR Code Generator's API section](https://www.qr-code-generator.com/). The token is required for authenticating API requests.

3. Run the script: **python3 qrcg_statistics.py**

4. The script will prompt you to **enter your API access token**

5. Optionally specify a date range to filter the QR codes by creation date.

6. The script will fetch and display all each QR codes:
   - **Created**: The date and time when the QR code was created.
   - **Short URL**: A shortened URL for the QR code.
   - **Target URL**: The target URL the QR code redirects to (or a fallback message if it’s missing).
   - **Type**: The type of the QR code (Dynamic/Static - URL, SMS, vCard etc.).
   - **Total Scans**: Total number of scans for the QR code.
   - **Unique Scans**: Number of unique scans.

7. After displaying all QR codes, the script will show the **total scans** across all QR codes that were created within the date range you specified (or for all time if no range is set).

---

## CSV Export

After displaying the QR code data in the terminal, the script will prompt if you want to export the data to a CSV file (y/n).

If you choose `y`, the script will create a CSV file with the following columns:
- **Created**: The creation date of the QR code.
- **Title**: The title of the QR code.
- **Short URL**: The short URL for the QR code.
- **Target URL**: The target URL for the QR code.
- **Solution Type**: The type of the QR code (e.g., URL, SMS, etc.).
- **QR Code Type**: Dynamic or Static
- **Total Scans**: Total number of scans.
- **Unique Scans**: Number of unique scans.

## Troubleshooting

- If you encounter any errors related to the API request, double-check your API access token and ensure it’s valid.
- If the script doesn't return all the QR codes, check for any pagination issues.
- If you get an error related to date parsing, make sure your date inputs are in the correct format (`YYYY-MM-DD`).
