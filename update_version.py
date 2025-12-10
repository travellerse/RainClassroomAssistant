#!/usr/bin/env python3
import subprocess
import sys

if len(sys.argv) != 2:
    print("Usage: python update_version.py <new_version>")
    sys.exit(1)

new_version = sys.argv[1]

# Update version.py
with open("version.py", "w") as f:
    f.write(f'__version__ = "{new_version}"\n')

print(f"Updated version.py to {new_version}")

# Run generate_version_info.py
subprocess.run([sys.executable, "generate_version_info.py"])

print("Version updated successfully!")
