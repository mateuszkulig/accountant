"""
xpathfinder.py
by Mateusz Kulig
Script to generate xpaths from clicks on elements in selenium webdriver browser.
"""

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

from pprint import pprint

URL_GAZETA = "https://konto.gazeta.pl/konto/rejestracja.do"

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
    return f"//{tag_name}".join(f"[@{k}=\"{attrs[k]}\"]" if k != "class" else f"[@{k}=\"{''.join(val for val in attrs[k])}\"]" for k in attrs)


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()

    driver.get(URL_GAZETA)
    driver.execute_script(JS_GET_CLICKED_ELEMENT)

    clicked_element: WebElement
    while True:
        leave = input("enter to continue; type anything to exit\n")
        if leave:
            break
        clicked_element = driver.execute_script("return document.a")
        html = clicked_element.get_attribute('outerHTML')
        parsed_element = BeautifulSoup(html, 'html.parser').find()
        tag = parsed_element.name
        attributes = parsed_element.attrs
        xp = combine_xpath(tag, attributes)
        print(xp)

    driver.quit()
