import json
import os
from pathlib import Path

def print_vscode_settings():
    # Determine the path to settings.json based on OS
    if os.name == 'nt':  # Windows
        settings_path = Path(os.environ['APPDATA']) / 'Code' / 'User' / 'settings.json'
    else:  # macOS and Linux
        settings_path = Path.home() / '.config' / 'Code' / 'User' / 'settings.json'
    print(settings_path)
    try:
        # First, let's print the raw contents
        print("Raw file contents:")
        with open(settings_path, 'r', encoding='utf-8') as f:
            raw_content = f.read()
            print(raw_content)
            
        print("\nAttempting to parse as JSON:")
        # Now try to parse it
        settings = json.loads(raw_content)
        print(json.dumps(settings, indent=2))
        
    except FileNotFoundError:
        print(f"Could not find settings.json at: {settings_path}")
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")
        print("Error position: Line {}, Column {}".format(e.lineno, e.colno))
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    print_vscode_settings()