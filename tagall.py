"""
WhatsApp Tag All Tool
A simple Windows tool to automatically tag all members in a WhatsApp group using @all.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


class WhatsAppTagAll:
    def __init__(self):
        """Initialize the WhatsApp Tag All tool."""
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Set up Chrome WebDriver with appropriate options."""
        print("Setting up Chrome WebDriver...")
        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=./User_Data")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 30)
        
    def open_whatsapp(self):
        """Open WhatsApp Web."""
        print("Opening WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        print("Please scan the QR code to log in to WhatsApp Web.")
        print("Waiting for WhatsApp to load...")
        
        try:
            # Wait for the main page to load (search box appears when logged in)
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("WhatsApp Web loaded successfully!")
            time.sleep(2)
        except TimeoutException:
            print("Timeout waiting for WhatsApp to load. Please check your connection and try again.")
            raise
            
    def select_group(self, group_name):
        """Select a WhatsApp group by name."""
        print(f"Searching for group: {group_name}")
        
        try:
            # Click on search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.click()
            time.sleep(1)
            
            # Type group name
            search_box.send_keys(group_name)
            time.sleep(2)
            
            # Click on the first result
            group = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{group_name}"]'))
            )
            group.click()
            print(f"Group '{group_name}' selected successfully!")
            time.sleep(2)
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error: Could not find group '{group_name}'. Please check the group name and try again.")
            raise
            
    def send_tag_all_message(self, message=""):
        """Send a message with @all tag to the group."""
        print("Sending @all message...")
        
        try:
            # Find the message input box
            message_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            message_box.click()
            time.sleep(1)
            
            # Type @all
            message_box.send_keys("@all")
            time.sleep(1)
            
            # Press Enter to select the @all tag
            message_box.send_keys(Keys.ENTER)
            time.sleep(1)
            
            # Add custom message if provided
            if message:
                message_box.send_keys(f" {message}")
                time.sleep(1)
            
            # Send the message
            message_box.send_keys(Keys.ENTER)
            print("Message sent successfully!")
            time.sleep(2)
            
        except (TimeoutException, NoSuchElementException) as e:
            print(f"Error sending message: {e}")
            raise
            
    def close(self):
        """Close the WebDriver."""
        if self.driver:
            print("Closing browser...")
            self.driver.quit()
            
    def run(self, group_name, message=""):
        """Main method to run the tag-all process."""
        try:
            self.setup_driver()
            self.open_whatsapp()
            self.select_group(group_name)
            self.send_tag_all_message(message)
            
            print("\n✓ Successfully tagged all members in the group!")
            print("Press Enter to close the browser...")
            input()
            
        except Exception as e:
            print(f"\n✗ An error occurred: {e}")
            print("Press Enter to close the browser...")
            input()
        finally:
            self.close()


def main():
    """Main function to run the WhatsApp Tag All tool."""
    print("=" * 50)
    print("WhatsApp Tag All Tool")
    print("=" * 50)
    print()
    
    # Get group name from user
    group_name = input("Enter the WhatsApp group name: ").strip()
    
    if not group_name:
        print("Error: Group name cannot be empty!")
        return
    
    # Get optional message
    custom_message = input("Enter a message (optional, press Enter to skip): ").strip()
    
    print("\nStarting WhatsApp Tag All tool...")
    print()
    
    # Create and run the tool
    tool = WhatsAppTagAll()
    tool.run(group_name, custom_message)


if __name__ == "__main__":
    main()
