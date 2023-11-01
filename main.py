import sys
import json
import argparse
import random

from pathlib import Path
from time import sleep

from selenium import webdriver

from Modules.Voltaire import VoltaireTool


def parse_arg() -> argparse:
    parser = argparse.ArgumentParser(prog='Miaouss',
                                     description='/!\\ This program is for educational purpose. /!\\\n'
                                                 'It demonstrate the power of Selenium by resolving level of Voltaire.\n'
                                                 'The Voltaire project is a website to train french.',
                                     epilog='Dev with ❤ by Vhelen',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-u', '--username', help='Username to log in', type=str, required=True)
    parser.add_argument('-p', '--password', help='Password to log in', type=str, required=True)
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action="store_true")
    args = parser.parse_args()

    return args


def init_webdriver() -> webdriver:
    browser_chrome = webdriver.Chrome()

    browser_chrome.maximize_window()

    return browser_chrome

def create_json_file():
    if not Path('Solutions/data.json').is_file():
        data = {
            'solution': {
                'drag_and_drop': {},
                'sentence': {},
                'click_on_word_right': {},
                'click_on_word_mistake': {}
            }
        }

        with open('Solutions/data.json', 'w+') as outfile:
            json.dump(data, outfile)

def main(username, password):
    browser = init_webdriver()

    voltaire_tool = VoltaireTool(browser)

    login_success = voltaire_tool.login(user_args.username, user_args.password)

    if login_success:
        module_to_launch = voltaire_tool.find_module()

        if not module_to_launch:
            sys.exit("Module not found")
    else:
        sys.exit("Error log in")
    
    # Début de la résolution du niveau
    while True:
        # Résolution d'une question
        voltaire_tool.type_question()

        sleep(random.randint(4, 10))

        # Question suivante
        voltaire_tool.next_question()


if __name__ == "__main__":
    user_args = parse_arg()

    create_json_file()

    main(user_args.username, user_args.password) 


