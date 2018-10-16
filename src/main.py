"""
1. Create a web page or GUI that will accept a URL input from the user

2. The URL should extract all text from the page (no tags!)

3. Display these statistics for the extracted data:
    - Each word's frequency
    - Longest word
    - Most common letter

Uses PyQt5 for GUI
Tested with Python 3.5
"""

import sys
import requests
import re
from collections import Counter
from lxml import html, etree
from lxml.html.clean import Cleaner
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Form(QWidget):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        urlLabel = QLabel("URL:")
        self.urlLine = QLineEdit()
        self.submitButton = QPushButton("&Submit")
        self.submitButton.clicked.connect(self.submitUrl)

        inputlayout = QVBoxLayout()
        inputlayout.addWidget(urlLabel)
        inputlayout.addWidget(self.urlLine)
        inputlayout.addWidget(self.submitButton)

        self.outputBrowser = QTextBrowser()

        mainLayout = QGridLayout()
        mainLayout.addLayout(inputlayout, 0, 1)
        mainLayout.addWidget(self.outputBrowser, 1, 0, 1, 2)

        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 500, 600)
        self.setWindowTitle("Web page statistics")

    def submitUrl(self):
        url = self.urlLine.text().strip()

        if not url:
            self.outputBrowser.setText("Empty URL")
            return

        try:
            page = fetch_from_url(url)
        except:
            self.outputBrowser.setText("Error fetching data from URL")
        else:
            text = get_statistics(page)
            self.outputBrowser.setText(text)


def fetch_from_url(url):
    """ (str) -> str
    Fetches data from given url
    Raises error if resource is unreachable
    """
    f = requests.get(url)
    f.raise_for_status()
    return f.text


def get_statistics(page):
    """ (str) -> str
    Accepts page source as input
    Gets statistics of a web page and formats it for output:
    - Longest word
    - Most common letter
    - Each word's frequency
    """
    parsed_text = parse_from_string(page)
    word_list = re.findall(r'\w+', parsed_text.lower())

    word = get_longest_word(word_list)
    letter = get_most_common_letter(word_list)
    word_count = count_words(word_list)

    lines = []
    lines.append('<b>Longest word:</b>')
    lines.append(word)
    lines.append('<b>Most common letter:</b>')
    lines.append('{0}: {1}'.format(letter[0], letter[1]))
    lines.append('<b>Word count:</b>')
    for k,v in word_count:
        lines.append('{0}: {1}'.format(k,v))

    return '<br>'.join(lines)


def parse_from_string(s):
    """ (str) -> str
    Extracts all text from web page
    """
    cleaner = Cleaner(javascript=True, style=True)
    cleaned_html = cleaner.clean_html(html.document_fromstring(s))
    return '\n'.join(etree.XPath("//text()")(cleaned_html))


def count_words(word_list):
    """ (list of str) -> dict
    Counts number of occurences of the words,
    returns in sorted order
    """
    return sorted(dict(Counter(word_list)).items(), key=lambda x: x[1], reverse=True)


def get_longest_word(word_list):
    """ (list of str) -> str
    Gets longest word
    """
    return max(word_list, key=len)


def get_most_common_letter(word_list):
    """ (list of str) -> tuple
    Gets most common letter and its frequency
    """
    return Counter(''.join(word_list)).most_common(1)[0]


if __name__ == '__main__':

    app = QApplication(sys.argv)

    screen = Form()
    screen.show()

    sys.exit(app.exec_())
