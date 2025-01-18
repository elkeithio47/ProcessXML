import os
from fpdf import FPDF


def text_to_pdf(txt_file, pdf_file):
    """
    Convert a text file to a PDF file.
    """
    try:
        # Create an FPDF instance
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Read the content of the text file
        with open(txt_file, 'r', encoding='utf-8') as file:
            for line in file:
                pdf.cell(0, 10, line.strip(), ln=True)

        # Save content to a PDF file
        pdf.output(pdf_file)
        print(f"Successfully converted {txt_file} to {pdf_file}.")
    except Exception as e:
        print(f"Error processing {txt_file}: {e}")


def process_txt_directory(directory):
    """
    Process all .txt files in the given directory and convert them to .pdf.
    """
    try:
        # Ensure the directory exists
        if not os.path.isdir(directory):
            print(f"Directory {directory} does not exist.")
            return

        # Get a list of all .txt files in the directory
        txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        if not txt_files:
            print(f"No .txt files found in directory {directory}.")
            return

        # Process each .txt file
        for txt_file in txt_files:
            txt_path = os.path.join(directory, txt_file)
            pdf_path = os.path.join(directory, txt_file.replace('.txt', '.pdf'))

            # Convert Text to PDF
            text_to_pdf(txt_path, pdf_path)

    except Exception as e:
        print(f"Error processing directory {directory}: {e}")


if __name__ == "__main__":
    # Specify the directory containing .txt files
    input_directory = "./../xml_files_as_txt/combined"

    # Call the processing function
    process_txt_directory(input_directory)

