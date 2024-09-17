import os
import sys
import subprocess
import socket
from tqdm import tqdm
import time
from colorama import Fore, Style, init
import shutil

# Initialize colorama
init(autoreset=True)

def is_command_installed(command):
    try:
        subprocess.run(['which', command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def install_package(package_name):
    print(f"{Fore.YELLOW}Attempting to install {package_name}...")
    try:
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        subprocess.run(['sudo', 'apt-get', 'install', '-y', package_name], check=True)
        print(f"{Fore.GREEN}{package_name} has been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}An error occurred while installing {package_name}: {e}")

def run_bash_command():
    bash_command = """
    clear
    figlet "SHOUNTO" -c | lolcat && figlet -f digital -c "                    Web Pentester" | lolcat
    """
    try:
        subprocess.run(bash_command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}An error occurred: {e}")

def simulate_long_process():
    progress_color = Fore.GREEN
    complete_color = Fore.CYAN + Style.BRIGHT
    for i in tqdm(range(100), desc=progress_color + "Processing", ncols=100, ascii=True):
        time.sleep(0.05)
    print(complete_color + "Process completed 100%!")

def check_internet_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except (socket.timeout, socket.gaierror, ConnectionRefusedError):
        return False

def is_kali_linux():
    try:
        result = subprocess.run(['lsb_release', '-i'], capture_output=True, text=True, check=True)
        if 'Kali' in result.stdout:
            print(f"{Fore.GREEN}This is Kali Linux")
            return True
        else:
            print(f"{Fore.RED}This is not Kali Linux")
            return False
    except subprocess.CalledProcessError:
        print(f"{Fore.RED}Failed to check OS information")
        return False

def install_and_setup_tool(tool_name, install_command, tool_path):
    source_file = f'/home/{os.getenv("USER")}/go/bin/{tool_name}'
    destination_path = '/bin'
    cp_command = f'sudo cp {source_file} {destination_path}'

    print(f"{Fore.GREEN} Installing {tool_name}....")
    print()
    try:
        subprocess.run(install_command, check=True, shell=True)
        subprocess.run(cp_command, shell=True, check=True)
        print(f"{Fore.GREEN} Successfully installed {tool_name}.....")
        print()
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}An error occurred: {e}")
        print()

def install_nuclei():
    print(f"{Fore.YELLOW}Installing Nuclei...")
    try:
        # Install Nuclei using go install
        subprocess.run('go install github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest', shell=True, check=True)
        
        # Copy the installed Nuclei binary to /bin
        source_file = f'/home/{os.getenv("USER")}/go/bin/nuclei'
        destination_path = '/bin/nuclei'
        
        if os.path.exists(source_file):
            subprocess.run(['sudo', 'cp', source_file, destination_path], check=True)
            print(f"{Fore.GREEN}Nuclei binary copied to {destination_path}.")
        else:
            print(f"{Fore.RED}Nuclei binary not found at {source_file}.")
            
        print(f"{Fore.GREEN}Nuclei installed and setup successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}An error occurred while installing or setting up Nuclei: {e}")

def clone_and_setup_repository():
    username = os.popen('whoami').read().strip()
    clone_path = f'/home/{username}/Gf-Patterns'
    gf_directory = os.path.expanduser('~/.gf')

    if os.path.exists(clone_path):
        print(f"{Fore.YELLOW}The directory {clone_path} already exists. Removing it...")
        try:
            shutil.rmtree(clone_path)
            print(f"{Fore.GREEN}Removed the existing directory {clone_path}.")
        except Exception as e:
            print(f"{Fore.RED}An error occurred while removing the directory: {e}")
            return

    print('Cloning the repository...')
    try:
        subprocess.run(['git', 'clone', 'https://github.com/1ndianl33t/Gf-Patterns', clone_path], check=True)
        print(f"{Fore.GREEN}Repository cloned successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}An error occurred during cloning: {e}")
        return

    if not os.path.exists(gf_directory):
        os.makedirs(gf_directory)

    print('Creating .gf file...')
    try:
        gf_file_path = os.path.join(clone_path, '.gf')
        with open(gf_file_path, 'w') as f:
            f.write('')
        print(f"{Fore.GREEN}.gf file created successfully.")
    except IOError as e:
        print(f"{Fore.RED}An error occurred while creating .gf file: {e}")
        return

    print('Moving .json files...')
    try:
        json_files = [f for f in os.listdir(clone_path) if f.endswith('.json')]
        if not json_files:
            print(f"{Fore.YELLOW}No .json files found to move.")
            return

        for json_file in json_files:
            src = os.path.join(clone_path, json_file)
            dst = os.path.join(gf_directory, json_file)
            shutil.move(src, dst)

        print(f"{Fore.GREEN}Files moved successfully.")
    except Exception as e:
        print(f"{Fore.RED}An error occurred during moving files: {e}")

def update_nuclei_templates():
    print(f"{Fore.YELLOW}Updating Nuclei templates...")
    try:
        subprocess.run(['nuclei', '-update-templates'], check=True)
        print(f"{Fore.GREEN}Nuclei templates updated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}An error occurred while updating Nuclei templates: {e}")

def install_additional_tools():
    additional_tools = ['assetfinder', 'subfinder', 'sublist3r','amass','dirsearch']

    for tool in additional_tools:
        if not is_command_installed(tool):
            print(f"{Fore.YELLOW}Installing {tool}...")
            install_package(tool)

if __name__ == "__main__":
    # Check if figlet and lolcat are installed
    packages = ['figlet', 'lolcat']
    for package in packages:
        if not is_command_installed(package):
            install_package(package)
    
    run_bash_command()

    if not check_internet_connection():
        print(f"{Fore.RED}No internet connection. Exiting program.")
        sys.exit()

    simulate_long_process()

    if is_kali_linux():
        tools = {
            'gau': ('go install github.com/lc/gau@latest', '/home/{os.getenv("USER")}/go/bin/gau'),
            'httpx': ('go install github.com/projectdiscovery/httpx/cmd/httpx@latest', '/home/{os.getenv("USER")}/go/bin/httpx'),
            'dalfox': ('go install github.com/hahwul/dalfox/v2@latest', '/home/{os.getenv("USER")}/go/bin/dalfox'),
            'waybackurls': ('go install github.com/tomnomnom/waybackurls@latest', '/home/{os.getenv("USER")}/go/bin/waybackurls'),
            'gf': ('go install github.com/tomnomnom/gf@latest', '/home/{os.getenv("USER")}/go/bin/gf')
        }
        for tool, (install_command, tool_path) in tools.items():
            install_and_setup_tool(tool, install_command, tool_path)
        
        install_nuclei()  # Install Nuclei and copy the binary to /bin

        # Install additional tools via apt
        install_additional_tools()

    else:
        print(f"{Fore.RED}This script is intended to run on Kali Linux only. Exiting.")
        sys.exit()

    clone_and_setup_repository()
    update_nuclei_templates()  # Update Nuclei templates after installation
    simulate_long_process()
