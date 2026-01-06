# Homebox Epson Label Creator

A Python tool to automatically generate QR code labels for your Homebox inventory items, compatible with the Epson LW-C410 label printer.

## About

### What is Homebox?
[Homebox](https://github.com/hay-kot/homebox) is a self-hosted home inventory and organization system. It allows you to track your belongings, their locations, values, and other metadata through a web interface.

### What is the Epson LW-C410?
The Epson LW-C410 is a portable label printer designed for creating custom labels with text, barcodes, and QR codes. This project generates label files in the `.lemd` format that can be used with the Epson Label Editor software for the LW-C410.

## Features

- Fetches all items from your Homebox instance via API
- Generates QR code labels linking to each item's Homebox page
- Customizable item names on labels (with interactive prompts)
- Skips already-generated labels to avoid duplicates
- Outputs labels in Epson Label Editor format (`.lemd`)

## Prerequisites

- Python 3.13 or higher
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- A running Homebox instance
- Epson Label Editor software (for printing the generated labels)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd homebox_epson_labelCreator
```

2. Install dependencies using uv:
```bash
uv sync
```

## Configuration

1. Copy the `.env.template` file to `.env`:
```bash
cp .env.template .env
```

2. Edit `.env` with your Homebox details:
```env
base_url="https://your-homebox-instance.com"
auth_code="your-auth-token"
```

**Note:** To get your auth token:
- Open your Homebox instance in a browser
- Log in and open browser developer tools (F12)
- Go to the Network tab, make a request, and copy the `Authorization` header value from any API request

## Usage

Run the label creator using uv:

```bash
uv run create_label.py
```

The script will:
1. Fetch all items from your Homebox instance
2. For each item not yet processed, prompt you for a label name (press Enter to use the item's full name)
3. Generate a `.lemd` label file in the `created_tags/` directory
4. Skip items that already have generated labels
5. Import the `.lemd` files in your Epson Mobile app

## Label Template (base_tag.lemd)

The `base_tag.lemd` file is a JSON template that defines the label layout for the Epson printer. It contains two placeholders that are automatically replaced:

### Placeholders

- **`ITEMURL`**: Replaced with the item's Homebox URL path (e.g., `/item/123`)
  - The URL is automatically escaped for JSON (slashes become `\/`)
  - This creates a QR code that links directly to the item in Homebox

- **`TEXTPLACEHOLDER`**: Replaced with the item name you specify
  - Can be customized during generation or defaults to the item's full name
  - Appears as text on the label next to the QR code

### Label Layout

The template defines a 12mm x 15mm label with:
- A QR code containing the full Homebox item URL
- Text label rotated 270 degrees
- Auto-length enabled for flexible label sizes

You can customize the template by editing `base_tag.lemd` in the Epson Label Editor software and ensuring the placeholders remain intact.

## Output

Generated labels are saved to `created_tags/` with the item ID as the filename. These `.lemd` files can be:
- Opened in Epson Label Editor
- Printed directly to your Epson LW-C410 printer
- Batch printed for multiple items

## TODOs

The following improvements are planned:

1. **Authentication**: Implement proper login flow or API key configuration instead of using browser cookie auth token (see `create_label.py:32`)
2. **Error Handling**: Add better error handling for malformed CSV data and network issues (see `create_label.py:43`)

## Troubleshooting

### SSL Certificate Warnings
The script currently disables SSL verification warnings. If you're using a self-hosted Homebox instance with a self-signed certificate, this is expected. For production use, consider using proper SSL certificates.

### Missing Items
If items aren't being processed:
- Check that your auth token is valid
- Verify your Homebox instance is accessible
- Ensure the CSV export endpoint is available at `/api/v1/items/export`

### Label Files Not Printing
- Ensure you have Epson Label Editor installed
- Verify your LW-C410 printer is connected and recognized
- Check that the label tape size matches the template (12mm width)

## License

[Add your license here]

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
