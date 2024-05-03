from selenium.webdriver.common.keys import Keys
import time
import requests
import os
import re
import zipfile
from flask import Blueprint, request, send_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the Flask blueprint
models = Blueprint("models", __name__)

# Define the absolute path for the static directory
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

@models.route('/scrape', methods=['POST'])
def scrape():
    try:
        # Get the URL from the request
        url = request.form.get('url')

        # Fetch the URL content
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            return f"Failed to fetch URL. Status code: {response.status_code}", 500

        # Check if the URL is provided in the request
        if not url:
            return "URL is missing in the request.", 400

        # Use the absolute path for the static directory
        path = STATIC_DIR

        # Initialize the Chrome driver with specific options
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # Initialize the Chrome driver
        driver = webdriver.Chrome(options=options)

        # Navigate to the provided URL
        driver.get(url)

        # Define helper functions for waiting and finding elements
        wait = WebDriverWait(driver, 20)

        # Extract business name and location
        business_name = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.TIHn2 > div > div.lMbq3e > div:nth-child(1) > h1"))).text
        print(business_name)
        try:
            target_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(8) > div.K7ntAe.zSdcRe"))
            )

            target_element1 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(10)"))
            )
            target_element2 = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.lMbq3e"))
            )

            # Scroll the element five times
            for _ in range(1):
                driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
                time.sleep(1)  # Adjust the sleep time if needed
                driver.execute_script("arguments[0].scrollIntoView(true);", target_element1)
                time.sleep(5)
                location = WebDriverWait(driver, 0.2).until(EC.visibility_of_element_located((By.CLASS_NAME, "rogA2c"))).text
                print(location)
                driver.execute_script("arguments[0].scrollIntoView(true);", target_element2)
                time.sleep(2)
        except Exception as e:
            print(f"error first scroll: {e}")

        # Wait for review button to be clickable and click it
        try:
            #  the first XPath
            path1 =  "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(3) > div.LRkQ2 > div.Gpq6kf.fontTitleSmall"
            review_button = driver.find_element(By.CSS_SELECTOR, path1).click()
        except Exception as e:
            print(f"Error clicking on review button using path1: {e}")

        try:
            path3 = "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(3) > div.LRkQ2 > div.Gpq6kf.fontTitleSmall"
            review_button = driver.find_element(By.CSS_SELECTOR, path3).click()
        except Exception as e:
            print(f"Error clicking on review button using path3: {e}")

        try:
            #  the second XPath
            path2 = "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2) > div.LRkQ2 > div.Gpq6kf.fontTitleSmall"
            review_button = driver.find_element(By.CSS_SELECTOR, path2).click()
        except Exception as e:
            print(f"Error clicking on review button using path2: {e}")

        # Find the sidebar element
        try:
            sidebar = driver.find_element(By.CSS_SELECTOR, "#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf")

            # Scroll the sidebar using Keys.ARROW_DOWN
            for _ in range(200):  # Adjust the range to scroll multiple times
                sidebar.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.2)

            # Find and click on all "More" buttons
            more_buttons = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button.w8nwRe.kyuRq")))
            
            for button in more_buttons:
                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(0.2)
                button.click()
                time.sleep(0.2)  # Add a short pause to allow content to load
                print("Clicked on a 'More' button")
                
        except Exception as e:
            print(f"Error clicking on 'More' buttons: {e}")

        try:
            WebDriverWait(driver , 60).until(EC.visibility_of_all_elements_located((By.CLASS_NAME,"d4r55")))
            author_elements = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "d4r55")))
            authors = [author.text for author in author_elements]

            review_elements = WebDriverWait(driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "span.wiI7pd")))
            reviews = [review.text for review in review_elements]

            for author, review in zip(authors, reviews):
                print("Author:", author)
                print("Review:", review)
                print()  # Add a line break between each author-review pair

        except Exception as e:
            print(f"Error extracting author names and reviews: {e}")
            return f"An error occurred: {str(e)}", 500

        # Download images
        folder_name = re.sub(r"[^\w\s]", "", business_name).lower().replace(" ", "_")
        img_folder = download_images(folder_name, driver)

        # Create a text file with scraped data
        txt_folder = os.path.join(path, folder_name, "Text-folder")
        os.makedirs(txt_folder, exist_ok=True)

        # Write scraped data to the text file
        zip_file_path = os.path.join(path, folder_name, "scraped_data.zip")
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            file_name = "listing.txt"
            file_path = os.path.join(txt_folder, file_name)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(f"Title: {business_name}\n")
                file.write(f"Location: {location}\n")
                for author, review in zip(authors, reviews):
                    file.write(f"Username: {author}\n")
                    file.write(f"Review: {review}\n")
            zip_file.write(file_path, arcname=file_name)

            # Add images to the zip
            for root, _, files in os.walk(img_folder):
                for file in files:
                    zip_file.write(os.path.join(root, file), arcname=os.path.join(folder_name, "images", file))

        # Quit the Chrome driver
        driver.quit()

        # Return the zip file for download
        return send_file(
            zip_file_path,
            as_attachment=True,
            download_name='scraped_data.zip'
        )

    except Exception as e:
        # Handle exceptions appropriately
        return f"An error occurred: {str(e)}", 500

def download_images(folder_name, driver):
    path = STATIC_DIR

    img_folder = os.path.join(path, folder_name, "images-folder")
    os.makedirs(img_folder, exist_ok=True)

    # Wait for the image elements to be present
    wait = WebDriverWait(driver, 20)
    image_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.KtCyie button.Tya61d")))

    for index, img in enumerate(image_elements):
        # Get the background image URL from the style attribute
        style_attribute = img.get_attribute("style")
        img_url_match = re.search(r'url\("(.+)"\)', style_attribute)
        if img_url_match:
            img_url = img_url_match.group(1)
            try:
                # Download the image
                img_name = f"image_{index}.jpg"  # You can customize the image naming convention here
                img_data = requests.get(img_url).content
                with open(os.path.join(img_folder, img_name), "wb") as f:
                    f.write(img_data)
                    print(f"Downloaded: {img_name}")
            except Exception as e:
                print(f"Error downloading image {img_url}: {e}")

    return img_folder
