from src import bot
from dotenv import load_dotenv
import sys

def check_verion() -> None:
    import pkg_resources
    load_dotenv()

    # Read the requirements.txt file and add each line to a list
    with open('requirements.txt') as f:
        required = f.read().splitlines()

    # For each library listed in requirements.txt, check if the corresponding version is installed
    for package in required:
        # Use the pkg_resources library to get information about the installed version of the library
        package_name, package_verion = package.split('==')
        installed = pkg_resources.get_distribution(package_name)
        # Extract the library name and version number
        name, version = installed.project_name, installed.version
        # Compare the version number to see if it matches the one in requirements.txt
        if package != f'{name}=={version}':
            sys.exit()
# test123
if __name__ == '__main__': 
    check_verion()
    bot.run_discord_bot()