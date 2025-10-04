"""
WhatsApp @all Auto-Tagger - System Tray Application
Author: Sandinu Pinnawala
Version: 1.0.0

A Windows system tray application that automatically tags all members 
in a WhatsApp group when you type @all.

Requirements:
pip install pyautogui pyperclip keyboard pillow pygetwindow pystray

To create EXE:
pip install pyinstaller
pyinstaller --onefile --windowed --name="WhatsApp-AutoTagger" whatsapp_tagger.py
"""

import pyautogui
import pyperclip
import keyboard
import time
import pygetwindow as gw
import tkinter as tk
import tkinter as tk
from tkinter import ttk
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import sys

# Configuration
TYPING_DELAY = 0.01  # Reduced from 0.05
MEMBER_DELAY = 0.1  # Reduced from 0.4 - main speed improvement!
MAX_MEMBERS = 1000    # Maximum members to tag (adjust based on your group size)

# Author info
__author__ = "Sandinu Pinnawala"
__version__ = "1.0.0"

class ProgressPopup:
    """
    A floating progress popup that stays on top.
    """
    def __init__(self):
        self.root = None
        self.label = None
        self.progress_bar = None
        self.status_label = None
        self.should_stop = False
        
    def create(self, max_value):
        """Create the popup window."""
        self.root = tk.Tk()
        self.root.title(f"@TagAll v{__version__}")
        self.root.geometry("380x170")
        self.root.attributes('-topmost', True)  # Always on top
        self.root.overrideredirect(False)  # Show window frame
        # Set icon for taskbar and title bar
        import os
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.ico')
        try:
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not set icon: {e}")
        
        # Position in bottom right corner
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = screen_width - 400
        y = screen_height - 220
        self.root.geometry(f"+{x}+{y}")
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Custom.Horizontal.TProgressbar", 
                       troughcolor='#e0e0e0',
                       background='#4CAF50',
                       thickness=20)
        
        # Main frame
        frame = tk.Frame(self.root, bg='#2d2d2d', padx=20, pady=20)
        frame.pack(fill='both', expand=True)
        
        # Title
        title = tk.Label(frame, text="🚀 Tagging Members", 
                        font=('Segoe UI', 14, 'bold'),
                        bg='#2d2d2d', fg='#ffffff')
        title.pack(pady=(0, 5))
        
        # Author label
        author = tk.Label(frame, text=f"by {__author__}", 
                         font=('Segoe UI', 8),
                         bg='#2d2d2d', fg='#888888')
        author.pack(pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(frame, text="Starting...", 
                                     font=('Segoe UI', 10),
                                     bg='#2d2d2d', fg='#cccccc')
        self.status_label.pack(pady=(0, 10))
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(frame, 
                                           length=320, 
                                           mode='determinate',
                                           maximum=max_value,
                                           style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(pady=(0, 10))
        
        # Progress label
        self.label = tk.Label(frame, text="0 / 0", 
                             font=('Segoe UI', 9),
                             bg='#2d2d2d', fg='#aaaaaa')
        self.label.pack()
        
        # Update window
        self.root.update()
        self.root.iconbitmap('app_icon.ico')
    
    def on_close(self):
        """Handle window close button click."""
        self.should_stop = True
        print("\n⚠️  User cancelled tagging process!")
        self.close()
        
    def update(self, current, total, status="Tagging..."):
        """Update progress."""
        if self.root:
            try:
                self.progress_bar['value'] = current
                self.label.config(text=f"{current} / {total}")
                self.status_label.config(text=status)
                self.root.update()
            except:
                pass
    
    def complete(self, message="✅ Done!"):
        """Show completion message."""
        if self.root:
            try:
                self.status_label.config(text=message, fg='#4CAF50')
                self.root.update()
                time.sleep(2)
            except:
                pass
            self.close()
    
    def close(self):
        """Close the popup."""
        if self.root:
            try:
                self.root.destroy()
            except:
                pass
            self.root = None

def focus_whatsapp():
    """
    Automatically focus WhatsApp window.
    """
    try:
        # Find WhatsApp window
        windows = gw.getWindowsWithTitle('WhatsApp')
        if windows:
            whatsapp_window = windows[0]
            whatsapp_window.activate()
            time.sleep(0.3)
            return True
        else:
            print("⚠️  WhatsApp window not found!")
            return False
    except Exception as e:
        print(f"⚠️  Could not focus WhatsApp: {e}")
        return False

def tag_all_members(message_text):
    """
    Automatically tag all members in the current WhatsApp group.
    """
    print("\n🚀 Starting auto-tag process...")
    
    # Focus WhatsApp window
    if not focus_whatsapp():
        print("❌ Please open WhatsApp Desktop first!")
        return
    
    print("✓ WhatsApp focused!")
    time.sleep(0.3)  # Reduced from 0.5
    
    # Remove @all from the message
    clean_message = message_text.replace('@all', '').replace('@ALL', '').strip()
    
    # Clear current text
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.02)  # Reduced from 0.1
    pyautogui.press('delete')
    time.sleep(0.05)  # Reduced from 0.3
    
    # Create progress popup
    popup = ProgressPopup()
    popup.create(MAX_MEMBERS)
    popup.update(0, MAX_MEMBERS, "⚠️ Don't touch keyboard/mouse!")
    
    print(f"📝 Tagging unique members (will auto-stop when list repeats)...")
    
    tagged_count = 0
    seen_tags = set()  # Track unique tags to avoid duplicates
    consecutive_duplicates = 0
    
    # Loop to tag members
    for i in range(MAX_MEMBERS):
        # Check if user closed the popup
        if popup.should_stop:
            print("🛑 Tagging cancelled by user")
            # Clear the message box to prevent accidental sends
            try:
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.05)
                pyautogui.press('delete')
                time.sleep(0.1)
            except:
                pass
            popup.close()
            return
            
        try:
            # Get current message content
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.03)  # Reduced from 0.05
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)  # Reduced from 0.1
            before_tag = pyperclip.paste()
            
            # Move cursor to end
            pyautogui.press('end')
            time.sleep(0.03)  # Reduced from 0.05
            
            # Type @ to open member list
            pyautogui.write('@', interval=0.02)  # Reduced from 0.05
            time.sleep(0.3)  # Reduced from 0.5
            
            # Press down arrow to select next member in list
            if i > 0:
                pyautogui.press('down')
                time.sleep(0.1)  # Reduced from 0.2
            
            # Press Tab to select the member
            pyautogui.press('tab')
            time.sleep(MEMBER_DELAY)
            
            # Get the new message content after tagging
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.03)  # Reduced from 0.05
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(0.05)  # Reduced from 0.1
            after_tag = pyperclip.paste()
            
            # Move cursor to end
            pyautogui.press('end')
            time.sleep(0.03)  # Reduced from 0.05
            
            # Extract the newly added tag
            if after_tag != before_tag and after_tag.startswith(before_tag):
                new_tag = after_tag[len(before_tag):].strip()
                
                # Check if we've seen this tag before (duplicate = list wrapped around)
                if new_tag in seen_tags:
                    consecutive_duplicates += 1
                    print(f"⚠️  Duplicate detected: {new_tag[:20]}... (#{consecutive_duplicates})")
                    
                    # If we see 2 consecutive duplicates, we've looped through all members
                    if consecutive_duplicates >= 2:
                        print(f"✓ All unique members tagged! (Total: {tagged_count})")
                        print("ℹ️  Note: Last 2 tags are duplicates - remove them manually")
                        break
                    
                    # Still add space after first duplicate to continue checking
                    pyautogui.press('space')
                    time.sleep(0.05)
                else:
                    # New unique tag
                    seen_tags.add(new_tag)
                    consecutive_duplicates = 0
                    tagged_count += 1
                    
                    # Add a space after the tag
                    pyautogui.press('space')
                    time.sleep(0.05)  # Reduced from 0.1
                    
                    # Update popup
                    popup.update(tagged_count, MAX_MEMBERS, f"Tagging members... ({tagged_count} unique)")
                    
                    # Show progress in terminal every 5 members
                    if tagged_count % 5 == 0:
                        print(f"✓ Tagged {tagged_count} unique members so far...")
            else:
                # No tag was added (end of list or error)
                consecutive_duplicates += 1
                if consecutive_duplicates >= 2:
                    print(f"✓ No more members available")
                    pyautogui.press('backspace')  # Remove trailing @
                    break
            
        except Exception as e:
            print(f"⚠️  Stopped at {tagged_count} members: {e}")
            popup.update(tagged_count, MAX_MEMBERS, f"⚠️ Stopped at {tagged_count} members")
            break
    
    print(f"\n✅ Successfully tagged {tagged_count} unique members!")
    
    # Add the original message if any
    if clean_message:
        popup.update(tagged_count, MAX_MEMBERS, "Adding your message...")
        time.sleep(0.15)  # Reduced from 0.3
        pyautogui.write(clean_message, interval=TYPING_DELAY)
        print(f"✓ Added your message: {clean_message}")
    
    print("\n✅ Done! The message is ready.")
    print("⚠️  IMPORTANT: Remove the last 2 duplicate tags manually, then press Enter to send")
    print("             This prevents accidental re-tagging!\n")
    
    # Show completion
    popup.complete(f"✅ Tagged {tagged_count} members! Remove last 2 duplicates & press Enter")

