import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import version

template = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
# filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
# Set not needed items to zero 0.
  filevers=(0, 5, 3, 0),
  prodvers=(0, 5, 3, 0),
# Contains a bitmask that specifies the valid bits 'flags'r
  mask=0x3f,
# Contains a bitmask that specifies the Boolean attributes of the file.
  flags=0x0,
# The operating system for which this file was designed.
# 0x4 - NT and there is no need to change it.
  OS=0x4,
# The general type of file.
# 0x1 - the file is an application.
  fileType=0x1,
# The function of the file.
# 0x0 - the function is not defined for this fileType
  subtype=0x0,
# Creation date and time stamp.
  date=(0, 0)
),
  kids=[
  StringFileInfo([
    StringTable(
      u'040904B0',
      [StringStruct(u'CompanyName', u''),
      StringStruct(u'FileDescription', u''),
      StringStruct(u'FileVersion', u'{version}'),
      StringStruct(u'InternalName', u''),
      StringStruct(u'LegalCopyright', u'travellerse Copyright'),
      StringStruct(u'OriginalFilename', u'RainClassroomAssistant.exe'),
      StringStruct(u'ProductName', u'RainClassroomAssistant'),
      StringStruct(u'ProductVersion', u'{version}')])
  ]),
  VarFileInfo([VarStruct(u'Translation', [2052, 1200])])
  ]
)"""

# Parse version
parts = version.__version__.split(".")
major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

content = template.replace("filevers=(0, 5, 3, 0)", f"filevers=({major}, {minor}, {patch}, 0)")
content = content.replace("prodvers=(0, 5, 3, 0)", f"prodvers=({major}, {minor}, {patch}, 0)")
content = content.replace("{version}", version.__version__)

with open("file_version_info.txt", "w", encoding="utf-8") as f:
    f.write(content)

print(f"Updated file_version_info.txt to version {version.__version__}")
