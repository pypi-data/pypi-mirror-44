## **Convert Landsat 8 MTL metadata files to XML.**

**Usage:**

mtl_to_xml has three modes.

1. -t Target mode converts a single MTL file to XML.
The script must be run in the same directory as the MTL file.
Example: mtl_to_xml -t your_landsat_file_MTL.txt

2. -d Directory mode converts all MTL files in the current directory to XML.
The script must be run in the same directory as the MTL files.
Example: mtl_to_xml -d

3. -s Scan mode is the same as directory mode, but converts all MTL files in the current directory and sub-directories.
Example: mtl_to_xml -s 
