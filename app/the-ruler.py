#!/usr/bin/env python3
"""
The Ruler - Automated Computer Lock System
----------------------------------------
A lightweight application that automatically locks your computer at specified times.
Perfect for managing computer access schedules and establishing routine boundaries.

Author: Samuel Miranda (samuelmirandasamt@gmail.com)
License: MIT
"""

import tkinter as tk
from tkinter import messagebox
import time
from datetime import datetime
import os
import sys
import threading
import json
import setproctitle
import logging
import psutil  # For process management

# Configure logging with timestamp and level
logging.basicConfig(
    filename='the_ruler_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def is_already_running():
    """
    Check if another instance of the script is already running.
    Returns True if another instance is found, False otherwise.
    """
    current_pid = os.getpid()
    script_name = os.path.basename(__file__)
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if the process is another instance of this script
            if (proc.info['pid'] != current_pid and  # Exclude the current process
                script_name in ' '.join(proc.info['cmdline'] or [])):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

class TimeLock:
    """
    Main class handling the computer locking functionality.
    
    This class manages the lock screen, timing, and state persistence.
    It automatically locks the computer at specified times on weekdays.
    """

    def __init__(self):
        """Initialize the TimeLock system with default settings."""
        try:
            # Set a recognizable process name for management
            setproctitle.setproctitle('ruler-background')
            logging.info("Process name set successfully")
        except Exception as e:
            logging.error(f"Failed to set process name: {e}")
        
        # Core configuration
        self.password = "youaskedforit"  # Consider using environment variables
        self.lock_hour = 19              # 24-hour format
        self.lock_minute = 55
        self.is_locked = False
        self.lock_triggered = False  # Track if the lock has been triggered
        
        # State management
        self.state_file = os.path.join(os.getenv('APPDATA'), 'timelock_state.json')
        logging.info(f"Initialized TimeLock. Target time: {self.lock_hour}:{self.lock_minute}")
        self.load_state()

    def save_state(self):
        """Persist the current lock state to disk."""
        try:
            state = {
                'is_locked': self.is_locked,
                'lock_triggered': self.lock_triggered,  # Save lock_triggered flag
                'last_updated': datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
            logging.info("State saved successfully")
        except Exception as e:
            logging.error(f"Error saving state: {e}")

    def load_state(self):
        """Load the previous lock state from disk."""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    state = json.load(f)
                self.is_locked = state.get('is_locked', False)
                self.lock_triggered = state.get('lock_triggered', False)  # Load lock_triggered flag
                logging.info(f"State loaded successfully. Locked: {self.is_locked}, Triggered: {self.lock_triggered}")
            else:
                logging.info("No state file found, using defaults")
        except Exception as e:
            logging.error(f"Error loading state: {e}")
            self.is_locked = False
            self.lock_triggered = False

    def check_password(self, event=None):
        """Verify the entered password and unlock if correct."""
        try:
            entered_password = self.password_entry.get()
            if entered_password == self.password:
                self.is_locked = False
                self.lock_triggered = False  # Reset lock trigger
                self.save_state()
                self.root.destroy()
                logging.info("Correct password entered - unlocking")
            else:
                self.password_entry.delete(0, tk.END)
                logging.info("Incorrect password attempt")
        except Exception as e:
            logging.error(f"Error in check_password: {e}")
    
    def is_weekday(self):
        """Check if today is a weekday (Monday-Friday)."""
        is_weekday = datetime.now().weekday() <= 4
        logging.debug(f"Current day is weekday: {is_weekday}")
        return is_weekday
    
    def create_lock_screen(self):
        """Create and display the lock screen interface."""
        logging.info("Creating lock screen")
        try:
            self.root = tk.Tk()
            self.root.attributes('-fullscreen', True)
            self.root.attributes('-topmost', True)
            self.root.configure(bg='black')

            # Create centered frame for lock screen elements
            frame = tk.Frame(self.root, bg='black')
            frame.place(relx=0.5, rely=0.5, anchor='center')
            
            # Add lock screen message
            tk.Label(
                frame, 
                text="Computer Locked\nEnter password to unlock:",
                fg='white', 
                bg='black',
                font=('Arial', 14)
            ).pack(pady=10)
            
            # Add password entry field
            self.password_entry = tk.Entry(frame, show="*", font=('Arial', 12))
            self.password_entry.pack(pady=10)
            
            # Add unlock button
            tk.Button(
                frame,
                text="Unlock",
                command=self.check_password,
                font=('Arial', 12)
            ).pack(pady=5)
            
            # Enable Enter key for submission
            self.password_entry.bind('<Return>', self.check_password)
            self.password_entry.focus_force()
            
            # Keep window on top
            def stay_on_top():
                while hasattr(self, 'root'):
                    try:
                        self.root.attributes('-topmost', True)
                        time.sleep(0.5)
                    except:
                        break
            
            threading.Thread(target=stay_on_top, daemon=True).start()
            self.root.mainloop()
            
        except Exception as e:
            logging.error(f"Error creating lock screen: {e}")
    
    def check_time(self):
        """
        Main timing loop that checks if it's time to lock the computer.
        Runs continuously in the background.
        """
        while True:
            try:
                current_time = datetime.now()
                logging.debug(f"Checking time: {current_time.strftime('%H:%M:%S')}")
                
                if self.is_weekday():
                    # Check if it's time to lock
                    if (current_time.hour == self.lock_hour and 
                        current_time.minute == self.lock_minute and 
                        not self.is_locked and 
                        not self.lock_triggered):  # Only trigger once
                        
                        logging.info("Lock time reached! Activating lock...")
                        self.is_locked = True
                        self.lock_triggered = True  # Mark lock as triggered
                        self.save_state()
                        self.create_lock_screen()
                    
                    # Reset lock trigger if we've moved past the lock time
                    elif (current_time.hour > self.lock_hour or 
                          (current_time.hour == self.lock_hour and current_time.minute > self.lock_minute)):
                        self.lock_triggered = False
                        self.save_state()
                        logging.info("Lock time has passed - resetting lock trigger")
                
                else:
                    # Unlock on weekends
                    if self.is_locked:
                        self.is_locked = False
                        self.lock_triggered = False
                        self.save_state()
                        logging.info("Weekend detected - unlocking")
                
            except Exception as e:
                logging.error(f"Error in check_time: {e}")
            
            time.sleep(5)  # Check every 5 seconds

def main():
    """Initialize and run the TimeLock application."""
    try:
        # Check if another instance is already running
        if is_already_running():
            logging.error("Another instance of the script is already running. Exiting.")
            print("Another instance of the script is already running. Exiting.")
            sys.exit(1)
        
        logging.info("Starting TimeLock application")
        time_lock = TimeLock()
        
        logging.info("Starting time checking thread")
        time_thread = threading.Thread(target=time_lock.check_time, daemon=True)
        time_thread.start()
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()