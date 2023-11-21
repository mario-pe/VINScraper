
import ipdb
import openpyxl
import logging
from prompt_toolkit.mouse_events import MouseButton
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.common import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep

from config import username, password, FILE_PATH, REMOVE_CONTENT_URL
from locators import (
    google_approval_button,
    login_button,
    next_username_input_name,
    next_username_xpath,
    password_input_name,
    password_next_button,
    button_new_block_request_xpath,
    input_block_address_xpath,
    button_send_block,
    button_send_block_request,
    all_results_xpath,
    page_exists_block_address_xpath,
    image_tab_xpath,
    google_image_link_link_input_id,
    google_image_link_radio_button_id, images_tab_xpath, request_send_correctly,
)

BLUE_VIN = "2C3CDZBT5LH210515"


PAGES_LINKS = []
IMAGES_LINKS = []

# VINS = [
#     "1hd1krp14kb602715",
#     "1hd1ydj16lb065180",
#     "1hd1ktc14jb673480",
#     "1hd1bxv14eb034736",
#     "1hd1kef14mb640278",
#     "1hd1jnv10eb023434",
# ]
VINS = [
    "1hd1kef14mb640278"
]


def load_vins():
    workbook = openpyxl.load_workbook(FILE_PATH)
    sheet = workbook.active
    for i in range(1, sheet.max_row + 1):
        VINS.append(sheet.cell(row=i, column=1).value.upper())


def init_driver():
    return uc.Chrome()


def login(driver):
    try:
        driver.get("https://www.google.com")
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, google_approval_button)).click()
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, login_button)).click()
        user_name_input_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.NAME, next_username_input_name))
        user_name_input_element.send_keys(username)
        driver.find_element(By.XPATH, next_username_xpath).click()
        password_input_name_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.NAME, password_input_name))
        password_input_name_element.send_keys(password)
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, password_next_button)).click()
    except Exception as e:
        sleep(1)
        password_input_name_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.NAME, password_input_name))
        password_input_name_element.send_keys(password)
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, password_next_button)).click()


def first_search(driver):
    try:
        search_textarea = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.TAG_NAME, "textarea"))
        search_textarea.send_keys("Dodge Challenger")
        search_textarea.submit()
    except Exception as e:
        ipdb.set_trace()
        logging.error(e)

def links_scrapper(driver, vin):
    links = []
    search_textarea = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.TAG_NAME, "textarea"))
    search_textarea.clear()
    search_textarea.send_keys(vin)
    search_textarea.submit()
    las = driver.find_elements(By.TAG_NAME, "a")
    for index, la in enumerate(las):
        href = la.get_attribute("href")
        if href:
            upper_href = href.upper()
            if "bid.cars".upper() in upper_href and f"-{vin.upper()}" in upper_href:
                links.append(href)
            if "ucars.pro".upper() in upper_href and f"-{vin.upper()}" in upper_href:
                links.append(href)
            if "stat.vin".upper() in upper_href and f"-{vin.upper()}" in upper_href:
                links.append(href)
            if "autohelperbot.com".upper() in upper_href and f"{vin.upper()}_" in upper_href:
                links.append(href)
            if "plc.auction".upper() in upper_href and f"-{vin.upper()}-" in upper_href:
                links.append(href)
            if "plc.ua".upper() in upper_href and f"-{vin.upper()}-" in upper_href:
                links.append(href)
    links = list(set(links))
    return [{"vin": vin, "link": l} for l in links]


def images_scrapper(driver, vin):
    links = []
    images_tab = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, images_tab_xpath))
    images_tab.click()
    action = ActionChains(driver)
    sleep(2)
    las = driver.find_elements(By.TAG_NAME, "img")

    for index, la in enumerate(las[10:]):
        try:
            action.move_to_element(la)
            sleep(0.1)
            action.context_click(la).send_keys(Keys.ESCAPE).perform()
            if index % 5 == 0:
                action.send_keys(Keys.ARROW_DOWN).perform()
        except ElementNotInteractableException as e:
            print("No href in tag a")
    las = driver.find_elements(By.TAG_NAME, "a")
    for index, la in enumerate(las):
        href = la.get_attribute("href")
        if href:
            upper_href = href.upper()
            if "bid.cars".upper() in upper_href and f"-{vin.upper()}-" in upper_href:
                links.append(href)
            if "ucars.pro".upper() in upper_href and f"-{vin.upper()}" in upper_href:
                links.append(href)
            if "stat.vin" in upper_href and f"-{vin.upper()}" in upper_href:
                links.append(href)
            if "autohelperbot.com".upper() in upper_href and f"{vin.upper()}_" in upper_href:
                links.append(href)
            if "plc.auction".upper() in upper_href and f"-{vin.upper()}-" in upper_href:
                links.append(href)
            if "plc.ua".upper() in upper_href and f"-{vin.upper()}-" in upper_href:
                links.append(href)

    links = list(set(links))
    return [{"vin": vin, "image_link": l} for l in links]



