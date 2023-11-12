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
    google_image_link_radio_button_id, images_tab_xpath,
)

BLUE_VIN = "2C3CDZBT5LH210515"


PAGES_LINKS = []
# IMAGES_LINKS = []
IMAGES_LINKS = [
    {
        'image_link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.bid.cars%2F70477833_652eda4397916%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945-6.jpg&tbnid=HcdDtrR9dBqfFM&vet=12ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygFegQIARBO..i&imgrefurl=https%3A%2F%2Fbid.cars%2Fen%2Flot%2F1-70477833%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945&docid=fjLoi3EFSk-s8M&w=640&h=480&q=1C4RJFBG4JC273945&hl=pl&ved=2ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygFegQIARBO',
        'vin': '1C4RJFBG4JC273945'},
    {
        'image_link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.bid.cars%2F70477833_652eda4397916%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945-10.jpg&tbnid=Cwcg8BQm58HZEM&vet=12ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygHegQIARBS..i&imgrefurl=https%3A%2F%2Fbid.cars%2Fen%2Flot%2F1-70477833%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945&docid=fjLoi3EFSk-s8M&w=640&h=480&q=1C4RJFBG4JC273945&hl=pl&ved=2ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygHegQIARBS',
        'vin': '1C4RJFBG4JC273945'},
    {
        'image_link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.bid.cars%2F70477833_652eda4397916%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945-7.jpg&tbnid=BzwNeHmhjI3-aM&vet=12ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygGegQIARBQ..i&imgrefurl=https%3A%2F%2Fbid.cars%2Fen%2Flot%2F1-70477833%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945&docid=fjLoi3EFSk-s8M&w=640&h=480&q=1C4RJFBG4JC273945&hl=pl&ved=2ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygGegQIARBQ',
        'vin': '1C4RJFBG4JC273945'},
    {
        'image_link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimages.bid.cars%2F70477833_652eda4397916%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945-9.jpg&tbnid=TaoEUYx9IhXmkM&vet=12ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygIegQIARBU..i&imgrefurl=https%3A%2F%2Fbid.cars%2Fen%2Flot%2F1-70477833%2F2018-Jeep-Grand-Cherokee-1C4RJFBG4JC273945&docid=fjLoi3EFSk-s8M&w=640&h=480&q=1C4RJFBG4JC273945&hl=pl&ved=2ahUKEwiQm671qr6CAxXOu6QKHRd8BLsQMygIegQIARBU',
        'vin': '1C4RJFBG4JC273945'}
]

# VINS = []
VINS = [
    "WP1AB2A25FLA56998",
    "WBA8B3C50GK383844",
    "1C6RR7FT3HS755769",
    "JTDKAMFP8M3182214",
    "1C4RJFBG4JC273945",
    "LYV102RKXKB263123",
    "1FA6P8CF6K5186661",
    "1C4RJFBG6KC841906",
    "YV426MDB4F2590434",
    "YV4162XZ7K2021323",
    "1C4RJFBGXMC701005",
]
# VINS = ["1C6RR7FT3HS755769"]
# VINS = ["WP1AB2A25FLA56998", "WBA8B3C50GK383844"]


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
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, next_username_xpath)).click()
        password_input_name_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.NAME, password_input_name))
        password_input_name_element.send_keys(password)
        WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, password_next_button)).click()
    except Exception as e:
        ipdb.set_trace()
        logging.error(e)




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
            if "bid.cars".upper() in upper_href and f"-{vin}" in upper_href:
                links.append(href)
            if "ucars.pro".upper() in upper_href and f"-{vin}" in upper_href:
                links.append(href)
            if "stat.vin".upper() in upper_href and f"-{vin}" in upper_href:
                links.append(href)
            if "autohelperbot.com".upper() in upper_href and f"{vin}_" in upper_href:
                links.append(href)
            if "plc.auction".upper() in upper_href and f"-{vin}-" in upper_href:
                links.append(href)
            if "plc.ua".upper() in upper_href and f"-{vin}-" in upper_href:
                links.append(href)
    links = list(set(links))
    list_dict = [{"vin": vin, "link": l} for l in links]
    print(list_dict)
    PAGES_LINKS.extend(list_dict)


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
        if href and "imgres" in href:
            upper_href = href.upper()
            if "bid.cars".upper() in upper_href and f"-{vin}-" in upper_href:
                links.append(href)
            if "ucars.pro".upper() in upper_href and f"-{vin}" in upper_href:
                links.append(href)
            if "stat.vin" in upper_href and f"-{vin}" in upper_href:
                links.append(href)
            if "autohelperbot.com".upper() in upper_href and f"{vin}_" in upper_href:
                links.append(href)
            if "plc.auction".upper() in upper_href and f"-{vin}-" in upper_href:
                links.append(href)
            if "plc.ua".upper() in upper_href and f"-{vin}-" in upper_href:
                links.append(href)

    links = list(set(links))
    list_dict = [{"vin": vin, "image_link": l} for l in links]
    print(list_dict)
    IMAGES_LINKS.extend(list_dict)


