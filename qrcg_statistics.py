import requests
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

# Initialize console
console = Console()

def fetch_qr_codes(access_token):
    base_url = f"https://api.qr-code-generator.com/v1/codes?access-token={access_token}"
    qr_codes = []
    page = 1  # Starting with the first page

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

        # Handle missing short URL (Static QR Code)
        if not short_url:
            short_url = "[italic red]No Short URL - This is a Static QR Code[/italic red]"
            total_scans = "[italic red]N/A[/italic red]"  # No scans for static QR codes
            unique_scans = "[italic red]N/A[/italic red]"  # No unique scans for static QR codes

        # Handle missing target URL
        if not target_url:
            target_url_display = f"[italic red]No Target URL - This is a {type_name} QR Code[/italic red]"
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

if __name__ == "__main__":
    console.print("[bold cyan]QR Code Generator API Data Fetcher[/bold cyan]")
    access_token = Prompt.ask("🔑 Enter your API access token")
    fetch_qr_codes(access_token)