def block_pages_request(driver, links):
    for link in links:
        print(link["link"], link["vin"])

        driver.get(
            "https://search.google.com/search-console/remove-outdated-content"
        )
        button_new_block_request_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, button_new_block_request_xpath))
        button_new_block_request_element.click()
        input_block_address = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, input_block_address_xpath))
        input_block_address.send_keys(link["link"])
        # input_block_address.send_keys(link)  # zły link do odtworzenia sytuacji i zabezpieczenia NoSuchElementException
        import ipdb; ipdb.set_trace()
        driver.find_element(By.XPATH, button_send_block).click()
        try:
            page_exists_block_address_button = WebDriverWait(driver, 1).until(lambda d: d.find_element(By.XPATH, page_exists_block_address_xpath))
            page_exists_block_address_button.send_keys(link["vin"])
        except Exception:
            pass
        action = ActionChains(driver)
        action.send_keys(Keys.ESCAPE)
        try:
            driver.find_element(By.XPATH, button_send_block_request).click()
        except Exception:
            pass
        sleep(0.5)
        try:
            sleep(1)
            request_send_correctly_button = WebDriverWait(driver, 1).until(lambda d: d.find_element(By.XPATH, request_send_correctly))
            request_send_correctly_button.click()
        except Exception as e:
            print(f"Exception  --------------------- block_pages_request")
            driver.get(
                "https://search.google.com/search-console/remove-outdated-content"
            )
            continue



def block_images_request(driver, links):
    # driver.find_element(By.XPATH, button_new_block_request_xpath).click()
        for link in links:
            print(link["image_link"], link["vin"])
            # driver.get(
            #     "https://search.google.com/search-console/remove-outdated-content"
            # )
            driver.get(REMOVE_CONTENT_URL)
            import ipdb;
            ipdb.set_trace()
            button_new_block_request_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, button_new_block_request_xpath))
            button_new_block_request_element.click()

            image_tab_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, image_tab_xpath))
            image_tab_element.click()
            google_image_link_radio_button_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, google_image_link_radio_button_id))
            google_image_link_radio_button_element.click()
            input_block_image = driver.find_element(By.ID, google_image_link_link_input_id)

            print(f" link zdjecia  -----------   {link['image_link']}")
            input_block_image.send_keys(link["image_link"])
            driver.find_element(By.XPATH, button_send_block).click()
            try:
                sleep(1)
                request_send_correctly_button = WebDriverWait(driver, 2).until(
                    lambda d: d.find_element(By.XPATH, request_send_correctly))
                request_send_correctly_button.click()
            except Exception:
                pass
            try:
                page_exists_block_address_button = WebDriverWait(driver, 3).until(
                    lambda d: d.find_element(By.XPATH, page_exists_block_address_xpath))
                page_exists_block_address_button.send_keys(link["vin"])
            except Exception as e:
                print(f"Exception  --------------------- block_images_request")
                driver.find_element(By.XPATH, '//span[text()="Prześlij prośbę"]').click()
                try:
                    request_send_correctly_button = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, request_send_correctly))
                    request_send_correctly_button.click()
                except Exception:
                    pass
                continue



def back_to_all_results(driver):
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(0.5)
        driver.find_element(By.XPATH, all_results_xpath).click()
    except Exception:
        import ipdb

        ipdb.set_trace()


if __name__ == "__main__":
    import ipdb
    # load_vins()
    driver = init_driver()
    login(driver)
    first_search(driver)

    for vin in VINS:
        print(f"______________________________________________________vin: {vin}")
        page_links = links_scrapper(driver, vin)
        print(f"_____________________________________________________________________________page_links       len: {len(page_links)}")
        print(f"______________________________________________________page_links: {page_links}")
        # images_links = images_scrapper(driver, vin)
        images_links = [{'vin': '1hd1kef14mb640278', 'image_link': 'https://www.google.com/url?sa=i&url=https%3A%2F%2Fplc.ua%2Fauctions%2Flot%2Fharley-davidson-fl-2021-vin-1hd1kef14mb640278-1-64968443%2F&psig=AOvVaw0UWKeNtcXwHqgEYspThrJQ&ust=1700610464115000&source=images&cd=vfe&opi=89978449&ved=2ahUKEwjFkJjm4dOCAxWXhaQKHVl_DFMQr4kDegQIARBm'}]

        print(f"_____________________________________________________________________________image_links      len: {len(images_links)}")
        print(f"______________________________________________________image_links: {images_links}")
        # block_pages_request(driver, page_links)
        block_images_request(driver, images_links)
        back_to_all_results(driver)



    # print(f"______________________________________________________IMAGES_LINKS len    { len(IMAGES_LINKS) }")
    # try:
    #     block_images_request(driver, IMAGES_LINKS)
    # except Exception:
    #     ipdb.set_trace()

    # print(f"______________________________________________________PAGES_LINKS len    {len(PAGES_LINKS)}")
    # try:
    #
    #     block_pages_request(driver, PAGES_LINKS)
    # except Exception:
    #     ipdb.set_trace()
    ipdb.set_trace()
    driver.quit()
