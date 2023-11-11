import openpyxl
from prompt_toolkit.mouse_events import MouseButton
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.common import ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains, Keys
from time import sleep

from config import username, password, FILE_PATH
from locators import (
    google_approval_button,
    login_button,
    next_username_input_name,
    next_username_xpath,
    password_input_name,
    password_next_button,
    button_new_block_request_xpath,
    input_block_address_xpath,
    button_send_block_request,
    all_results_xpath, page_exists_block_address_xpath, image_tab_xpath, google_image_link_link_input_id,
    google_image_link_radio_button_id,
)

BLUE_VIN = "2C3CDZBT5LH210515"


PAGES_LINKS = []
# IMAGES_LINKS = []
IMAGES_LINKS = [
    {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg.plc.ua%2Ffull%2Fimg3%2F01%2F2019%2F18%2F94%2F47021efb9dcf9777d32fe81247600110%2Fa9aa13e00739476eb71342ee5abd5efd_hrs.jpg&tbnid=fhLVI24UBKjAjM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygBegQIARBK..i&imgrefurl=https%3A%2F%2Fplc.ua%2Fen%2Fauctions%2Flot%2Fdodge-challenger-2019-vin-2c3cdzl93kh606802-1-63715472%2F&docid=UahM0ynIUhxnrM&w=1280&h=960&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygBegQIARBK', 'vin': '2C3CDZL93KH606802'},
    {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fcs.copart.com%2Fv1%2FAUTH_svc.pdoc00001%2FLPP447%2Ffc7255d9541d4fc1b7b44891f387b965_ful.jpg&tbnid=i27yn30mzpvLTM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygCegQIARBM..i&imgrefurl=https%3A%2F%2Fucars.pro%2Flot%2F127451736-2019-dodge-challenger-srt-hellcat-redeye-2c3cdzl93kh606802&docid=w094uwGjQAb7UM&w=640&h=480&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygCegQIARBM', 'vin': '2C3CDZL93KH606802'},
    # {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fcs.copart.com%2Fv1%2FAUTH_svc.pdoc00001%2FLPP439%2Fd790388e83f349b68eddc92660e97be3_ful.jpg&tbnid=Q3dAohWUjUGaAM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygEegQIARBQ..i&imgrefurl=https%3A%2F%2Fucars.pro%2Flot%2F127451736-2019-dodge-challenger-srt-hellcat-redeye-2c3cdzl93kh606802&docid=w094uwGjQAb7UM&w=640&h=480&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygEegQIARBQ', 'vin': '2C3CDZL93KH606802'},
    # {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fcs.copart.com%2Fv1%2FAUTH_svc.pdoc00001%2FLPP439%2Fb1b64fd4fd114438beb640f21be0a0c2_ful.jpg&tbnid=8h3MeYjw8FtHzM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygHegQIARBW..i&imgrefurl=https%3A%2F%2Fucars.pro%2Flot%2F127451736-2019-dodge-challenger-srt-hellcat-redeye-2c3cdzl93kh606802&docid=w094uwGjQAb7UM&w=640&h=480&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygHegQIARBW', 'vin': '2C3CDZL93KH606802'}, {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg.plc.ua%2Ffull%2Fimg3%2F01%2F2019%2F18%2F94%2F47021efb9dcf9777d32fe81247600110%2F2c221f53b40148a7a5edaee5368c028a_hrs.jpg&tbnid=RXE0PhAjEs9yoM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygGegQIARBU..i&imgrefurl=https%3A%2F%2Fplc.ua%2Fen%2Fauctions%2Flot%2Fdodge-challenger-2019-vin-2c3cdzl93kh606802-1-63715472%2F&docid=UahM0ynIUhxnrM&w=1280&h=960&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygGegQIARBU', 'vin': '2C3CDZL93KH606802'}, {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg.plc.ua%2Ffull%2Fimg3%2F01%2F2019%2F18%2F94%2Fb6e750be2696b84ce327f9103fc0052b%2Fd6d047cdaf2b40a092744014c30fce3f_hrs.jpg&tbnid=dcplpSvyjUO33M&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygIegQIARBY..i&imgrefurl=https%3A%2F%2Fplc.ua%2Fen%2Fauctions%2Flot%2Fdodge-challenger-2019-vin-2c3cdzl93kh606802-1-63715472%2F&docid=UahM0ynIUhxnrM&w=1280&h=960&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygIegQIARBY', 'vin': '2C3CDZL93KH606802'}, {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg.plc.ua%2Ffull%2Fimg3%2F01%2F2019%2F18%2F94%2F47021efb9dcf9777d32fe81247600110%2F3c89b4d1063a49869872a7bbfee638aa_hrs.jpg&tbnid=CzX2xXELicgEMM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygAegQIARBI..i&imgrefurl=https%3A%2F%2Fplc.ua%2Fen%2Fauctions%2Flot%2Fdodge-challenger-2019-vin-2c3cdzl93kh606802-1-63715472%2F&docid=UahM0ynIUhxnrM&w=1280&h=960&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygAegQIARBI', 'vin': '2C3CDZL93KH606802'}, {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fimg.plc.ua%2Ffull%2Fimg3%2F01%2F2019%2F18%2F94%2F47021efb9dcf9777d32fe81247600110%2F0a471b95a91840c5a24b44e01dc4adae_hrs.jpg&tbnid=GhqEFyTKyoVxQM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygDegQIARBO..i&imgrefurl=https%3A%2F%2Fplc.ua%2Fen%2Fauctions%2Flot%2Fdodge-challenger-2019-vin-2c3cdzl93kh606802-1-63715472%2F&docid=UahM0ynIUhxnrM&w=1280&h=960&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygDegQIARBO', 'vin': '2C3CDZL93KH606802'},
    # {'link': 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fcs.copart.com%2Fv1%2FAUTH_svc.pdoc00001%2FLPP439%2Fbb0df910e3934b0aab6e98c636ed5f8a_ful.jpg&tbnid=urFGGq-Phy_VCM&vet=12ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygJegQIARBa..i&imgrefurl=https%3A%2F%2Fucars.pro%2Flot%2F127451736-2019-dodge-challenger-srt-hellcat-redeye-2c3cdzl93kh606802&docid=w094uwGjQAb7UM&w=640&h=480&itg=1&q=2C3CDZL93KH606802&hl=pl&ved=2ahUKEwjYne6zjMaBAxUPDRAIHbZuA4UQMygJegQIARBa', 'vin': '2C3CDZL93KH606802'}
]

VINS = []
# VINS = ["2C3CDZBT5LH210515", "3CZRU6H75JM727661"]


def load_vins():
    workbook = openpyxl.load_workbook(FILE_PATH)
    sheet = workbook.active
    for i in range(1, sheet.max_row + 1):
        VINS.append(sheet.cell(row=i, column=1).value.upper())


def init_driver():
    return uc.Chrome()


def login(driver):
    driver.get("https://www.google.com")
    sleep(2)
    driver.find_element(By.XPATH, google_approval_button).click()
    driver.find_element(By.XPATH, login_button).click()
    sleep(3)
    driver.find_element(By.NAME, next_username_input_name).send_keys(username)
    driver.find_element(By.XPATH, next_username_xpath).click()
    sleep(5)
    driver.find_element(By.NAME, password_input_name).send_keys(password)
    driver.find_element(By.ID, password_next_button).click()
    sleep(3)


def first_search(driver):
    sleep(2)
    search_textarea = driver.find_elements(By.TAG_NAME, "textarea")[0]
    search_textarea.send_keys("Dodge Challenger")
    search_textarea.submit()


def links_scrapper(driver, vin):
    links = []
    search_textarea = driver.find_elements(By.TAG_NAME, "textarea")[0]
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
    list_dict = [{"link": l, "vin": vin} for l in links]
    print(list_dict)
    PAGES_LINKS.extend(list_dict)


def images_scrapper(driver, vin):
    links = []
    driver.find_element(By.XPATH, '//span[text()="Grafika"]').click()  # zmienić link
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
    list_dict = [{"link": l, "vin": vin} for l in links]
    print(list_dict)
    IMAGES_LINKS.extend(list_dict)


def block_pages_request(driver, links):
    vin = ""
    # lopp over dictionary
    for link in links:
        driver.get("https://search.google.com/search-console/remove-outdated-content")
        driver.find_element(By.XPATH, button_new_block_request_xpath).click()
        input_block_address = driver.find_element(By.XPATH, input_block_address_xpath)
        input_block_address.send_keys(link)
        driver.find_element(By.XPATH, button_send_block_request).click()

        import ipdb

        ipdb.set_trace()
        driver.find_element(
            By.XPATH, page_exists_block_address_xpath
        ).send_keys(vin)
        action = ActionChains(driver)
        action.send_keys(Keys.ESCAPE)
        driver.find_element(By.XPATH, '//span[text()="Prześlij prośbę"]').click()

def block_images_request(driver, links):
    # driver.find_element(By.XPATH, button_new_block_request_xpath).click()
    for link in links:
        import ipdb;
        driver.get("https://search.google.com/search-console/remove-outdated-content")
        ipdb.set_trace()
        sleep(2)
        driver.find_element(By.XPATH, button_new_block_request_xpath).click()
        driver.find_element(By.XPATH, image_tab_xpath).click()
        driver.find_element(By.ID, google_image_link_radio_button_id).click()
        input_block_image = driver.find_element(By.ID, google_image_link_link_input_id)
        input_block_image.send_keys(link["link"])

        driver.find_element(By.XPATH, '//span[text()="Prześlij prośbę"]').click()
        try:
            print(link)
            sleep(2)
            # driver.find_element(By.XPATH,'//*[@id="lblTad"]/span[3]').click()
            driver.find_element(By.XPATH, '//span[text()="Grafika"]').click()
            driver.find_element(By.XPATH, button_send_block_request).click()

        # from selenium.webdriver.support.wait import WebDriverWait
        # from selenium.webdriver.support import expected_conditions as EC
        # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe")))
        # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Grafika"]'))).click()

        # WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//span[text()="Grafika"]')))

        except:
            import ipdb; ipdb.set_trace()
        dd.send_keys(link)
    # button_image_block_request = '//span[text()="Grafika"]'
    # input_block_address = driver.find_element(By.XPATH, button_image_block_request)

    pass


def back_to_all_results(driver):
    driver.execute_script("window.scrollTo(0, 0);")
    sleep(0.5)
    driver.find_element(By.XPATH, all_results_xpath).click()


if __name__ == "__main__":
    # load_vins()
    driver = init_driver()
    login(driver)
    first_search(driver)
    #
    # for vin in VINS:
    #     links_scrapper(driver, vin)
    #     images_scrapper(driver, vin)
    #     back_to_all_results(driver)
    # block_pages_request(driver, PAGES_LINKS)
    block_images_request(driver, IMAGES_LINKS)
    driver.quit()
