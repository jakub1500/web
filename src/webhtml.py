from pathlib import Path
from bs4 import BeautifulSoup
from enum import Enum, auto

class WebState(Enum):
    NOT_LOGGED = auto()
    LOGIN_FAILED = auto()
    LOGGED = auto()

    def _instance_checker(self, other):
        if type(self) != type(other):
            raise RuntimeError(f"Cannot operate on non {self.__class__.name} object")

    def __lt__(self, other):
        self._instance_checker(other)
        return self.value < other.value
    
    def __le__(self, other):
        self._instance_checker(other)
        return self.value <= other.value

    def __eq__(self, other):
        self._instance_checker(other)
        return self.value == other.value

    def __gt__(self, other):
        self._instance_checker(other)
        return self.value > other.value
    
    def __ge__(self, other):
        self._instance_checker(other)
        return self.value >= other.value



class FrontEnd:
    def get_content(self, state: WebState):
        wb = WebBuilder()

        if state <= WebState.LOGIN_FAILED:
            wb.add_elements(java_script="login/login.js", css="login/login.css", html="login/login.html")
        else:
            wb.add_elements(html="logged/logged.html")
        return wb.get_web()

    
    def get_favicon(self):
        return Path("html/favicon.ico")
        

class WebBuilder:
    HTML_DIRECTORY = "html"

    def __init__(self):
        self.index_html_path = Path(f"{self.HTML_DIRECTORY}/index.html")
        if not self.index_html_path.exists():
            raise RuntimeError(f"HTML file under {self.index_html_path} doesn't exists")
        with open(self.index_html_path, "r", encoding="utf-8") as file:
            self.html_content = file.read()
        self.soup = BeautifulSoup(self.html_content, 'html.parser')

    def get_web(self):
        return self.soup.prettify()
    
    def _get_file_content(self, name):
        with open(f"{self.HTML_DIRECTORY}/{name}", "r", encoding="utf-8") as file:
            return file.read()

    def add_elements(self, java_script=None, css=None, html=None):
        if java_script is not None:
            self._add_javascript(java_script)
        if css is not None:
            self._add_css(css)
        if html is not None:
            self._add_html(html)

    def _add_javascript(self, name):
        js_scripts = self.soup.find('script')
        js_content = self._get_file_content(name)
        js_scripts.string += js_content

    def _add_css(self, name):
        css_scripts = self.soup.find('style')
        css_content = self._get_file_content(name)
        css_scripts.string += css_content

    def _add_html(self, name):
        html_content = self._get_file_content(name)
        new_soup = BeautifulSoup(html_content, 'html.parser')
        main_div = self.soup.find(id="main-div")
        main_div.append(new_soup)