def block_pages_request(driver, links):
    for link in links:
        try:
            driver.get(
                "https://search.google.com/search-console/remove-outdated-content"
            )
            button_new_block_request_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, button_new_block_request_xpath))
            button_new_block_request_element.click()
            input_block_address = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, input_block_address_xpath))
            input_block_address.send_keys(link["link"])
            # input_block_address.send_keys(link)  # zły link do odtworzenia sytuacji i zabezpieczenia NoSuchElementException
            driver.find_element(By.XPATH, button_send_block_request).click()

            driver.find_element(By.XPATH, page_exists_block_address_xpath).send_keys(
                link["vin"]
            )
            action = ActionChains(driver)
            action.send_keys(Keys.ESCAPE)
            driver.find_element(By.XPATH, '//span[text()="Prześlij prośbę"]').click()
        except Exception:
            import ipdb

            ipdb.set_trace()


def block_images_request(driver, links):
    # driver.find_element(By.XPATH, button_new_block_request_xpath).click()
    try:
        for link in links:
            driver.get(REMOVE_CONTENT_URL)
            button_new_block_request_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, button_new_block_request_xpath))
            button_new_block_request_element.click()

            image_tab_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.XPATH, image_tab_xpath))
            image_tab_element.click()

            google_image_link_radio_button_element = WebDriverWait(driver, 10).until(lambda d: d.find_element(By.ID, google_image_link_radio_button_id))
            google_image_link_radio_button_element.click()
            input_block_image = driver.find_element(
                By.ID, google_image_link_link_input_id
            )
            input_block_image.send_keys(link["image_link"])
            driver.find_element(By.XPATH, button_send_block).click()
            send_request_button_element = WebDriverWait(driver, 10).until(
                lambda d: d.find_element(By.XPATH, button_send_block_request))
            send_request_button_element.click()
    except Exception:
        import ipdb

        ipdb.set_trace()



def back_to_all_results(driver):
    try:
        driver.execute_script("window.scrollTo(0, 0);")
        sleep(0.5)
        driver.find_element(By.XPATH, all_results_xpath).click()
    except Exception:
        import ipdb

        ipdb.set_trace()


if __name__ == "__main__":
    # load_vins()
    try:
        driver = init_driver()
    except Exception:
        import ipdb

        ipdb.set_trace()

    try:
        login(driver)
    except Exception:
        import ipdb

        ipdb.set_trace()

    # try:
    #     first_search(driver)
    # except Exception:
    #     import ipdb
    #
    #     ipdb.set_trace()
    #
    # for vin in VINS:
    #     try:
    #         links_scrapper(driver, vin)
    #     except Exception:
    #         import ipdb
    #
    #         ipdb.set_trace()
    #
    #     try:
    #         images_scrapper(driver, vin)
    #     except Exception:
    #         import ipdb
    #
    #         ipdb.set_trace()
    #
    #     try:
    #         back_to_all_results(driver)
    #     except Exception:
    #         import ipdb
    #
    #         ipdb.set_trace()

    # try:
    #     block_pages_request(driver, PAGES_LINKS)
    # except Exception:
    #     import ipdb
    #     ipdb.set_trace()
    try:
        block_images_request(driver, IMAGES_LINKS)
    except Exception:
        import ipdb
        ipdb.set_trace()

    driver.quit()
