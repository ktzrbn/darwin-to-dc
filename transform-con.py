import csv
import xml.etree.ElementTree as ET

# DarwinCore2 to DublinCore
def transform_csv(input_csv, output_xml):
    mappings = {
        'CommonNameAll': 'dc:title',
        'Distribution': 'dc:coverage:spatial',
        'ItemLocationName': 'dc:description',
        'NameID': 'dc:identifier'
    }
    
    # Description field mappings
    description_fields = {
        'TaxonName': 'Scientific value',
        'Family': 'Family',
        'Genus': 'Genus',
        'Species': 'Species',
        'Cultivar': 'Cultivar',
        'LifeForm': 'Life Form'
    }
    
# Root element
    root = ET.Element('root')
    
# Reads CSV, concatenates values for dc:description, prepends gardenexplorer URL, transforms
# writes to XML    

    with open(input_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = ET.Element('record')
            description_values = []
            
            # Add formatted description fields
            for field, label in description_fields.items():
                if field in row and row[field]:
                    description_values.append(f"{label}: {row[field]}")
            
            # Process other mappings
            for key, value in row.items():
                if key in mappings:
                    if mappings[key] == 'dc:description':
                        description_values.append(value)
                    else:
                        elem = ET.Element(mappings[key])
                        elem.text = value
                        record.append(elem)
                elif key == 'QRCodeURL' and value:
                    # Create dc:relation element for QRCodeURL
                    relation_elem = ET.Element('dc:relation')
                    relation_elem.text = 'https://scbg.gardenexplorer.org/' + value
                    record.append(relation_elem)
            
            # Create description element
            if description_values:
                desc_elem = ET.Element('dc:description')
                desc_elem.text = '; '.join(description_values)
                record.append(desc_elem)
            
            root.append(record)

    # Formats XML with human readable indentation and writes file
    ET.indent(root, space="  ", level=0)
    tree = ET.ElementTree(root)
    tree.write(output_xml, encoding='utf-8', xml_declaration=True)
    print(f"XML written to {output_xml}")

if __name__ == "__main__":
    transform_csv('input.csv', 'output.xml') # change file names or be sure csv is correctly named