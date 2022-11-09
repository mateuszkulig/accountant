"""
xpathfinder.py
by Mateusz Kulig
Script to generate xpaths from clicks on elements in selenium webdriver browser.
"""
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

URL_GAZETA = "https://oauth.gazeta.pl/poczta/auth"

JS_SET_DOCUMENT_A = """
    document.a = document.getElementsByTagName('html')[0];
    """

JS_GET_CLICKED_ELEMENT = """
    document.addEventListener('click', function(e) {
    e = e || window.event;
    var target = e.target || e.srcElement;
    document.a = target;
    }, false);
    """

JS_GET_ARGS_FROM_ELEMENT = """
    var items = {};
    for (index = 0; index < arguments[0].attributes.length; ++index) { 
        items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value };
        return items;
    """

def combine_xpath(tag_name, attrs:dict) -> str:
    """combine xpath from element tag and attributes"""
    return f"//{tag_name}" + "".join(f"[@{k}=\"{attrs[k]}\"]" if k != "class" else f"[@{k}=\"{' '.join(val for val in attrs[k])}\"]" for k in attrs)    # to cool to hand

def start_listening(driver:webdriver.Chrome):
    """start listening for clicks"""
    driver.execute_script(JS_GET_CLICKED_ELEMENT)

    clicked_element: WebElement
    last_element = None
    while True:
        time.sleep(0.25)
        try:
            clicked_element = driver.execute_script("return document.a")
        except (selenium.common.exceptions.StaleElementReferenceException, AttributeError):
            driver.execute_script(JS_SET_DOCUMENT_A)
            continue

        if clicked_element == last_element:
            continue
        html = clicked_element.get_attribute('outerHTML')
        parsed_element = BeautifulSoup(html, 'html.parser').find()
        tag = parsed_element.name
        attributes = parsed_element.attrs
        xp = combine_xpath(tag, attributes)

        print('\n', xp)
        print(driver.find_element(by=By.XPATH, value=xp).get_attribute("outerHTML")[:100])

        last_element = clicked_element

if __name__ == "__main__":
    print("module loaded as main")



