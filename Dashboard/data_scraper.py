from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Set the download directory within your codebase
download_dir = os.path.join(os.path.dirname(__file__), "download")


def delete_existing_csv_files():
    """
    Delete all CSV files in the download directory before scraping new data
    """
    try:
        # Create download directory if it doesn't exist
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Get all files in the download directory
        files = os.listdir(download_dir)

        # Delete each CSV file
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(download_dir, file)
                os.remove(file_path)

        return True, "Existing CSV files deleted successfully"
    except Exception as e:
        return False, f"Error while deleting CSV files: {str(e)}"


def scrape_onion_data(progress_callback=None):
    """
    Scrapes onion price data from the CEDA website and downloads it as CSV.
    """
    try:
        # First delete any existing CSV files
        success, message = delete_existing_csv_files()
        if progress_callback:
            progress_callback(message)

        if not success:
            return False, message
        # Create download directory if it doesn't exist
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        # Set up Chrome options for headless operation
        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
            "profile.default_content_setting_values.automatic_downloads": 1,
        }
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

        # Initialize Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        wait = WebDriverWait(driver, 20)

        if progress_callback:
            progress_callback("Initializing browser...")

        # Load the page
        url = "https://dca.ceda.ashoka.edu.in/index.php/home/timeseries"
        driver.get(url)
        if progress_callback:
            progress_callback("Page loaded successfully")
        time.sleep(3)

        try:
            # Select 'Daily' from Mode dropdown
            mode_dropdown = wait.until(EC.presence_of_element_located((By.ID, "mode")))
            Select(mode_dropdown).select_by_visible_text("Daily")
            if progress_callback:
                progress_callback("Selected Daily mode")
            time.sleep(2)

            # Select 'Vegetables' from Group dropdown
            group_dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "group"))
            )
            Select(group_dropdown).select_by_visible_text("Vegetables")
            if progress_callback:
                progress_callback("Selected Vegetables")
            time.sleep(2)

            # Select 'Onion' from Commodity dropdown
            commodity_dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "commodity"))
            )
            Select(commodity_dropdown).select_by_visible_text("Onion")
            if progress_callback:
                progress_callback("Selected Onion")
            time.sleep(2)

            # Select 'East Zone' from Zones dropdown
            zone_dropdown = wait.until(EC.presence_of_element_located((By.ID, "zone")))
            Select(zone_dropdown).select_by_visible_text("East Zone")
            if progress_callback:
                progress_callback("Selected East Zone")
            time.sleep(2)

            # Select 'All Centers' for East Zone
            center_dropdown = wait.until(
                EC.presence_of_element_located((By.ID, "centre"))
            )
            Select(center_dropdown).select_by_visible_text("All Centres")
            if progress_callback:
                progress_callback("Selected All Centres")
            time.sleep(2)

            # Click Submit button
            submit_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Submit']"))
            )
            submit_button.click()
            if progress_callback:
                progress_callback("Clicked Submit button")
            time.sleep(5)

            # Click download button
            download_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[@onclick='downloadCSV();']")
                )
            )
            driver.execute_script("arguments[0].click();", download_button)
            if progress_callback:
                progress_callback("Initiated download")

            # Wait and verify download
            time.sleep(10)
            files = os.listdir(download_dir)
            csv_files = [f for f in files if f.endswith(".csv")]
            if csv_files:
                return True, f"Download successful! Files: {csv_files}"
            else:
                return False, "No CSV file found in download directory"

        except Exception as e:
            return False, f"Error during form interaction: {str(e)}"

    except Exception as e:
        return False, f"An error occurred: {str(e)}"

    finally:
        try:
            driver.quit()
            if progress_callback:
                progress_callback("Browser closed successfully")
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error closing browser: {str(e)}")
