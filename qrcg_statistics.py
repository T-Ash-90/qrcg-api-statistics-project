import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from datetime import datetime

# Initialize console
console = Console()

def fetch_qr_codes(access_token, start_date, end_date):
    base_url = f"https://api.qr-code-generator.com/v1/codes?access-token={access_token}"
    qr_codes = []
    page = 1  # Starting with the first page
    total_scans_all_time = 0  # Variable to hold total scans for all QR codes

    while True:
        # Construct the URL with pagination (page number)
        url = f"{base_url}&page={page}"

        try:
            response = requests.get(url)

            if response.status_code != 200:
                console.print(Panel.fit(f"[red]Failed to fetch QR codes[/red]\n[bold]Status Code:[/bold] {response.status_code}\n[bold]Response:[/bold] {response.text}"))
                return

            # Get the response data
            data = response.json()

            # Check if data is a list (instead of a dictionary)
            if isinstance(data, list):
                qr_codes_page = data
            elif isinstance(data, dict):
                qr_codes_page = data.get("data", [])
            else:
                console.print("[red]Unexpected data format![/red]")
                return

            if not qr_codes_page:
                console.print("[yellow]No QR codes found.[/yellow]")
                return

            # Add the current page's QR codes to the overall list
            qr_codes.extend(qr_codes_page)

            # Check if there is a next page, if not, break the loop
            if len(qr_codes_page) < 20:  # Assuming 20 is the max number of QR codes per page
                break  # No more pages to fetch
            else:
                page += 1  # Move to the next page

        except Exception as e:
            console.print(f"[bold red]An error occurred:[/bold red] {e}")
            break

    # Loop through each QR code and display the required fields
    for qr in qr_codes:
        created = qr.get("created", "N/A")
        title = qr.get("title", "Untitled")
        short_url = qr.get("short_url", "")
        target_url = qr.get("target_url")
        type_name = qr.get("type_name", "Unknown")
        total_scans = qr.get("total_scans", 0)
        unique_scans = qr.get("unique_scans", 0)

        # Parse the 'created' date field (handle both formats)
        try:
            if 'T' in created:  # If the format is '2023-08-11T13:13:29.123Z'
                qr_date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:  # If the format is '2025-08-11 13:13:29'
                qr_date = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            qr_date = None  # If parsing fails, skip this QR code

        # If the QR code is within the date range, process it
        if qr_date:
            if start_date != "all time" and end_date != "all time":
                if qr_date < start_date or qr_date > end_date:
                    continue  # Skip this QR code if it's outside the date range

        # Handle missing short URL (Static QR Code)
        if not short_url:
            short_url = "[italic red]No Short URL - This is a Static QR Code[/italic red]"
            total_scans = "[italic red]N/A[/italic red]"  # No scans for static QR codes
            unique_scans = "[italic red]N/A[/italic red]"  # No unique scans for static QR codes

        # Handle missing target URL
        if not target_url:
            target_url_display = f"[italic red]No Target URL, as this is a {type_name} QR Code[/italic red]"
        else:
            target_url_display = target_url

        # Format the output in the desired order
        output = (
            f"[bold]Created:[/bold] {created}\n"
            f"[bold]Title:[/bold] {title}\n"
            f"[bold]Short URL:[/bold] {short_url}\n"
            f"[bold]Target URL:[/bold] {target_url_display}\n"
            f"[bold]Type:[/bold] {type_name}\n"
            f"[bold]Total Scans:[/bold] {total_scans}\n"
            f"[bold]Unique Scans:[/bold] {unique_scans}"
        )

        # Display the result in a nice panel format
        console.print(Panel(output, title=f"QR Code: {title}", expand=False))

        # Sum up the total scans for all QR codes
        if isinstance(total_scans, int):
            total_scans_all_time += total_scans

    # Display the total scans summary
    console.print(f"\n[bold green]Total Scans for all QR Codes: {total_scans_all_time}[/bold green]")

if __name__ == "__main__":
    console.print("[bold cyan]QR Code Generator API Data Fetcher[/bold cyan]")

    # Ask the user for the API key
    access_token = Prompt.ask("🔑 Enter your API access token")

    # Ask for the date range (defaults to 'all time' if not specified)
    start_date_input = Prompt.ask("📅 Enter start date (YYYY-MM-DD) or leave blank for all time", default="all time")
    end_date_input = Prompt.ask("📅 Enter end date (YYYY-MM-DD) or leave blank for all time", default="all time")

    # If user provides a valid date range, convert them to datetime objects
    if start_date_input != "all time":
        start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
    else:
        start_date = "all time"  # Keep as 'all time' if the user doesn't specify a start date

    if end_date_input != "all time":
        end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
    else:
        end_date = "all time"  # Keep as 'all time' if the user doesn't specify an end date

    # Fetch QR codes and show the data
    fetch_qr_codes(access_token, start_date, end_date)
