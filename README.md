# DarwinCore2 to DublinCore

This Python script transforms a DarwinCore2 dataset to standard DublinCore. 

The script transforms column titles in a CSV file to the XML attributes requested by EBSCO. If more columns are added to the data exports in the future, it is important that 
the outbound link remain the only value in the <dc:relation> field because the IR questionnaire lists that value as the outbound link tied to the "Online Access" in EDS.  

To use the script, download a CSV file (in this case, from IrisBG). Rename the CSV file ```input.csv``` or change the script 
to reflect the correct CSV file name in line 50. 

Make sure the CSV file is in the same directory as the Python script, then run ```python3 transform-con.py```. 
