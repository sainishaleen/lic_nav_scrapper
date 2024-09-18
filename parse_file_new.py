import os
import pandas as pd
from bs4 import BeautifulSoup
import logging

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

# List of companies
companies = [
    'HDFC Life Insurance Company Limited',
    'Bajaj Allianz Life Insurance Company Limited',
    'Max Life Insurance Company Limited',
    'TATA AIA Life Insurance Company Limited',
    'SBI Life Insurance Company Limited',
    'ICICI Prudential Life Insurance Company Limited'
]

# Define the base path for the files
base_path = '/home/strange/nav_scrapper/downloads'

def read_xls_as_html(file_path):
    try:
        logging.info(f"Reading file: {file_path}")
        # Open the .xls file and read the content as text
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the content with BeautifulSoup
        soup = BeautifulSoup(content, "html.parser")

        # Find the table in the HTML
        table = soup.find("table")

        # Extract table headers from the third row (header row)
        headers = [header.get_text().strip() for header in table.find_all("th")]

        # Extract table rows (skip first two rows)
        data = []
        for row in table.find_all("tr")[1:]:  # Skip the header row
            cols = row.find_all("td")
            cols = [ele.get_text().strip() for ele in cols]
            data.append(cols)

        # Create a pandas DataFrame from the extracted data
        df = pd.DataFrame(data, columns=headers)

        # Drop the original Sr. No. column
        if 'Sr.no.' in df.columns:
            df = df.drop(columns=['Sr.no.'])

        return df

    except Exception as e:
        logging.error(f"Error reading the .xls file: {e}")
        return None

def process_files(base_path, companies):
    all_data = pd.DataFrame()  # Initialize an empty DataFrame to store all data

    # Loop through each company
    for company in companies:
        company_folder = os.path.join(base_path, company.replace(' ', '_').lower())
        logging.info(f"Processing files for company: {company}")

        # Check if the company folder exists
        if not os.path.exists(company_folder):
            logging.warning(f"Directory not found for {company}")
            continue

        # Iterate through all .xls files in the company folder
        for file_name in os.listdir(company_folder):
            if file_name.endswith('.xls'):
                file_path = os.path.join(company_folder, file_name)
                logging.info(f"Found file: {file_path}")

                # Extract date from file name
                try:
                    date_part = file_name.split('_')[-1].replace('.xls', '')
                except IndexError:
                    logging.error(f"Could not extract date from file: {file_name}")
                    continue

                # Read the .xls file
                df = read_xls_as_html(file_path)

                if df is not None:
                    # Add company name and date to the DataFrame
                    df['Company Name'] = company
                    df['Date'] = date_part

                    # Create a new 'Sr.no.' column with a correct sequence starting from 1
                    df['Sr.no.'] = range(1, len(df) + 1)

                    # Append the DataFrame to the all_data DataFrame
                    all_data = pd.concat([all_data, df], ignore_index=True)
                else:
                    logging.error(f"Failed to process file: {file_path}")

    return all_data

def save_to_csv(df, output_file):
    try:
        logging.info(f"Saving data to CSV file: {output_file}")
        # Save the final DataFrame to a CSV file
        df.to_csv(output_file, index=False)
        logging.info(f"Data successfully saved to {output_file}")
    except Exception as e:
        logging.error(f"Error saving data to CSV: {e}")

# Main execution
logging.info("Starting file processing...")

# Process all files and store the final DataFrame
all_data = process_files(base_path, companies)

# Save the final DataFrame to a CSV file
if not all_data.empty:
    save_to_csv(all_data, 'final_fund_navs_data.csv')
else:
    logging.info("No data to save.")

logging.info("File processing complete.")
