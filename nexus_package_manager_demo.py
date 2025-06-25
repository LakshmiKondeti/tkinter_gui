import tkinter as tk
from tkinter import ttk, messagebox
import requests
from PIL import Image, ImageTk
import os
import sys
import ctypes

def is_admin():
    """Check if the script is running with administrator privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-run the script with administrator privileges"""
    try:
        if not is_admin():
            # Re-run the program with admin rights
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    except Exception as e:
        messagebox.showerror('Admin Error', f'Failed to elevate privileges: {e}')
        sys.exit(1)

API_URL = 'https://api.restful-api.dev/objects'

# Fetch and group packages by name, versions as ids
def fetch_packages():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
        packages = {}
        for item in data:
            name = item.get('name', 'Unknown')
            version = item.get('id', 'N/A')
            if name not in packages:
                packages[name] = []
            packages[name].append(version)
        return [ {'name': name, 'versions': versions} for name, versions in packages.items() ]
    except Exception as e:
        messagebox.showerror('API Error', f'Failed to fetch packages: {e}')
        return []

class PackageFrame(ttk.Frame):
    def __init__(self, parent, package, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.package = package
        self.installed_version = None
        self.selected_version = tk.StringVar(value=package['versions'][0])
        self.create_widgets()
        self.update_buttons()

    def create_widgets(self):
        ttk.Label(self, text=self.package['name'], width=30).grid(row=0, column=0, padx=5, pady=2)
        self.version_menu = ttk.Combobox(self, values=self.package['versions'], textvariable=self.selected_version, state='readonly', width=8)
        self.version_menu.grid(row=0, column=1, padx=5)
        self.install_btn = ttk.Button(self, text='Install', command=self.install)
        self.uninstall_btn = ttk.Button(self, text='Uninstall', command=self.uninstall)
        self.installed_lbl = ttk.Label(self, text='Installed', foreground='green')
        self.install_btn.grid(row=0, column=2, padx=5)
        self.uninstall_btn.grid(row=0, column=3, padx=5)
        self.installed_lbl.grid(row=0, column=4, padx=5)

    def update_buttons(self):
        if self.installed_version == self.selected_version.get():
            self.install_btn.state(['disabled'])
            self.uninstall_btn.state(['!disabled'])
            self.installed_lbl.grid()
        elif self.installed_version:
            self.install_btn.state(['!disabled'])
            self.uninstall_btn.state(['!disabled'])
            self.installed_lbl.grid()
        else:
            self.install_btn.state(['!disabled'])
            self.uninstall_btn.state(['disabled'])
            self.installed_lbl.grid_remove()

    def install(self):
        version = self.selected_version.get()
        package_name = self.package['name']
        
        try:
            # Show progress dialog
            progress_window = tk.Toplevel()
            progress_window.title("Installing Package")
            progress_window.geometry("300x150")
            progress_window.transient(self.winfo_toplevel())
            progress_window.grab_set()
            
            # Center the progress window
            progress_window.geometry("+%d+%d" % (
                self.winfo_toplevel().winfo_rootx() + 50,
                self.winfo_toplevel().winfo_rooty() + 50))
            
            ttk.Label(progress_window, text=f"Installing {package_name} v{version}...").pack(pady=20)
            progress = ttk.Progressbar(progress_window, mode='indeterminate')
            progress.pack(pady=10, padx=20, fill='x')
            progress.start()
            
            # Use subprocess to run PowerShell command
            import subprocess
            import threading
            
            def install_package():
                try:
                    # PowerShell command for installing packages
                    # You can use different PowerShell package managers here
                    
                    # Option 1: Using PowerShell Gallery (Install-Module)
                    if version != 'N/A':
                        ps_command = f'Install-Module -Name "{package_name}" -RequiredVersion "{version}" -Force -AllowClobber'
                    else:
                        ps_command = f'Install-Module -Name "{package_name}" -Force -AllowClobber'
                    
                    # Option 2: Using Chocolatey (if installed)
                    # ps_command = f'choco install {package_name}'
                    
                    # Option 3: Using Winget (Windows Package Manager)
                    # ps_command = f'winget install {package_name}'
                    
                    # Option 4: Using Scoop (if installed)
                    # ps_command = f'scoop install {package_name}'
                    
                    # Run PowerShell command
                    result = subprocess.run([
                        'powershell', '-Command', ps_command
                    ], capture_output=True, text=True, timeout=120)
                    
                    # Update UI in main thread
                    self.after(0, lambda: self._install_complete(result, progress_window))
                    
                except subprocess.TimeoutExpired:
                    self.after(0, lambda: self._install_error("Installation timed out", progress_window))
                except Exception as e:
                    self.after(0, lambda: self._install_error(f"Installation failed: {e}", progress_window))
            
            # Run installation in background thread
            install_thread = threading.Thread(target=install_package)
            install_thread.daemon = True
            install_thread.start()
            
        except Exception as e:
            messagebox.showerror('Install Error', f'Failed to start installation: {e}')

    def _install_complete(self, result, progress_window):
        """Handle installation completion"""
        progress_window.destroy()
        
        if result.returncode == 0:
            messagebox.showinfo('Install Success', f"Successfully installed {self.package['name']} v{self.selected_version.get()}")
            self.installed_version = self.selected_version.get()
            self.update_buttons()
        else:
            error_msg = result.stderr if result.stderr else "Unknown error occurred"
            messagebox.showerror('Install Error', f'Failed to install package:\n{error_msg}')

    def _install_error(self, error_msg, progress_window):
        """Handle installation error"""
        progress_window.destroy()
        messagebox.showerror('Install Error', error_msg)

    def uninstall(self):
        package_name = self.package['name']
        
        try:
            # Show progress dialog
            progress_window = tk.Toplevel()
            progress_window.title("Uninstalling Package")
            progress_window.geometry("300x150")
            progress_window.transient(self.winfo_toplevel())
            progress_window.grab_set()
            
            # Center the progress window
            progress_window.geometry("+%d+%d" % (
                self.winfo_toplevel().winfo_rootx() + 50,
                self.winfo_toplevel().winfo_rooty() + 50))
            
            ttk.Label(progress_window, text=f"Uninstalling {package_name}...").pack(pady=20)
            progress = ttk.Progressbar(progress_window, mode='indeterminate')
            progress.pack(pady=10, padx=20, fill='x')
            progress.start()
            
            # Use subprocess to run PowerShell command
            import subprocess
            import threading
            
            def uninstall_package():
                try:
                    # PowerShell command for uninstalling packages
                    # You can use different PowerShell package managers here
                    
                    # Option 1: Using PowerShell Gallery (Uninstall-Module)
                    ps_command = f'Uninstall-Module -Name "{package_name}" -Force -AllVersions'
                    
                    # Option 2: Using Chocolatey (if installed)
                    # ps_command = f'choco uninstall {package_name} -y'
                    
                    # Option 3: Using Winget (Windows Package Manager)
                    # ps_command = f'winget uninstall {package_name}'
                    
                    # Option 4: Using Scoop (if installed)
                    # ps_command = f'scoop uninstall {package_name}'
                    
                    # Run PowerShell command
                    result = subprocess.run([
                        'powershell', '-Command', ps_command
                    ], capture_output=True, text=True, timeout=120)
                    
                    # Update UI in main thread
                    self.after(0, lambda: self._uninstall_complete(result, progress_window))
                    
                except subprocess.TimeoutExpired:
                    self.after(0, lambda: self._uninstall_error("Uninstallation timed out", progress_window))
                except Exception as e:
                    self.after(0, lambda: self._uninstall_error(f"Uninstallation failed: {e}", progress_window))
            
            # Run uninstallation in background thread
            uninstall_thread = threading.Thread(target=uninstall_package)
            uninstall_thread.daemon = True
            uninstall_thread.start()
            
        except Exception as e:
            messagebox.showerror('Uninstall Error', f'Failed to start uninstallation: {e}')

    def _uninstall_complete(self, result, progress_window):
        """Handle uninstallation completion"""
        progress_window.destroy()
        
        if result.returncode == 0:
            messagebox.showinfo('Uninstall Success', f"Successfully uninstalled {self.package['name']}")
            self.installed_version = None
            self.update_buttons()
        else:
            error_msg = result.stderr if result.stderr else "Unknown error occurred"
            messagebox.showerror('Uninstall Error', f'Failed to uninstall package:\n{error_msg}')

    def _uninstall_error(self, error_msg, progress_window):
        """Handle uninstallation error"""
        progress_window.destroy()
        messagebox.showerror('Uninstall Error', error_msg)

class TabWithSearch(ttk.Frame):
    def __init__(self, parent, all_packages, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.all_packages = all_packages
        self.filtered_packages = all_packages.copy()
        self.search_var = tk.StringVar()
        self.search_var.trace_add('write', self.update_filter)
        self.create_widgets()
        self.populate_packages()

    def create_widgets(self):
        search_frame = ttk.Frame(self)
        search_frame.pack(fill='x', padx=8, pady=4)
        ttk.Label(search_frame, text='Search:').pack(side='left')
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=4)
        # Scrollable area
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')

    def populate_packages(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for i, pkg in enumerate(self.filtered_packages):
            pf = PackageFrame(self.scrollable_frame, pkg)
            pf.grid(row=i, column=0, sticky='w', pady=4, padx=4)

    def update_filter(self, *args):
        search_text = self.search_var.get().lower()
        self.filtered_packages = [pkg for pkg in self.all_packages if search_text in pkg['name'].lower()]
        self.populate_packages()

class NexusPackageManagerDemo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Nexus Package Manager Demo')
        self.geometry('700x600')
        self.pack_logo()
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand=True)
        packages = fetch_packages()
        for env in ['dev', 'test', 'prod']:
            tab = TabWithSearch(self.notebook, packages)
            self.notebook.add(tab, text=env.capitalize())

    def pack_logo(self):
        logo_frame = ttk.Frame(self)
        logo_frame.pack(fill='x', pady=8)
        
        # Handle logo path for both script and exe execution
        try:
            # For PyInstaller exe files
            if hasattr(sys, '_MEIPASS'):
                # Running as exe (PyInstaller)
                base_path = sys._MEIPASS
            else:
                # Running as script
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            logo_path = os.path.join(base_path, "logo.png")
            
            if os.path.exists(logo_path):
                try:
                    img = Image.open(logo_path)
                    # Stretch height while keeping width at 120px
                    img = img.resize((120, 120), Image.Resampling.LANCZOS)  # Increased height to 120px
                    self.logo_img = ImageTk.PhotoImage(img)
                    label = ttk.Label(logo_frame, image=self.logo_img)
                    label.pack()
                except Exception as e:
                    print(f"Error loading logo: {e}")
                    ttk.Label(logo_frame, text='[Logo could not be loaded]').pack()
            else:
                print(f"Logo not found at: {logo_path}")
                # Try alternative locations
                alternative_paths = [
                    os.path.join(os.getcwd(), "logo.png"),  # Current working directory
                    os.path.join(os.path.dirname(sys.executable), "logo.png"),  # Exe directory
                    "logo.png"  # Just the filename
                ]
                
                logo_loaded = False
                for alt_path in alternative_paths:
                    if os.path.exists(alt_path):
                        try:
                            img = Image.open(alt_path)
                            img = img.resize((120, 120), Image.Resampling.LANCZOS)
                            self.logo_img = ImageTk.PhotoImage(img)
                            label = ttk.Label(logo_frame, image=self.logo_img)
                            label.pack()
                            logo_loaded = True
                            print(f"Logo loaded from: {alt_path}")
                            break
                        except Exception as e:
                            print(f"Failed to load logo from {alt_path}: {e}")
                            continue
                
                if not logo_loaded:
                    ttk.Label(logo_frame, text='[Logo image not found: logo.png]').pack()
                    
        except Exception as e:
            print(f"Error in logo loading: {e}")
            ttk.Label(logo_frame, text='[Logo loading error]').pack()

if __name__ == '__main__':
    # Check for admin privileges before starting
    run_as_admin()
    
    try:
        from PIL import Image, ImageTk
    except ImportError:
        messagebox.showerror('Missing Dependency', 'Please install Pillow: pip install pillow')
        exit(1)
    app = NexusPackageManagerDemo()
    app.mainloop() 