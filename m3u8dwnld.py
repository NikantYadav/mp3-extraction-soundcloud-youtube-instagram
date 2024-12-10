from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests

def fncm3u8dwnld(input_url):
    chrome_options = Options()
    chrome_options.add_argument("--ignore-certificate-errors")  
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(seleniumwire_options={}, options=chrome_options)

    driver.get(input_url)


    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
        ).click()
        print("Cookie consent banner accepted.")
    except Exception as e:
        print("No cookie consent banner or failed to close it:", e)


    try:
        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.soundTitle__playButton .sc-button-play'))
        )
        
        
        driver.execute_script("arguments[0].scrollIntoView(true);", play_button)
        
        
        actions = ActionChains(driver)
        actions.move_to_element(play_button).click().perform()
        print("Play button clicked.")
    except Exception as e:
        print("Failed to click Play button:", e)


    time.sleep(5)

    desired_url = None

    for request in driver.requests:
        if request.response:
            if "m3u8" in request.url:
                desired_url = request.url
                break


    driver.quit()

    if desired_url:
        print(f"Found m3u8 URL")

        
        output_file = "playlist.m3u8"
        try:
            response = requests.get(desired_url)  
            response.raise_for_status()  

            
            with open(output_file, "wb") as file:
                file.write(response.content)

            print(f"File downloaded successfully and saved as {output_file}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download file: {e}")
    else:
        print("No m3u8 URL found.")