# CSV_to_OTC
Convert "KepServer" CSV file to "OPC Quick Client" OTC file for a quick visualization of all tags in a datalogger.

**USAGE:**
- In KepServer, go to Data Logger, select Data Map and click on "Export CSV..."
- Save this CSV file to a folder on your local computer.
- Run CSV_to_OTC in this folder to generate an OTC file. If older OTC files exist, they will be overwritten.
- Open "OPC Quick Client". File, Open... and select the OTC file.

**Options:**
- No arguments: Process all .csv files in the current directory.
- 1 argument:
* If it's a .csv filename: Process the specific file in the current directory.
* If it's a directory: Process all .csv files in the directory.
- 2 arguments:
* Arguments can be in any order: .csv filename and directory.
* Process the specific file in the specified directory.
