import subprocess

with open('requirements.txt', 'r') as f:
    for line in f:
        package = line.strip()
        if package:
            try:
                subprocess.check_call(['pip', 'install', package])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"Failed to install {package}")
print("\n\n\nDone installing packages!\n\nBeware, some packages probably failed to install for a variety of reasons.\n\nKeep an eye out for suprises!")