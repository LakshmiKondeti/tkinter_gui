# Nexus Package Manager Demo - Python Script Documentation

## 📄 Script Overview

**File**: `nexus_package_manager_demo.py`  
**Purpose**: A GUI-based Python package manager that installs/uninstalls packages with admin privileges  
**Language**: Python 3.7+  
**GUI Framework**: tkinter/ttk  

## 🏗️ Script Structure

### Imports and Dependencies
```python
import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import os
import sys
import ctypes
```

### Key Components

#### 1. Admin Privilege Functions
```python
def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with administrator privileges"""
    # Automatically elevates privileges if not running as admin
```

#### 2. API Data Fetching
```python
def fetch_packages():
    """Fetch and group packages by name, versions as ids"""
    # Fetches from: https://api.restful-api.dev/objects
    # Groups packages by name with their available versions
```

#### 3. Main Classes

##### PackageFrame Class
**Purpose**: Individual package display and control widget

**Key Methods**:
- `create_widgets()`: Creates package name, version dropdown, install/uninstall buttons
- `install()`: Performs real pip installation with progress dialog
- `uninstall()`: Performs real pip uninstallation with progress dialog
- `update_buttons()`: Updates button states based on installation status

**Features**:
- Version selection dropdown
- Install/Uninstall buttons
- Installation status indicator
- Background threading for non-blocking operations

##### TabWithSearch Class
**Purpose**: Tab container with search functionality

**Key Methods**:
- `create_widgets()`: Creates search box and scrollable package list
- `populate_packages()`: Fills the tab with package frames
- `update_filter()`: Real-time search filtering

**Features**:
- Search box for filtering packages
- Scrollable package list
- Real-time search updates

##### NexusPackageManagerDemo Class
**Purpose**: Main application window

**Key Methods**:
- `__init__()`: Initializes the main window and tabs
- `pack_logo()`: Loads and displays the application logo

**Features**:
- 700x600 pixel window
- Logo display at top
- Three tabs: Dev, Test, Prod
- Each tab contains the same package list

## 🔧 How the Script Works

### 1. Startup Process
```python
if __name__ == '__main__':
    # Check for admin privileges before starting
    run_as_admin()
    
    # Check for PIL dependency
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror('Missing Dependency', 'Please install Pillow: pip install pillow')
        exit(1)
    
    # Start the application
    app = NexusPackageManagerDemo()
    app.mainloop()
```

### 2. Admin Privilege Check
- Script checks if running with admin rights
- If not, automatically requests elevation via UAC
- Exits if elevation fails

### 3. Package Data Loading
- Fetches package data from REST API
- Groups packages by name with available versions
- Populates all three tabs with the same data

### 4. Logo Loading
```python
def pack_logo(self):
    # Handles logo path for both script and exe execution
    # Supports PyInstaller bundled files
    # Falls back to multiple alternative paths
```

### 5. Package Installation Process
```python
def install(self):
    # Shows progress dialog
    # Runs pip install in background thread
    # Updates UI when complete
    # Shows success/error message
```

## 📊 Data Flow

```
API Request → Package Data → Group by Name → Create PackageFrames → Display in Tabs
     ↓
User clicks Install → Background Thread → pip install → Update UI → Show Result
```

## 🎨 GUI Layout

```
┌─────────────────────────────────────────────────────────┐
│                    [LOGO]                               │
├─────────────────────────────────────────────────────────┤
│ [Dev] [Test] [Prod]                                     │
├─────────────────────────────────────────────────────────┤
│ Search: [________________]                              │
├─────────────────────────────────────────────────────────┤
│ Package Name    │ Version │ Install │ Uninstall │ Status│
│ Package1        │ v1.0    │ [Install]│ [Uninstall]│ [✓]  │
│ Package2        │ v2.1    │ [Install]│ [Uninstall]│      │
│ ...             │ ...     │ ...     │ ...        │ ...  │
└─────────────────────────────────────────────────────────┘
```

## 🔍 Key Functions Explained

### Package Installation
```python
def install(self):
    # 1. Get selected version
    # 2. Show progress window
    # 3. Run pip install in background thread
    # 4. Update UI with result
    # 5. Show success/error message
```

### Package Uninstallation
```python
def uninstall(self):
    # 1. Show progress window
    # 2. Run pip uninstall in background thread
    # 3. Update UI with result
    # 4. Show success/error message
```

### Search Functionality
```python
def update_filter(self, *args):
    # 1. Get search text
    # 2. Filter packages by name
    # 3. Re-populate the list
    # 4. Update in real-time
```

## 🛠️ Configuration Points

### API Endpoint
```python
API_URL = 'https://api.restful-api.dev/objects'
```

### Window Settings
```python
self.title('Nexus Package Manager Demo')
self.geometry('700x600')
```

### Logo Settings
```python
img = img.resize((120, 120), Image.Resampling.LANCZOS)
```

### Package Installation
```python
# Install with specific version
f"{package_name}=={version}" if version != 'N/A' else package_name

# Uninstall package
f"{package_name}"
```

## 🐛 Error Handling

### Admin Privileges
- Checks for admin rights on startup
- Automatically requests elevation
- Shows error if elevation fails

### Package Installation
- Timeout handling (60 seconds)
- Error message display
- Background thread error catching

### Logo Loading
- Multiple fallback paths
- Format validation
- Graceful error display

### API Connection
- Network error handling
- JSON parsing errors
- User-friendly error messages

## 📝 Code Quality Features

### Threading
- Background operations for UI responsiveness
- Proper thread management
- UI updates in main thread

### Error Handling
- Comprehensive try-catch blocks
- User-friendly error messages
- Graceful degradation

### Code Organization
- Clear class structure
- Separated concerns
- Well-documented functions

## 🔧 Dependencies

### Required Packages
- `tkinter` - GUI framework (usually included with Python)
- `requests` - HTTP requests for API calls
- `Pillow` - Image processing for logo display

### Optional for Building
- `pyinstaller` - For creating executable files

## 📋 Usage Notes

### Running the Script
```bash
python nexus_package_manager_demo.py
```

### Requirements
- Python 3.7 or higher
- Administrator privileges
- Internet connection for API calls
- `logo.png` file in same directory

### Expected Behavior
- UAC prompt on startup (admin elevation)
- Package list loads from API
- Logo displays at top
- Three tabs with same package data
- Real package installation/uninstallation

---

**Note**: This script is designed to be a functional package manager, not just a demo. It actually installs and uninstalls Python packages using pip with administrator privileges. 