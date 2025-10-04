# tagAll-Whatsapp

A simple Windows tool to automatically tag all members in a WhatsApp group using `@all`.

## Features

- 🚀 Automatically tag all group members with `@all`
- 💬 Add custom messages along with the tag
- 🔐 Uses WhatsApp Web for secure authentication
- 🖥️ Simple command-line interface

## Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- Active WhatsApp account
- Internet connection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Sandinu/tagAll-Whatsapp.git
cd tagAll-Whatsapp
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the script:
```bash
python tagall.py
```

2. Enter the WhatsApp group name when prompted

3. (Optional) Enter a custom message to send along with the `@all` tag

4. On first run, scan the QR code with your phone to log in to WhatsApp Web

5. The tool will automatically:
   - Open WhatsApp Web
   - Search for your group
   - Send a message with `@all` tag
   - Tag all group members

## How It Works

1. The tool opens WhatsApp Web using Selenium WebDriver
2. After you scan the QR code, it searches for the specified group
3. It types `@all` in the message box
4. Adds your custom message (if provided)
5. Sends the message to tag all group members

## Important Notes

- ⚠️ This tool uses WhatsApp Web automation. Use it responsibly and in accordance with WhatsApp's Terms of Service
- 🔒 Your WhatsApp session is stored locally in the `User_Data` folder for convenience
- 📱 You need to scan the QR code only on the first run
- ⏱️ Make sure you have a stable internet connection
- 👥 You must be a member of the group you want to tag

## Troubleshooting

### Chrome driver issues
If you encounter Chrome driver issues, make sure you have the latest version of Google Chrome installed. The tool will automatically download the appropriate ChromeDriver.

### Group not found
Make sure you type the exact group name as it appears in WhatsApp.

### QR code timeout
If the QR code times out, just restart the script and scan again.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for educational purposes only. Please use it responsibly and respect WhatsApp's Terms of Service and community guidelines. The developers are not responsible for any misuse of this tool.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## Author

Sandinu Pinnawala