def process_message():
    """
    Process the message when hotkey is pressed.
    """
    print("\n⏳ Processing...")
    
    # Focus WhatsApp first
    if not focus_whatsapp():
        print("❌ WhatsApp window not found!")
        return
    
    time.sleep(0.3)
    
    # Get text from message input
    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(0.2)
    
    message = pyperclip.paste()
    
    if '@all' in message.lower():
        print(f"🎯 Found @all in: '{message}'")
        tag_all_members(message)
    else:
        print("⚠️  No @all found in message")
        # Restore cursor position
        pyautogui.press('end')

class WhatsAppTaggerApp:
    """System tray application for WhatsApp Auto-Tagger."""
    
    def __init__(self):
        self.icon = None
        self.running = False
        
    def create_image(self):
        """Load app_icon.ico for system tray."""
        import os
        from PIL import Image
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.ico')
        try:
            image = Image.open(icon_path)
            return image
        except Exception as e:
            print(f"Warning: Could not load tray icon: {e}")
            # fallback: create a simple green icon
            width = 64
            height = 64
            image = Image.new('RGB', (width, height), '#25D366')
            return image
    
    def show_about(self, icon=None, item=None):
        """Show about dialog."""
        root = tk.Tk()
        root.withdraw()

        about_window = tk.Toplevel(root)
        about_window.title("About @TagAll")
        about_window.geometry("350x200")
        about_window.resizable(False, False)
        # Set window icon (robust path)
        import os
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app_icon.ico')
        try:
            about_window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Warning: Could not set icon: {e}")
        
        # Center window
        about_window.update_idletasks()
        x = (about_window.winfo_screenwidth() // 2) - (350 // 2)
        y = (about_window.winfo_screenheight() // 2) - (200 // 2)
        about_window.geometry(f"+{x}+{y}")
        
        frame = tk.Frame(about_window, bg='white', padx=30, pady=30)
        frame.pack(fill='both', expand=True)
        
        tk.Label(frame, text="@TagAll", 
                font=('Segoe UI', 16, 'bold'), bg='white').pack(pady=5)
        tk.Label(frame, text=f"Version {__version__}", 
                font=('Segoe UI', 10), bg='white', fg='#666').pack(pady=2)
        tk.Label(frame, text=f"Author: {__author__}", 
                font=('Segoe UI', 11), bg='white').pack(pady=15)
        tk.Label(frame, text="Hotkey: Ctrl+Shift+A", 
                font=('Segoe UI', 10, 'bold'), bg='white', fg='#25D366').pack(pady=5)
        tk.Label(frame, text="Type @all in WhatsApp, then press the hotkey", 
                font=('Segoe UI', 9), bg='white', fg='#666').pack(pady=5)
        
        tk.Button(frame, text="Close", command=about_window.destroy,
                 bg='#25D366', fg='white', font=('Segoe UI', 10),
                 relief='flat', padx=20, pady=5).pack(pady=10)
        
        about_window.mainloop()
    
    def quit_app(self, icon, item):
        """Quit the application."""
        print("\n👋 Shutting down @TagAll...")
        self.running = False
        keyboard.unhook_all()
        icon.stop()
        sys.exit(0)
    
    def setup_tray(self):
        """Setup system tray icon."""
        menu = Menu(
            MenuItem('@TagAll', self.show_about, default=True),
            MenuItem('About', self.show_about),
            MenuItem('Quit', self.quit_app)
        )
        
        self.icon = Icon(
            "@TagAll",
            self.create_image(),
            "@TagAll - Running\nCtrl+Shift+A to tag @all",
            menu
        )
    
    def run(self):
        """Run the application."""
        self.running = True
        
        print("=" * 60)
        print(f"@TagAll v{__version__}")
        print(f"Author: {__author__}")
        print("=" * 60)
        print("\n✅ Application started!")
        print("📍 System tray icon active")
        print("\n⌨️  Hotkey: Ctrl+Shift+A")
        print("📝 Usage:")
        print("   1. Type your message with @all in WhatsApp")
        print("   2. Press Ctrl+Shift+A")
        print("   3. Wait for tagging to complete")
        print("   4. Press Enter to send")
        print("\n💡 Right-click tray icon for options")
        print("=" * 60)
        
        # Setup hotkey
        keyboard.add_hotkey('ctrl+shift+a', process_message)
        
        # Setup and run tray icon
        self.setup_tray()
        self.icon.run()

def main():
    """Main entry point."""
    app = WhatsAppTaggerApp()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")