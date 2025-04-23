# DarwinCore2 to DublinCore

This Python script transforms a DarwinCore2 dataset to standard DublinCore. 

The script transforms column titles in a CSV file to XML attributes. 

To use the script, download a CSV file (in this case, from IrisBG). Rename the CSV file ```input.csv``` or change the script 
to reflect the correct CSV file name in line 50. 

Make sure the CSV file is in the same directory as the Python script, then run ```python3 transform-con.py```. 

The DublinCore XML file will be named output.xml once the process is completed. You can use something like https://jsonformatter.org/xml-formatter to format 
the XML for human readability. 
