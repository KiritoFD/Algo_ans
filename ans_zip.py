import requests
from PyPDF2 import PdfMerger
from pathlib import Path  # Added import for pathlib

# Create a directory to store the downloaded files, if it doesn't exist
output_dir = Path("Algo_answers")  # Use Path object for directory
output_dir.mkdir(parents=True, exist_ok=True)

base_url = "https://sites.math.rutgers.edu/~ajl213/CLRS/Ch"

downloaded_files = []  # To store paths of successfully downloaded files

for i in range(1, 36):
    file_url = f"{base_url}{i}.pdf"
    # Use Path object for file_name
    file_name = output_dir / f"Ch{i}.pdf"

    print(f"Downloading {file_url}...")
    try:
        response = requests.get(file_url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Successfully downloaded {file_name}")
        downloaded_files.append(file_name)  # Add Path object to list

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {file_url}. Error: {e}")

print("All downloads attempted.")

# Merge the downloaded PDFs
if downloaded_files:
    merger = PdfMerger()
    # Use Path object for merged_pdf_path
    merged_pdf_path = output_dir / "Ans_Merged.pdf"

    print(f"\nMerging {len(downloaded_files)} PDF files into {merged_pdf_path}...")

    for pdf_path_obj in downloaded_files:  # pdf_path_obj is now a Path object
        # Path.exists() is used implicitly by PdfMerger when opening,
        # but an explicit check is still good for a clear message.
        if pdf_path_obj.exists():
            try:
                # PyPDF2's append method can take a string path or a file object.
                # Passing the Path object directly might work if it's implicitly converted to string,
                # or use str(pdf_path_obj) to be explicit.
                # Most libraries handling file paths will accept Path objects directly in modern Python.
                merger.append(str(pdf_path_obj))
                print(f"Appended {pdf_path_obj}")
            except Exception as e:
                print(f"Could not append {pdf_path_obj}. Error: {e}")
        else:
            print(f"File {pdf_path_obj} not found, skipping.")

    try:
        with open(merged_pdf_path, 'wb') as f_out:
            merger.write(f_out)
        print(f"Successfully merged PDFs into {merged_pdf_path}")
    except Exception as e:
        print(f"Failed to write merged PDF. Error: {e}")
    finally:
        merger.close()
else:
    print("No files were downloaded successfully, so no merging will be done.")
