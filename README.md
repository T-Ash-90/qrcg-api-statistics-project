# QR Code Generator API Data Fetcher

A simple Python script that fetches QR code data from the [QR Code Generator API](https://www.qr-code-generator.com/), parses the data, and displays it in a clean and readable format in the terminal.

### Features:
- Fetches a list of QR codes from your account.
- Supports pagination to retrieve all QR codes (even beyond the first 20).
- Displays QR code information, including:
  - Created date
  - Title
  - Short URL
  - Target URL
  - Type
  - Total scans
  - Unique scans
- Handles missing target URLs by displaying a fallback message.
- **Filter QR codes by date range**: You can now filter QR codes based on a start and end date.
  - The default date range is "all time," but you can specify a custom start and end date in the format `YYYY-MM-DD`.
- **Total scans summary**: Displays the total number of scans for all QR codes within the selected date range or for all QR codes if no range is specified.

---

## Requirements

- **Python 3.6+**
- **Required Libraries**:
  - `requests`: For making API requests.
  - `rich`: For formatting and displaying output in the terminal.

You can install the necessary dependencies using `pip`:

  pip install requests rich

---

## Setup

1. Clone the repository or download the script

2. Ensure you have your **QR Code Generator API access token**. You can get it from [QR Code Generator's API section](https://www.qr-code-generator.com/). The token is required for authenticating API requests.

---

## Usage

1. Run the script:

    python3 qrcg_statistics.py

2. The script will prompt you to **enter your API access token**:

    🔑 Enter your API access token

   Paste your token and press `Enter`.

3. The script will then prompt you to **enter a start and end date** for filtering the QR codes (or leave the fields blank for "all time"):

    📅 Enter start date (YYYY-MM-DD) or leave blank for all time (all time):
    📅 Enter end date (YYYY-MM-DD) or leave blank for all time (all time):

4. The script will fetch and display all your QR codes, formatted as follows:
   - **Created**: The date and time when the QR code was created.
   - **Title**: The title of the QR code.
   - **Short URL**: A shortened URL for the QR code.
   - **Target URL**: The target URL the QR code redirects to (or a fallback message if it’s missing).
   - **Type**: The type of the QR code (e.g., URL, SMS, etc.).
   - **Total Scans**: Total number of scans for the QR code.
   - **Unique Scans**: Number of unique scans.

   If any QR code does not have a **target URL**, the script will display:

    No Target URL, as this is a <Type> QR Code

5. After displaying all the QR codes, the script will show the **total scans** across all QR codes within the date range you specified (or for all time if no range is set).

---

## Example Output:

    QR Code Generator API Data Fetcher
    Enter your API access token: ***************

    📦 Sample QR Code Title
    ────────────────────────────────────────
    Created: 2023-08-15T10:22:30Z
    Title: Sample QR Code Title
    Short URL: https://short.url/sample
    Target URL: https://example.com
    Type: URL
    Total Scans: 100
    Unique Scans: 50

    📦 Another QR Code Title
    ────────────────────────────────────────
    Created: 2023-08-14T08:10:20Z
    Title: Another QR Code Title
    Short URL: https://short.url/another
    Target URL: No Target URL, as this is a SMS QR Code
    Type: SMS
    Total Scans: 200
    Unique Scans: 150

    [bold green]Total Scans for all QR Codes: 300[/bold green]

---

## Notes

- The script **automatically handles pagination** if there are more than 20 QR codes in your account, fetching all pages of results.
- If no QR codes are found, the script will print "No QR codes found."
- You can **filter QR codes by date range** by entering specific start and end dates (in `YYYY-MM-DD` format). If no date range is provided, the script will consider all QR codes ever created.
- The API limits the number of requests you can make, so be mindful of your request rate.

---

## Troubleshooting

- If you encounter any errors related to the API request, double-check your API access token and ensure it’s valid.
- If the script doesn't return all the QR codes, make sure you have more than 20 QR codes and check for any pagination issues.
- If you get an error related to date parsing, make sure your date inputs are in the correct format (`YYYY-MM-DD`).
