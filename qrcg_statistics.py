# qrcg_statistics.py

import os
import requests
import csv
import re
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from datetime import datetime
from granular_statistics import process_qr_codes  # Import the granular script function

# Initialize the rich console for pretty output in terminal
console = Console()

# Helper function to remove rich formatting from text for CSV output
def remove_rich_formatting(text):
    return re.sub(r'\[.*?\]', '', text)

# Main function to fetch QR code data from the QRCG API
def fetch_qr_codes(access_token, start_date, end_date):
    # Initialize counters for static and dynamic QR codes
    static_qr_count = 0
    dynamic_qr_count = 0

    # Set up the base URL for the QRCG API with the provided access token
    base_url = f"https://api.qr-code-generator.com/v1/codes?access-token={access_token}"
    qr_codes = []  # This will store all QR code data fetched
    page = 1
    total_scans_all_time = 0  # Total scans for dynamic QR codes
    qr_code_data = []  # List to store the QR code data to be written to CSV

    max_pages = 50000  # Maximum number of pages to fetch

    # Fetch QR codes in batches (pagination) and handle API response
    with console.status("[bold green]Fetching QR codes...") as status:
        for page in range(1, max_pages + 1):
            url = f"{base_url}&page={page}"
            try:
                response = requests.get(url)
                # Check if the API request was successful
                if response.status_code != 200:
                    console.print(Panel.fit(
                        f"[red]Failed to fetch QR codes[/red]\n[bold]Status Code:[/bold] {response.status_code}\n[bold]Response:[/bold] {response.text}"))
                    return

                # Parse the response data
                data = response.json()
                qr_codes_page = data if isinstance(data, list) else data.get("data", [])

                # If no QR codes are found, exit
                if not qr_codes_page:
                    console.print("[yellow]No QR codes found.[/yellow]")
                    return

                # Add newly fetched QR codes to the list
                qr_codes.extend(qr_codes_page)

                # If fewer than 20 QR codes are returned, we've likely reached the last page
                if len(qr_codes_page) < 20:
                    break
            except Exception as e:
                console.print(f"[bold red]An error occurred while fetching page {page}:[/bold red] {e}")
                break

    # Process the fetched QR codes
    with console.status("[bold green]Processing QR codes...") as status:
        for qr in qr_codes:
            # Extract information for each QR code
            id = qr.get("id", "N/A")
            created = qr.get("created", "N/A")
            title = qr.get("title", None)
            short_url = qr.get("short_url", "")
            target_url = qr.get("target_url")
            type_name = qr.get("type_name", "Unknown")
            total_scans = qr.get("total_scans", 0)
            unique_scans = qr.get("unique_scans", 0)

            # Check if the QR code is dynamic (based on the presence of a short URL)
            is_dynamic = bool(short_url)
            qr_code_type = "Dynamic" if is_dynamic else "Static"
            qr_type_display = f"{qr_code_type} - {type_name}"

            # Default title if not available
            if not title:
                title = target_url if target_url else f"My {type_name}"

            # Convert the creation date into a datetime object
            try:
                if 'T' in created:
                    qr_date = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S.%fZ")
                else:
                    qr_date = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                qr_date = None

            # Filter QR codes by date range (if specified)
            if qr_date and start_date != "all time" and end_date != "all time":
                if qr_date < start_date or qr_date > end_date:
                    continue

            # Count dynamic and static QR codes
            if is_dynamic:
                dynamic_qr_count += 1
                hide_scans = False  # Show scan data for dynamic QR codes
            else:
                static_qr_count += 1
                hide_scans = True  # Hide scan data for static QR codes

            # Prepare output text for displaying in the console
            short_url_display = short_url if short_url else "[red]No Short URL - Static[/red]"
            target_url_display = target_url if target_url else f"[red]No Target URL - {type_name}[/red]"

            output = (
                f"[bold]ID:[/bold] {id}\n"
                f"[bold]Created:[/bold]{created}\n"
                f"[bold]Short URL:[/bold] [cyan]{short_url_display}[/cyan]\n"
                f"[bold]Target URL:[/bold] [cyan]{target_url_display}[/cyan]\n"
                f"[bold]Type:[/bold] {qr_type_display}"
            )

            # Display scan data for dynamic QR codes
            if not hide_scans:
                output += (
                    "\n"
                    f"[bold]Total Scans:[/bold] {total_scans}\n"
                    f"[bold]Unique Scans:[/bold] {unique_scans}"
                )

            # Print the formatted QR code info in the console
            console.print()
            console.print(Panel(output, title=f"[bold]{title}[/bold]", expand=False))

            # Prepare row data for CSV export
            row = {
                "ID": remove_rich_formatting(str(id)),
                "Created": remove_rich_formatting(created),
                "Title": remove_rich_formatting(title),
                "Short URL": remove_rich_formatting(short_url),
                "Target URL": remove_rich_formatting(target_url),
                "Solution Type": remove_rich_formatting(type_name),
                "QR Code Type": qr_code_type,
                "Total Scans": remove_rich_formatting(str(total_scans)) if is_dynamic else "",
                "Unique Scans": remove_rich_formatting(str(unique_scans)) if is_dynamic else "",
            }

            # Append QR code data for CSV export
            qr_code_data.append(row)

            # Accumulate total scans for dynamic QR codes
            if is_dynamic and isinstance(total_scans, int):
                total_scans_all_time += total_scans

    # Display summary statistics for the fetched QR codes
    console.print(f"\n[bold magenta]Total number of Static QR Codes:[/bold magenta] [cyan]{static_qr_count}[/cyan]")
    console.print(f"[bold magenta]Total number of Dynamic QR Codes:[/bold magenta] [cyan]{dynamic_qr_count}[/cyan]")
    console.print(f"\n[bold magenta]Aggregate Total Scans for all Dynamic QR Codes:[/bold magenta] [cyan]{total_scans_all_time}[/cyan]\n")

    # Prompt user if they want to download the QR code data as CSV
    download_csv = Prompt.ask("[bold cyan]📥 Do you want to download the data as CSV? (y/n)", default=None)
    if download_csv is None:
        download_csv = 'n'

    # If user chooses to download CSV
    if download_csv.lower() == "y":
        # Define folder and file name for CSV export
        folder_name = "QRCG STATISTICS EXPORTS"

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = os.path.join(folder_name, f"qrcg_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

        # Define CSV columns
        fieldnames = [
            "ID", "Created", "Title", "Short URL", "Target URL",
            "Solution Type", "QR Code Type",
            "Total Scans", "Unique Scans"
        ]

        # Write QR code data to the CSV file
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(qr_code_data)

        # Confirm successful CSV export
        console.print(f"[bold green]CSV file '{filename}' has been successfully saved![/bold green]")

        # Ask user if they want to download granular data for each QR Code
        download_granular = Prompt.ask("[bold cyan]📥 Would you like to download granular data for each QR Code (y/n)?", default=None)
        if download_granular.lower() == "y":
            # Trigger the granular statistics download
            console.print("[bold green]Starting the granular data download...[/bold green]")
            process_qr_codes(filename, access_token, "GRANULAR STATISTICS EXPORTS")  # Triggering granular statistics

# Main entry point of the script
if __name__ == "__main__":
    console.print("[bold cyan]📱 QRCG API: Bulk QR Code Statistics[/bold cyan]")

    # Prompt user for API access token
    access_token = Prompt.ask("[bold green]🔑 Enter your API access token[/bold green]")

    # Prompt user to specify date range for QR code search
    specify_date_range = Prompt.ask("[bold cyan]📅 Would you like to specify date ranges (y/n)?[/bold cyan]", default="n").lower()

    # If user wants to specify date range, parse start and end dates
    if specify_date_range == "y":
        start_date_input = Prompt.ask("[bold cyan]⏩ 📅 Search for QR Codes created from (YYYY-MM-DD)[/bold cyan]")
        end_date_input = Prompt.ask("[bold cyan]📅 ⏪ Search for QR Codes created until (YYYY-MM-DD)[/bold cyan]")

        if start_date_input != "all time":
            start_date = datetime.strptime(start_date_input, "%Y-%m-%d")
        else:
            start_date = "all time"

        if end_date_input != "all time":
            end_date = datetime.strptime(end_date_input, "%Y-%m-%d")
        else:
            end_date = "all time"
    else:
        start_date = "all time"
        end_date = "all time"

    # Call the fetch_qr_codes function to begin processing
    fetch_qr_codes(access_token, start_date, end_date)
