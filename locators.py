# zgody
google_approval_button = f'//div[text()="Zaakceptuj wszystko"]'


#login
google_login_button_content = "Zaloguj się"
next_username_input_name = 'identifier'
next_username_xpath = '//span[text()="Dalej"]'
password_input_name = 'Passwd'
password_next_button = 'passwordNext'
login_button = '//span[text()="Zaloguj się"]'

#images
images_tab_xpath = '//span[text()="Grafika"]'
all_results_xpath = '//a[text()="Wszystko"]'

#block request
button_new_block_request_xpath = '//span[text()="Nowa prośba"]'
input_block_address_xpath = "//input[@placeholder='Wpisz URL strony']"


button_send_block = '//span[text()="Prześlij"]'
# page_exists_block_address_xpath = "//input[@placeholder='Wpisz słowo']"
page_exists_block_address_xpath = "/html/body/div[7]/div[2]/div/div[1]/div/div/div[2]/label/input"
button_send_block_request = '//span[text()="Prześlij prośbę"]'
image_tab_xpath = "/html/body/div[7]/div[2]/div/div[1]/div/div/div[1]/div/div/span/button[2]/span[3]"
google_image_link_radio_button_id = "c13"
google_image_link_link_input_id = "c16"
google_image_link_input_xpath = "//input[@placeholder='URL z&nbsp;wyników wyszukiwania']"

def tests():
    import undetected_chromedriver as uc
    from selenium.webdriver import ActionChains, Keys
    la = 'sds'
    driver.sand_keys(link["link"])
    driver.find_element(By.XPATH, "//span[text()='Wpisz słowo']").send_keys("2C3CDZBT5LH210515")
    driver.find_element(By.XPATH, "/html/body/div[7]/div[2]/div/div[1]/div/div/div[2]/label/input").send_keys("2C3CDZBT5LH210515")
    driver.find_element(By.XPATH, '//span[text()="Prześlij prośbę"]').click()

    la.get_attribute("id")
    driver = uc.Chrome()
    action = ActionChains(driver)
    action.context_click(la).send_keys(Keys.SHIFT, Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
    action.context_click(la).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.RETURN).perform()
    action.context_click(la).send_keys(Keys.SHIFT, Keys.ARROW_DOWN).perform()
    action.send_keys(Keys.SHIFT, Keys.ARROW_DOWN)
    driver.find_element(By.XPATH, '//a[text()="Wszystko"]').click()