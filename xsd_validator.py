import os
import lxml.etree as ET

def validate_xml_with_xsd(xml_file_path, xsd_file_path):
    """
    Validates an XML file against an XSD schema.
    :param xml_file_path: Path to the XML file to validate
    :param xsd_file_path: Path to the XSD schema file
    :return: (is_valid, error_messages) -> A tuple where is_valid is a boolean indicating success,
             and error_messages contains any errors or an empty list
    """
    try:
        # Load the XSD schema
        with open(xsd_file_path, 'rb') as f:
            xsd_doc = ET.parse(f)
        xsd_schema = ET.XMLSchema(xsd_doc)

        # Parse and validate the XML file
        with open(xml_file_path, 'rb') as f:
            xml_doc = ET.parse(f)
        xsd_schema.assertValid(xml_doc)

        # If no exceptions, the XML is valid
        return True, []
    except ET.XMLSchemaError as e:
        # Return validation errors if XSD validation fails
        return False, [str(e)]
    except ET.XMLSyntaxError as e:
        # Handle XML parsing errors
        return False, [f"XML Syntax Error: {e}"]
    except Exception as e:
        # Handle other unexpected errors
        return False, [f"Unexpected Error: {e}"]

def main():
    # Path to the directory containing XML files
    xml_directory = "./xml_files"  # Change to your directory path
    xsd_file_path = "./schema.xsd"  # Change to your XSD schema file path

    # if not os.path.exists(xsd_file_path):
    #     print(f"Error: XSD file not found at '{xsd_file_path}'")
    #     return

    # Get a list of all XML files in the directory
    xml_files = [f for f in os.listdir(xml_directory) if f.endswith('.xml')]

    # if not xml_files:
    #     print(f"No XML files found in directory: {xml_directory}")
    #     return

    # Process each XML file
    for count, xml_file in enumerate(xml_files, start=1):
        xml_file_path = os.path.join(xml_directory, xml_file)
        #print(f"Processing File {count}: {xml_file}")

        try:
            # Validate the XML file with the XSD schema
            is_valid, errors = validate_xml_with_xsd(xml_file_path, xsd_file_path)

            if is_valid:
                #print(f"File {count}: {xml_file} - Validation Success")
                n=1
            else:
                print(f"File {count}: {xml_file} - Validation Failed")
                for error in errors:
                    print(f"  - {error}")
        except Exception as e:
            #print(f"File {count}: {xml_file} - Unexpected Error: {e}")
            n=2

if __name__ == "__main__":
    main()
