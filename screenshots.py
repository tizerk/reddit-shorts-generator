import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


def get_screenshots(post, id_list):
    driver, wait = initialize_driver(post.url)
    post_ss(driver, wait, post)
    comment_ss(driver, wait, id_list)
    driver.quit()


def post_ss(driver, wait, post):
    driver.execute_script(
        "document.querySelector('._1tvdSTbdxaK-BnUbzUIqIY').style.display = 'none';"
    )
    driver.execute_script(
        "document.querySelector('._1cubpGNEaCAVnpJl1KBPcO').style.display = 'none';"
    )
    title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Post")))
    driver.execute_script("window.focus();")
    ss_name = f"Screenshots/title-{post.id}.png"
    with open(ss_name, "wb") as file:
        file.write(title.screenshot_as_png)


def comment_ss(driver, wait, id_list):
    for id in id_list:
        try:
            comment = wait.until(EC.presence_of_element_located((By.ID, f"t1_{id}")))
        except TimeoutException:
            more_comments = wait.until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR,
                        "div._3sf33-9rVAO_v4y0pIW_CH[style='padding-left: 0px;']",
                    )
                )
            )
            more_comments.click()
            comment = wait.until(EC.presence_of_element_located((By.ID, f"t1_{id}")))
        driver.execute_script("window.focus();")
        ss_name = f"Screenshots/comment-{id}.png"
        with open(ss_name, "wb") as file:
            file.write(comment.screenshot_as_png)


def initialize_driver(url):
    options = Options()
    options.add_argument(f"user-data-dir={os.getenv('user_data_dir')}")
    options.add_argument("profile-directory=Default")
    service = Service(f"{os.getenv('edge_driver_dir')}")
    driver = webdriver.Edge(service=service, options=options)
    wait = WebDriverWait(driver, timeout=10)
    driver.set_window_size(width=600, height=800)
    driver.get(url)

    return driver, wait
