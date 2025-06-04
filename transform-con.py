import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom

# DarwinCore2 to DublinCore
def transform_csv(input_csv, output_xml):
    mappings = {
        'TaxonName': 'dc:title',
        'Distribution': 'dcterms:spatial',
        'Family': 'dc:description',
        'CommonNameDefault': 'dc:description',
        'LifeForm': 'dc:description',
        'ItemLocationName': 'dc:description',
        'NameID': 'dc:identifier'
        # Removed QRCodeURL from mappings as it will be handled separately
    }
    
    # Creates root element
    root = ET.Element('root')
    
    # Reads CSV, concatenates values for dc:description, creates separate dc:relation for URL
    # writes to XML    
    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = ET.Element('record')
            description_values = []
            for key, value in row.items():
                if key in mappings:
                    if mappings[key] == 'dc:description':
                        description_values.append(value)
                    else:
                        elem = ET.Element(mappings[key])
                        elem.text = value
                        record.append(elem)
                # Handle QRCodeURL separately for dc:relation
                elif key == 'QRCodeURL' and value:
                    relation_elem = ET.Element('dc:relation')
                    relation_elem.text = 'https://scbg.gardenexplorer.org/' + value
                    record.append(relation_elem)
                    
            if description_values:
                desc_elem = ET.Element('dc:description')
                desc_elem.text = '; '.join(description_values)
                record.append(desc_elem)
            root.append(record)

    # Format the XML with proper indentation
    tree = ET.ElementTree(root)
    
    # Attempt indentation 
    try:
        ET.indent(tree, space="  ")
        # Write the indented XML
        tree.write(output_xml, encoding='utf-8', xml_declaration=True)
    except AttributeError:
        # Fallback for older Python versions using minidom
        rough_string = ET.tostring(root, encoding='utf-8')
        reparsed = xml.dom.minidom.parseString(rough_string)
        with open(output_xml, 'w', encoding='utf-8') as f:
            f.write(reparsed.toprettyxml(indent="  "))
    
    print(f"Formatted XML written to {output_xml}")

if __name__ == "__main__":
    transform_csv('input.csv', 'output.xml') # change file names or be sure csv is correctly named
