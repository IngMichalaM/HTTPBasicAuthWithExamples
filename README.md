# Dealing with the HTTPBasicAuthentication window

## About 
There are different methods how to get pass the basic authentification window when loging in a web page.
This script presents several of them. The four working methods are: 
 - selenium-wire
 - requests
 - send the username and password directly in the url
 - pyint

Possible methods to use when the previous do not work (not finished):
 - requestium
 - javascript
 - DevTools
 - python proxy
 - HTTPsClient
 - Urlilib 

## How to use it 
Fill the following info into the file *custom_credentials.py*.

1) For the webpage which you want to access you need to provide: 
  - url
  - username
  - password
2) In order to be able to check the successful login onto the page, you need to provide:
  - text (string) which you want to check. E.g.: text_to_check = 'You have authorized successfully!'
  - its locator:  locator = (By.CSS_SELECTOR, '.post-body h2')
  - the endpoint of the target url, e.g. "home"

Now run the main file *basic_authentication_main.py* and select the desired method:
 - s: selenium-wire
 - r: requests
 - d: directly send the username and password within the url
 - p: pyint (works only on Windows, only method that works with Frafos monitor so far)
 - q: requestium (not implemented yet)
 - j: javascript (not implemented yet)
 - v: DevTools (not implemented yet)
 - x: python proxy (not implemented yet)
 - u: urllib (not implemented yet)

## Example
In the custom_credentials.py you can find examples of webpages with the basic authentication:
- https://www.webelement.click/stand/basic?lang=en
- https://the-internet.herokuapp.com/basic_auth
- https://pythonscraping.com/pages/auth/login.php

Methods that work for these examples are: selenium-wire, requests, directly send the username and password within the url, and pyint.

# Problems
- *pyint* works only on Windows (tested on Win11/Chrome) and not on MacOS or Linux
- only for Chrome. Chrome needs to be in the PATH.

# Futher reading
- proxy.py - https://pypi.org/project/proxy.py/#start-proxypy
- sikuli - alternative to pyint https://alternativeto.net/software/sikuli/about/
- requestium - https://pypi.org/project/requestium/0.1.4/