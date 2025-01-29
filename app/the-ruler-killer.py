#!/usr/bin/env python3
"""
The Ruler Killer - Process Management Utility
-------------------------------------------
A utility script to safely stop The Ruler application and clean up its processes.
Requires the correct password to execute.

Author: Samuel Miranda (samuelmirandasamt@gmail.com)
License: MIT
"""

import psutil
import sys
import os
import setproctitle
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='the_ruler_killer.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def kill_timelock_processes(password):
    """
    Find and terminate all running instances of The Ruler.
    
    Args:
        password (str): The password required to authorize the kill operation
        
    Returns:
        bool: True if the operation was successful, False otherwise
    """
    correct_password = "youaskedforit"  # Consider using environment variables
    
    if password != correct_password:
        print("Incorrect password!")
        logging.warning("Kill attempt with incorrect password")
        return False
    
    killed_count = 0
    try:
        # Scan for relevant processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Look for pythonw processes running our script
                if proc.info['name'] == 'pythonw.exe':
                    cmdline = proc.info['cmdline']
                    if cmdline and 'the-ruler.py' in ' '.join(cmdline):
                        proc.kill()
                        killed_count += 1
                        logging.info(f"Killed process {proc.pid}")
                
                # Look for our specific process name
                elif proc.name() == 'ruler-background':
                    proc.kill()
                    killed_count += 1
                    logging.info(f"Killed process {proc.pid}")
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    
        # Clean up persistent state
        appdata = os.getenv('APPDATA')
        state_file = os.path.join(appdata, 'timelock_state.json')
        if os.path.exists(state_file):
            os.remove(state_file)
            logging.info("Removed state file")
            
        print(f"Successfully killed {killed_count} TimeLock processes")
        logging.info(f"Killed {killed_count} processes total")
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Error killing processes: {e}")
        return False

def main():
    """Parse command line arguments and execute the kill operation."""
    if len(sys.argv) != 2:
        print("Usage: python the_ruler_killer.py <password>")
        return
    
    password = sys.argv[1]
    kill_timelock_processes(password)

if __name__ == "__main__":
    main()
