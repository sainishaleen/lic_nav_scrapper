import os
import logging

# Logging configuration
log_file = "logs/scraping_log.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
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

# Random user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/602.3.12 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36"
]

# Download directory
base_download_dir = os.path.join(os.getcwd(), 'downloads')