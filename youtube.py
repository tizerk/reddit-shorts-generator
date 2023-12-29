# Code from https://github.com/redianmarku/youtube-autoupload-bot/blob/master/main.py

from dotenv import load_dotenv
import time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

load_dotenv()


def upload_youtube(nameofvid):
    print("YouTube - Starting Upload...")
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument(f"user-data-dir={os.getenv('user_data_dir')}")
    service = Service(f"{os.getenv('edge_driver_dir')}")
    driver = webdriver.Edge(service=service, options=options)
    driver.set_window_size(width=1000, height=800)

    driver.get("https://studio.youtube.com")
    time.sleep(3)
    upload_button = driver.find_element(By.XPATH, '//*[@id="upload-icon"]')
    upload_button.click()
    time.sleep(1)

    file_input = driver.find_element(By.XPATH, '//*[@id="content"]/input')
    simp_path = f"{nameofvid}"
    abs_path = os.path.abspath(simp_path)
    file_input.send_keys(abs_path)

    time.sleep(7)

    next_button = driver.find_element(By.XPATH, '//*[@id="next-button"]')
    for i in range(3):
        next_button.click()
        time.sleep(2)

    done_button = driver.find_element(By.XPATH, '//*[@id="done-button"]')
    done_button.click()
    time.sleep(5)
    driver.quit()
    print("YouTube - Upload Complete!")
