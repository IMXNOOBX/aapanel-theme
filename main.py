import sys
import shutil
import os
from datetime import datetime



def is_sudo():
    return os.geteuid() == 0

def is_linux():
    return sys.platform.startswith('linux')

def load_theme(path, theme):
    replacements = {
        'white': theme['background_color'],
        '#fff': theme['background_color'],
        '#fffff': theme['background_color'],

        '#20a53a': theme['theme_color'],

        '#f2f2f2': theme['secondary_color'],
        '#fbfbfb': theme['secondary_color'],
        
        '#e6e6e6': theme['tertiary_color'],
        '#f0f0f0': theme['tertiary_color'],
        '#f1f1f1': theme['tertiary_color'],
        '#f9f9f9': theme['tertiary_color'],
        '#f6f6f6': theme['tertiary_color'],

        '#353d44': theme['tab_highlight'],
        '#3c444d': theme['left_tab'],

        '#333': theme['general_text'],
        '#666': theme['general_text'],

        # known issues
        # .file_bodys doesn't change background-color
        # #20a53a is not allways changed to theme_color
        # .cw class is overwritten by background_color in the theme and it shouldnt
        # .btn-default classes are not taken into account by this script for some reason
        # many :hover classes are not taken into account by this script for some reason
        # input, textarea, select: should have a darker background like tab_highlight color
    }

    with open(path, 'r') as file:
        original_css = file.read()

    modified_css = original_css
    for old_value, new_value in replacements.items():
        modified_css = modified_css.replace(old_value, new_value)

    with open(path, 'w') as file:
        file.write(modified_css)
    print("Theme loaded successfully.")

def create_backup(path):
    backup_path = path + f".{datetime.now().strftime('%m-%d_%M:%S')}.bk"

    shutil.copy2(path, backup_path)
    print(f"Backup saved to {backup_path}")

def restore_backup(path):
    backups = [f for f in os.listdir(os.path.dirname(path)) if f.endswith('.bk')]
    if not backups:
        print("No backup files found.")
        return

    latest_backup = max(backups)
    backup_path = os.path.join(os.path.dirname(path), latest_backup)

    shutil.copy2(backup_path, path)
    os.remove(backup_path)
    print(f"Restored from backup: {latest_backup}")

def main():
    print("Starting AAPanel Theme Changer")

    if not is_linux():
        print("This script is designed for Linux operating systems.")
        sys.exit(1)

    if not is_sudo():
        print("This script should be run as sudo.")

    css_path = "/www/server/panel/BTPanel/static/css/site.css"

    theme = { # Discord Dark Theme
        "background_color": "#36393e", # (54,57,62)
        "theme_color": "#7289da", # (114,137,218)
        "secondary_color": "#282b30", # (40,43,48)
        "tertiary_color": "#424549", # (66,69,73)
        "tab_highlight": "#1e2124", # (30,33,36)
        "left_tab": "#1e2124", # (30,33,36)
        "general_text": "#fff", # (255,255,255)
    }

    if "--reset" in sys.argv:
        restore_backup(css_path)
        sys.exit(0)

    if not os.path.exists(css_path):
        print(f"Error: CSS file not found at {css_path}")
        print(f"Please provide the path of the AAPanel site.css file")
        css_path = input("CSS file path: ")

        if not os.path.exists(css_path):
            print(f"Invalid css path, please try again.")
            sys.exit(1)

    create_backup(css_path)

    load_theme(css_path, theme)

    print("Script finished.")

if __name__ == "__main__":
    main()
