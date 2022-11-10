
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.auth import HTTPBasicAuth
from seleniumwire import webdriver
import base64
import autoit
from  requestium import Session
from selenium.common.exceptions import TimeoutException

from custom_credentials import custom_credentials

# I don't know how to put it within the class
# https://github.com/wkeeling/selenium-wire#example-add-a-request-header
def interceptor(request):
    url, username, password, text_to_check, locator, target_url_endpoint = custom_credentials()

    auth_b = username + ':' + password

    auth = (
        base64.encodebytes(auth_b.encode())
            .decode()
            .strip()
    )

    del request.headers['Authorization']  # Remember to delete the header first
    request.headers['Authorization'] = f'Basic {auth}'  # Spoof the referer


class CustomBasicAuthWithExamples:

    def __init__(self) -> None:
        self.url, self.username, self.password, self.text_to_check, self.locator, self.target_url_endpoint = custom_credentials()

    def check_content(self, content=None, driver=None) -> None:
        """ Check if the desired string (self.text_to_check) can be found on the page.
            - text_to_check is mandatory
            - either directly "content" of the page or the "driver" need to be provided
              """

        if driver is not None:
            content = driver.find_element(*self.locator).text
        #     print(f'The text in the first paragraph is: "{content}".')

        assert self.text_to_check in content, f'There is no "{self.text_to_check}" on the page.'

        print(f'OK ("{self.text_to_check}" found on the page).')

    def check_url(self, driver:webdriver, target_endpoint:str=None) -> None:
        """ Check the current url """

        # need to wait, since it takes time for the web page to fully load
        try:
            webpage = WebDriverWait(driver, 10).until(EC.url_contains(target_endpoint))
            print(f'We are on "{driver.current_url}".')
        except TypeError:
            print(f'We are somewhere else - we are on "{driver.current_url}".')
        except TimeoutException:
            print(f'We are somewhere else - we are on "{driver.current_url}".')


    # ############ REQUESTS ###############################################
    def login_requests(self) -> None:
        """ Using requests to get the page content.
            https://stackoverflow.com/questions/61992076/logging-into-website-using-requests-python
        """

        r = requests.get(self.url, auth=HTTPBasicAuth(self.username, self.password))
        print(f'Status code of the request is: {r.status_code}.')
        # print(r.content)

        self.check_content(content=str(r.content))

    # ################## Direct injection of the username and password #########################################
    def login_direct_inj(self):
        """ The username and password are directly incorporated in the URL as:
            https://username:password@url """

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)

        url_parts = self.url.split('//')
        new_url = 'https://' + self.username + ':' + self.password + '@' + url_parts[1]
        #url = 'http://{}:{}@{}'.format(username, password, url)
        # print(new_url)
        driver.get(new_url)
        self.check_content(driver=driver)
        driver.close()

    # ################## PYINT #########################################
    def fill_in_login_credentials(self, driver:webdriver, username:str, password: str) -> None:
        """ Use the autoit to fill the username and password input fields ,
            Does not work in headless mode .

            if 'pip install autoit' does not work, try: 'pip install -U pyautoit'

            Only for windows  """

        try:
           # automatically type where we are (in the popup authentification window)
           autoit.win_wait_active("", 3)  # Make sure you give blank since the cursor is at userid
           autoit.send('{}{}'.format(username, '{Tab}'))
           autoit.send('{}{}'.format(password, '{Enter}'))
        except Exception:
           print('General exception in the "fill_in_login_credentials" for filling the login form.')
           driver.close()

    def login_pyint(self):
        """ Modul Pyint is used to type in the username and password in the login window.
            It types where the cursor currently is. Does not work with headless mode.

            Dos not work for MacOS and Linux. Other possibilities are for example
                https://alternativeto.net/software/sikuli/about/ """

        # there might be a problem when importing webdriver from seleniumwire instead of selenium
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self.url)
        time.sleep(2)
        self.fill_in_login_credentials(driver, self.username, self.password)

        if self.target_url_endpoint:
            self.check_url(driver=driver, target_endpoint=self.target_url_endpoint)
        else:
            self.check_url(driver=driver)

        self.check_content(driver=driver)

        driver.close()

    # ################## REQUESTIUIM #########################################

    def login_requestium(self):
        """ Requestium is an integration layer between Requests and Selenium for automation of web actions.
            Instalation: pip install requestium
            URL: https://tryolabs.com/blog/2017/11/22/requestium-integration-layer-requests-selenium-web-automation
                 https://github.com/tryolabs/requestium/blob/master/README.md

            Dependencies: from requestium import Session

        """

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        # chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)

        s = Session(webdriver_path='./chromedriver',
                    browser='chrome',
                    default_timeout=10,
                    webdriver_options={'arguments': ['--start-maximized']}
                    )

        # works like "requests" to retrieve the content from the page. But what about the browser?
        r = s.get(self.url, auth=HTTPBasicAuth(self.username, self.password))
        print(r.status_code)
        print(r.content)
        time.sleep(2)

        s.transfer_session_cookies_to_driver()  # You can mantain the session if needed
        s.driver.get(self.url)
        print('todo: how to get to the browser after login?')
        s.driver.close()

    # ################## JAVASCRIPT #########################################
    def login_javascript():
        print('login_javascript not implemented yer.')


    # ################  Chrome DevTools ###########################################

    def login_devtools():
        """
        URL: https://medium.com/automationmaster/handling-basic-authentication-window-with-selenium-webdriver-and-devtools-api-ec716965fdb6
             https://www.browserstack.com/guide/handling-login-popups-in-selenium-webdriver-and-java

        """
        print('"DevTools" not implemented yet.')
        print('Obviously, python selenium does not have getDevTools method. ')
        print('But it is actually prety similar to login_seleniumwire()')
        #
        # # set the browser
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--start-maximized")
        # # chrome_options.add_argument('headless')
        # driver = webdriver.Chrome(options=chrome_options)
        #
        # # devTools.createSession()
        # devTools = driver.getDevTools()
        # devTools.createSession()
        #
        # # Concatenate username and password separated by colon and store it any String object
        # auth = username + ':' + password
        # message_bytes = auth.encode('ascii')
        # # https://stackabuse.com/encoding-and-decoding-base64-strings-in-python/
        # encoded_aut = base64.b64encode(message_bytes) # Base64.getEncoder().encodeToString(auth.getBytes());
        #
        # print(encoded_aut)
        # #
        # # message_bytes = message.encode('ascii')
        # # base64_bytes = base64.b64encode(message_bytes)
        # # base64_message = base64_bytes.decode('ascii')
        #
        # print(base64_message)

        # DevTools devTools = driver.getDevTools();
        # devTools.createSession();

    # #################### PYTHON PROXY #######################################
    def login_python_proxy():
        print('login_python_proxy not implemented ')
        # https://www.webelement.click/en/four_simple_steps_to_add_custom_http_headers_in_selenium_webdriver_tests_in_python


    # ############  URLLIB ###############################################
    def login_urllib():
        """
            URL:  https://stackoverflow.com/questions/8862492/python-proxy-error-with-requests-library/8862633#8862633
                  https://urllib3.readthedocs.io/en/1.26.x/advanced-usage.html#ssl-warnings
        """
        # from urllib import request
        # request.urlopen("your URL", proxies=request.getproxies())
        print('login_urllib not implemented yet')

    def login_seleniumwire(self) -> None:
        """ Using selenium-wire to add the Authentication header to the get requests.

            URL: https://pypi.org/project/selenium-wire/#intercepting-requests-and-responses
                 https://stackoverflow.com/questions/72312662/how-to-add-a-request-header-at-selenium-wire-as-passed-argument
                 https://github.com/wkeeling/selenium-wire#example-add-a-request-header

        """

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=chrome_options)
        driver.request_interceptor = interceptor
        driver.get(self.url)
        print(f'Current URL is: {driver.current_url} (method seleniumwire).')
        print(f'Waiting for the "{self.target_url_endpoint}" endpoint ... ')
        self.check_url(driver=driver, target_endpoint=self.target_url_endpoint)
        # self.check_content(driver=driver)

        driver.close()
