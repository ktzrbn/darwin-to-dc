import csv
import xml.etree.ElementTree as ET

# DarwinCore2 to DublinCore
def transform_csv(input_csv, output_xml):
    mappings = {
        'TaxonName': 'dc:title',
        'Distribution': 'dcterms:spatial',
        'Family': 'dc:description',
        'CommonNameDefault': 'dc:description',
        'LifeForm': 'dc:description',
        'ItemLocationName': 'dc:description',
        'NameID': 'dc:identifier',
        'QRCodeURL': 'dc:description'
    }
    
# Creates root element
    root = ET.Element('root')
    
# Reads CSV, concatenates values for dc:description, prepends gardenexplorer URL, transforms 
# writes to XML    

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = ET.Element('record')
            description_values = []
            for key, value in row.items():
                if key in mappings:
                    if mappings[key] == 'dc:description':
                        if key == 'QRCodeURL':
                            description_values.append('https://scbg.gardenexplorer.org/' + (value or ''))
                        else:
                            description_values.append(value)
                    else:
                        elem = ET.Element(mappings[key])
                        elem.text = value
                        record.append(elem)
            if description_values:
                desc_elem = ET.Element('dc:description')
                desc_elem.text = '; '.join(description_values)
                record.append(desc_elem)
            root.append(record)

    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding='utf-8', xml_declaration=True)
    print(f"XML written to {output_xml}")

if __name__ == "__main__":
    transform_csv('input.csv', 'output.xml') # change file names or be sure csv is correctly named 
