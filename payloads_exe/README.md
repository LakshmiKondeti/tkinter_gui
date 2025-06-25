# Nexus Package Manager Demo

A professional Python package management application with a modern GUI interface that allows users to install, uninstall, and manage Python packages with administrator privileges.

## 🚀 Features

### Core Functionality
- **Real Package Management**: Actually installs and uninstalls Python packages using pip
- **Administrator Privileges**: Requires and runs with admin rights for system-level package operations
- **Multi-Environment Support**: Separate tabs for Development, Testing, and Production environments
- **Search Functionality**: Real-time search through available packages
- **Version Management**: Install specific package versions
- **Progress Tracking**: Visual progress indicators during installation/uninstallation

### User Interface
- **Modern GUI**: Built with tkinter and ttk for a professional look
- **Responsive Design**: Non-blocking operations with background threading
- **Logo Support**: Custom logo display at the top of the application
- **Tabbed Interface**: Organized package management across different environments
- **Scrollable Package List**: Handle large numbers of packages efficiently

### Technical Features
- **API Integration**: Fetches package data from RESTful API
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Threading**: Background operations to keep UI responsive
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Executable Support**: Can be compiled to standalone .exe file

## 📋 Requirements

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: Python 3.7 or higher
- **Administrator Rights**: Required for package installation/uninstallation

### Python Dependencies
```
tkinter (usually included with Python)
requests>=2.25.0
Pillow>=8.0.0
```

## 🛠️ Installation

### Option 1: Run from Source

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd nexus-package-manager
   ```

2. **Install dependencies**
   ```bash
   pip install requests pillow
   ```

3. **Add logo file**
   - Place your `logo.png` file in the same directory as the script
   - The logo should be in PNG format

4. **Run the application**
   ```bash
   python nexus_package_manager_demo.py
   ```

### Option 2: Use Pre-built Executable

1. **Download the executable** from releases
2. **Right-click** the .exe file
3. **Select "Run as administrator"**
4. **Grant admin privileges** when prompted

## 🏗️ Building the Executable

### Prerequisites
```bash
pip install pyinstaller
```

### Method 1: Using the Spec File (Recommended)
```bash
pyinstaller nexus_package_manager_demo.spec
```

### Method 2: Using Command Line
```bash
pyinstaller --onefile --windowed --add-data "logo.png;." --uac-admin nexus_package_manager_demo.py
```

### Build Options Explained
- `--onefile`: Creates a single executable file
- `--windowed`: Runs without console window
- `--add-data "logo.png;."`: Includes logo file in the exe
- `--uac-admin`: Requests admin privileges automatically

## 📖 Usage Guide

### Starting the Application

1. **Launch the application** (as administrator)
2. **Wait for package data** to load from the API
3. **Browse packages** in the Dev, Test, or Prod tabs

### Installing Packages

1. **Select a package** from the list
2. **Choose version** from the dropdown (if available)
3. **Click "Install"** button
4. **Wait for progress** dialog to complete
5. **Confirm success** message

### Uninstalling Packages

1. **Find installed package** (marked with green "Installed" label)
2. **Click "Uninstall"** button
3. **Wait for progress** dialog to complete
4. **Confirm success** message

### Searching Packages

1. **Use the search box** at the top of each tab
2. **Type package name** to filter results
3. **Real-time filtering** updates as you type

## 🔧 Configuration

### API Configuration
The application fetches package data from:
```python
API_URL = 'https://api.restful-api.dev/objects'
```

### Logo Configuration
- **File name**: `logo.png`
- **Location**: Same directory as the script/exe
- **Format**: PNG recommended
- **Size**: Will be resized to 120x120 pixels

### Window Configuration
```python
self.title('Nexus Package Manager Demo')
self.geometry('700x600')
```

## 🏗️ Project Structure

```
nexus-package-manager/
├── nexus_package_manager_demo.py    # Main application script
├── nexus_package_manager_demo.spec  # PyInstaller specification
├── logo.png                         # Application logo
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
└── dist/                           # Built executable (after build)
    └── nexus_package_manager_demo.exe
```

## 🔍 Troubleshooting

### Common Issues

#### Logo Not Loading
- **Problem**: Logo doesn't appear in the application
- **Solution**: Ensure `logo.png` is in the same directory as the script/exe
- **Alternative**: Check console output for detailed error messages

#### Admin Privileges Required
- **Problem**: Application won't start
- **Solution**: Right-click and "Run as administrator"
- **Note**: This is required for package installation

#### Package Installation Fails
- **Problem**: Installation shows error message
- **Solution**: Check internet connection and package name validity
- **Debug**: Check console output for detailed error information

#### API Connection Issues
- **Problem**: No packages appear in the list
- **Solution**: Check internet connection and API availability
- **Alternative**: The application will show an error dialog

### Debug Mode
To see detailed error messages, run with console:
```bash
pyinstaller --onefile --console --add-data "logo.png;." --uac-admin nexus_package_manager_demo.py
```

## 🚀 Development

### Adding New Features

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Code Structure

- **`NexusPackageManagerDemo`**: Main application class
- **`PackageFrame`**: Individual package display and controls
- **`TabWithSearch`**: Tab container with search functionality
- **`fetch_packages()`**: API data retrieval function

### Key Functions

- **`is_admin()`**: Check for administrator privileges
- **`run_as_admin()`**: Elevate privileges if needed
- **`pack_logo()`**: Load and display application logo
- **`install()`**: Install packages with progress tracking
- **`uninstall()`**: Remove packages with progress tracking

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the console output for error details

## 🔄 Version History

- **v1.0.0**: Initial release with basic package management
- **v1.1.0**: Added admin privileges and real installation
- **v1.2.0**: Added progress tracking and better error handling
- **v1.3.0**: Added logo support and executable building

## 🙏 Acknowledgments

- Built with Python and tkinter
- Uses Pillow for image processing
- PyInstaller for executable creation
- RESTful API for package data

---

**Note**: This application requires administrator privileges to install and uninstall system packages. Always review packages before installation. 