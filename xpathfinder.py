from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
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

driver = webdriver.Chrome()
driver.maximize_window()

driver.get(URL_GAZETA)
driver.execute_script(JS_GET_CLICKED_ELEMENT)

clicked_element:WebElement
while True:
    input("enter to continue\n")

    clicked_element = driver.execute_script("return document.a")
    html = clicked_element.get_attribute('outerHTML')
    # print(f"value of a is: {a.get_attribute('outerHTML')}")

driver.quit()