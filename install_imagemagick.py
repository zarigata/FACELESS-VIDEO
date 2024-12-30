import sys
import subprocess
import platform

def install_imagemagick():
    """
    Cross-platform ImageMagick installation script
    Supports Windows, macOS, and Linux
    """
    os_name = platform.system().lower()
    
    print(f"Detected OS: {os_name}")
    
    try:
        if os_name == 'windows':
            # Use Chocolatey for Windows
            subprocess.run(['powershell', '-Command', 
                'Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString("https://chocolatey.org/install.ps1"))'], 
                check=True)
            subprocess.run(['choco', 'install', 'imagemagick', '-y'], check=True)
        
        elif os_name == 'darwin':  # macOS
            subprocess.run(['brew', 'install', 'imagemagick'], check=True)
        
        elif os_name == 'linux':
            # Supports multiple Linux package managers
            package_managers = [
                ['apt-get', 'install', '-y', 'imagemagick'],  # Debian/Ubuntu
                ['yum', 'install', '-y', 'ImageMagick'],      # CentOS/RHEL
                ['dnf', 'install', '-y', 'ImageMagick'],      # Fedora
                ['pacman', '-S', '--noconfirm', 'imagemagick']  # Arch Linux
            ]
            
            for cmd in package_managers:
                try:
                    subprocess.run(cmd, check=True)
                    break
                except subprocess.CalledProcessError:
                    continue
            else:
                print("Could not install ImageMagick. Please install manually.")
                sys.exit(1)
        
        else:
            print(f"Unsupported OS: {os_name}")
            sys.exit(1)
        
        print("ImageMagick installed successfully!")
    
    except subprocess.CalledProcessError as e:
        print(f"Error installing ImageMagick: {e}")
        sys.exit(1)

if __name__ == '__main__':
    install_imagemagick()
