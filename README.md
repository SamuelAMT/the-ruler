# The Ruler

Ever arrived home to find your PC occupied at inconvenient hours? Meet **The Ruler** - a lightweight Python application that automatically locks your computer at specified times, ensuring you maintain control over your PC usage schedule.

## 🚀 Features

- 🔒 **Automatic computer locking** at configurable times
- 📅 **Weekday-only operation** (automatically disables on weekends)
- 💪 **Persistence** across system restarts
- 🎯 **Minimal resource usage**
- ⚡ **Quick and easy setup**

---

## 💽 Installation

### 1⃣ Clone this repository

```bash
git clone https://github.com/SamuelAMT/the-ruler
cd the-ruler
```

### 2⃣ Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

### 3⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚦 Basic Usage

Start the application:

```bash
start_ruler.bat
```

- The application will run in the background and lock your computer at the specified time (default: **15:25**) on weekdays.
- To unlock, enter the password (default: **"youaskedforit"**).
- To stop the application:

```bash
python the-ruler-killer.py youaskedforit
```

---

## ⚙️ Advanced Configuration

### ⏰ Custom Lock Time
Modify `lock_hour` and `lock_minute` in `the-ruler.py`:

```python
lock_hour = 15
lock_minute = 25
```

### 🔐 Secure Password Storage
By default, the password is stored in plain text for ease of use. However, you can use an **environment variable** for better security:

```python
import os
from dotenv import load_dotenv

load_dotenv()

class TimeLock:
    def __init__(self):
        self.password = os.getenv('RULER_PASSWORD', 'default_password')
```

Create a `.env` file:

```env
RULER_PASSWORD=your_secure_password
```

✅ **Don't forget to add `.env` to your `.gitignore`!**

### 🛠️ Virtual Environment Path

If you're using a virtual environment, update `start_ruler.bat` to match your `venv` folder name. Most users create it as `venv`, but if yours is different, change this line:

```bat
call "..\venv\Scripts\activate.bat"
```

to

```bat
call "..\my_venv\Scripts\activate.bat"
```

---

## 🔧 Troubleshooting

### 🔍 The application runs in the background
- **Important Note**: The process is designed to run in the background, making it impossible to unlock the system without entering the correct password.
- **If you forget your password**: Restart your computer in **secure boot mode** and follow the instructions in `the-ruler-killer.py` to disable the process.

### 📛 The lock screen appears multiple times
- **Issue**: Multiple instances of the application are running.
- **Solution**: Run `python the-ruler-killer.py youaskedforit` to kill all instances, then restart the application.

### 🚫 The application doesn't start
- **Issue**: Common startup issues include:
  - Virtual environment not activated
  - Dependencies not installed
  - Missing administrator privileges
- **Solution**:
  - Ensure you've activated the virtual environment
  - Run `pip install -r requirements.txt`
  - Run `start_ruler.bat` as administrator

### 🔒 Can't type in the password field
- **Issue**: The lock screen might be in an unresponsive state.
- **Solution**:
  1. Press `Ctrl+Alt+Delete`
  2. Open **Task Manager**
  3. End the **ruler-background** process
  4. Run the killer script and restart the application

### ⏳ The application doesn't lock at the specified time
- **Issue**: Time synchronization or process issues.
- **Solution**:
  - Check that system time is correct
  - Verify the log file at `the_ruler_debug.log`
  - Ensure the application is running (check Task Manager)

---

## ❓ FAQ

### 🔍 Is this safe to use?
Yes, **The Ruler** is designed with safety in mind. You can always:
- Use **Task Manager** to close it
- Run the **killer script**
- Restart your computer

🤚 The application intentionally allows these "escape routes" for safety.

### 🔄 Will it work after system updates?
Yes, **The Ruler** persists after system updates and restarts. It will automatically resume its schedule when the computer starts.

### 🛡️ Can someone just end the process to bypass it?
Yes, this is intentional. **The Ruler** is designed for scheduling and routine management, not as a security tool. If you need strict access control, consider using Windows' built-in parental controls.

### 🗓️ Why doesn't it work on weekends?
This is a **feature!** The Ruler assumes you might want more flexible computer access on weekends. You can modify this in the code if you want different behavior.

### ⏳ Can I change the lock time dynamically?
Currently, the lock time is set in the code. Future versions may include a configuration file or UI for easier time management.

### 🤝 How can I contribute or report issues?
Feel free to:
- **Open issues** on GitHub
- **Submit pull requests**
- **Contact the maintainer**: [samuelmirandasamt@gmail.com](mailto:samuelmirandasamt@gmail.com)

---

## 🔒 Security Considerations

- The application **runs with administrator privileges** to ensure lock screen functionality.
- Password is **stored in plain text by default** – use the **environment variable approach** for better security.
- The lock **can be bypassed by killing the process** – this is intentional for safety reasons.
- If you forget your password, you can **secure boot into recovery mode** and follow the instructions in `the-ruler-killer.py` to stop the process.

---

## 🌱 Contributing

Pull requests are welcome! For major changes, please open an **issue** first to discuss what you would like to change.

---

## 🐝 License

**MIT**

---

## ⚠️ Disclaimer

This tool is intended for **personal use** to help manage computer access times. It is **not designed** to be a security tool and should **not** be relied upon for critical security purposes.

