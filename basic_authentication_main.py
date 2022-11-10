""" Dealing with the HTTP Basic Authentication window
    Url and user credentials need to be saved in custom_credentials.py file

    Methods available:
        - selenium-wire
        - requests
        - send the username and password directly in the url
        - pyint

    Methods to work on:
        - requestium (works like "requests". Not able to display the page)
        - javascript
        - DevTools
        - python proxy
        - HTTPsClient
        - Urlilib
    """

from basic_authentication_func import CustomBasicAuthWithExamples

################ CHANGE APPROPRIATELY ##############################################
#            Every imput goes to custom_credentials()                              #
####################################################################################

custom_auth = CustomBasicAuthWithExamples()

user_input = input('''Chose the method to use for the HTTPBasicAuthentication login:
           - s: selenium-wire
           - r: requests
           - d: send the username and password directly in the url
           - p: pyint
           - q: requestium
           - j: javascript
           - v: DevTools
           - x: python proxy
           - u: urllib

        Your choice is?: ''').lower()

if user_input == 's':
    custom_auth.login_seleniumwire()
elif user_input == 'r':
    custom_auth.login_requests()
elif user_input == 'd':
    custom_auth.login_direct_inj()
elif user_input == 'p':
    custom_auth.login_pyint()
elif user_input == 'q':
    custom_auth.login_requestium()
elif user_input == 'j':
    custom_auth.login_javascript()
elif user_input == 'v':
    custom_auth.login_devtools()
elif user_input == 'x':
    custom_auth.login_python_proxy() # proxy.start not working
elif user_input == 'u':
    custom_auth.login_urllib()
else:
    print('Unknown selection.')

