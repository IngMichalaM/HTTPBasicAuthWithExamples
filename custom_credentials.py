from selenium.webdriver.common.by import By

def custom_credentials():
    """ Change the fields accordingly to your project """

    ## PYTHONSCRAPING
    url = 'https://pythonscraping.com/pages/auth/login.php'
    username = 'admin'
    password = 'admin'
    text_to_check = 'Hello'
    locator = (By.XPATH, '/html/body/p[1]')
    target_url_endpoint = 'login'

    return url, username, password, text_to_check, locator, target_url_endpoint


    ## WEBELEMENT CLICK
    # text_to_check = 'You have authorized successfully!'
    # locator = (By.CSS_SELECTOR, '.post-body h2')
    # url = 'https://www.webelement.click/stand/basic?lang=en'
    # username = 'webelement'
    # password = 'click'
    # target_url_endpoint = url
    #
    # return url, username, password, text_to_check, locator, target_url_endpoint

    ## HEROKUAPP
    # url = 'https://the-internet.herokuapp.com/basic_auth'
    # username = 'admin'
    # password = 'admin'
    # text_to_check = 'Basic Auth'
    # locator = (By.XPATH, '//*[@id="content"]/div/h3')
    #
    # return url, username, password, text_to_check, locator, target_url_endpoint



