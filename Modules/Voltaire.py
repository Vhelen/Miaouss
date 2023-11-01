import sys
import json
from time import sleep
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


@dataclass
class VoltaireTool:
    browser: webdriver

    def check_exists_by_xpath(self, xpath)-> bool:
        try:
            self.browser.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            return False
        return True

    def login(self, usr: str, pwd: str) -> bool:
        # Login page URL
        self.browser.get('https://www.projet-voltaire.fr/voltaire/com.woonoz.gwt.woonoz.Voltaire/Voltaire.html')
        # Wait for page to load
        sleep(2)

        # Type username
        text_area = self.browser.find_element(By.ID, 'user_pseudonym')
        text_area.send_keys(usr)
        sleep(0.5)

        # Type password
        text_area = self.browser.find_element(By.ID, 'user_password')
        text_area.send_keys(pwd)
        sleep(1.5)

        # Submit the form
        submit_button = self.browser.find_element(By.ID, "login-btn")
        submit_button.click()

        # Wait for the server to log us
        sleep(10)

        return True

    def find_module(self) -> bool:
        module = None

        advancement_div = self.browser.find_elements(By.XPATH,"//div[@class='activity-selector-cell-progression-text']"
                                                              "[contains(text(), '%')]")
        for ava in advancement_div:
            if not ava.text == "" and "100" not in ava.text:
                module = ava

        if module is not None:
            self.browser.execute_script("arguments[0].click();", module)

            sleep(10)

            return True
        else:
            return False
    
    def type_question(self)-> bool:
        self.intensive_training()

        self.end_module()

        if self.check_exists_by_xpath("//div[@class='pointAndClick questionDisplayed']"):
            self.click_on_word()

        elif self.check_exists_by_xpath("//div[@class='clickOnWord questionDisplayed clickOnRight']"):
            self.click_on_word_right()

        elif self.check_exists_by_xpath("//div[@class='clickOnWord questionDisplayed clickOnMistake']"):
            self.click_on_word_mistake()

        elif self.check_exists_by_xpath("//div[@class='classify drag-and-drop-mode questionDisplayed']"):
            self.resolve_drag_and_drop_v2()
        else:
            print("question inconnu")
            input()
            sys.exit("Question inconnu")

        return True

    def click_on_word(self):
        with open("Solutions/data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        sentence = self.browser.find_element(By.XPATH, "//div[@class='sentence']").text

        save_answer = False

        if sentence in data['solution']['sentence']:
            answer = data['solution']['sentence'][sentence]

            if answer == "":
                answer = self.browser.find_element(By.XPATH, "//button[@id='btn_pas_de_faute']")
            else:
                pos_answer = answer.rfind('.')
                if pos_answer == -1:
                    pos_answer = answer.rfind('\'')
                if pos_answer == -1:
                    pos_answer = answer.rfind(',')
                if pos_answer == -1:
                    pos_answer = answer.rfind(' ')

                if pos_answer != -1:
                    answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                + answer[pos_answer + 1:] +
                                                                "')][@class='pointAndClickSpan']")
                else:
                    answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                + answer + "')][@class='pointAndClickSpan']")

            answer.click()

            sleep(3)
        else:
            # On ne connait pas la réponse
            save_answer = True

        
        if save_answer:
            sentence = self.browser.find_element(By.XPATH, "//div[@class='sentence']")
            span = sentence.find_element(By.XPATH, "//span[@class='pointAndClickSpan']")
            span.click()
            sleep(3)

            if self.browser.find_element(By.XPATH, "//div[@class='answerStatusBarLabel2']").text \
                    != "Il n'y a pas de faute.":

                div_answer = self.browser.find_element(By.XPATH, "//span[@class='answerWord']")

                data['solution']['sentence'][sentence.text] = div_answer.text
            else:
                data['solution']['sentence'][sentence.text] = ""

            with open("Solutions/data.json", "w") as jsonFile:
                json.dump(data, jsonFile)

    def click_on_word_right(self):
        with open("Solutions/data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        instructions = self.browser.find_element(By.CLASS_NAME, "instructions").text

        sentence = self.browser.find_element(By.XPATH, "//div[@class='sentence']").text

        possibilities = sentence.split(" – ")

        if len(possibilities) == 1:
            save_answer = False

            if instructions in data['solution']['click_on_word_right']:
                if sentence in data['solution']['click_on_word_right'][instructions]:
                    answer = data['solution']['click_on_word_right'][instructions][sentence]

                    if answer == "":
                        answer = self.browser.find_element(By.XPATH, "//button[@id='btn_pas_de_faute']")
                    else:
                        pos_answer = answer.rfind('.')
                        if pos_answer == -1:
                            pos_answer = answer.rfind('\'')
                        if pos_answer == -1:
                            pos_answer = answer.rfind(',')
                        if pos_answer == -1:
                            pos_answer = answer.rfind(' ')

                        if pos_answer != -1:
                            answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                        + answer[pos_answer + 1:] +
                                                                        "')][@class='pointAndClickSpan']")
                        else:
                            answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                        + answer + "')][@class='pointAndClickSpan']")

                    answer.click()

                    sleep(3)
                else:
                    # On ne connait pas la réponse
                    save_answer = True
            else:
                data['solution']['click_on_word_right'][instructions] = {}
                save_answer = True

            if save_answer:
                sentence = self.browser.find_element(By.XPATH, "//div[@class='sentence']")
                span = sentence.find_element(By.XPATH, "//span[@class='pointAndClickSpan']")
                span.click()
                sleep(3)

                if self.browser.find_element(By.XPATH, "//div[@class='answerStatusBarLabel2']").text \
                        != "Il n'y a pas de faute.":
                    div_answer = self.browser.find_element(By.XPATH, "//span[@class='answerWord']")

                    data['solution']['click_on_word_right'][instructions][sentence.text] = div_answer.text
                else:
                    data['solution']['click_on_word_right'][instructions][sentence.text] = ""

        else:
            answer = None
            save_answer = False

            if instructions in data['solution']['click_on_word_right']:
                for possibility in possibilities:
                    if possibility in data['solution']['click_on_word_right'][instructions]:
                        pos_answer = possibility.rfind('.')
                        if pos_answer == -1:
                            pos_answer = possibility.rfind('\'')
                        if pos_answer == -1:
                            pos_answer = possibility.rfind(',')
                        if pos_answer == -1:
                            pos_answer = possibility.rfind(' ')

                        if pos_answer != -1:
                            answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                        + possibility[pos_answer + 1:]
                                                                        + "')][@class='pointAndClickSpan']")
                        else:
                            answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                        + possibility + "')]"
                                                                                        "[@class='pointAndClickSpan']")
            else:
                data['solution']['click_on_word_right'][instructions] = []

            if answer is None:
                pos_answer = possibilities[0].rfind('.')
                if pos_answer == -1:
                    pos_answer = possibilities[0].rfind('\'')
                if pos_answer == -1:
                    pos_answer = possibilities[0].rfind(',')
                if pos_answer == -1:
                    pos_answer = possibilities[0].rfind(' ')

                if pos_answer != -1:
                    answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                + possibilities[0][pos_answer + 1:]
                                                                + "')][@class='pointAndClickSpan']")
                else:
                    answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                + possibilities[0] + "')][@class='pointAndClickSpan']")
                save_answer = True

            answer.click()

            if save_answer:
                div_answer = self.browser.find_element(By.XPATH, "//span[@class='answerWord']")

                for possibility in possibilities:
                    if div_answer.text in possibility:
                        data['solution']['click_on_word_right'][instructions].append(possibility)

        with open("Solutions/data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def click_on_word_mistake(self):
        with open("Solutions/data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        instructions = self.browser.find_element(By.CLASS_NAME, "instructions").text

        sentence = self.browser.find_element(By.XPATH, "//div[@class='sentence']").text

        save_answer = False

        if instructions in data['solution']['click_on_word_mistake']:
            if sentence in data['solution']['click_on_word_mistake'][instructions]:
                answer = data['solution']['click_on_word_mistake'][instructions][sentence]

                if answer == "":
                    answer = self.browser.find_element(By.XPATH, "//button[@id='btn_pas_de_faute']")
                else:
                    pos_answer = answer.rfind('.')
                    if pos_answer == -1:
                        pos_answer = answer.rfind('\'')
                    if pos_answer == -1:
                        pos_answer = answer.rfind(',')
                    if pos_answer == -1:
                        pos_answer = answer.rfind(' ')

                    if pos_answer != -1:
                        answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                    + answer[pos_answer + 1:]
                                                                    + "')][@class='pointAndClickSpan']")
                    else:
                        answer = self.browser.find_element(By.XPATH, "//span[contains(text(), '"
                                                                    + answer + "')][@class='pointAndClickSpan']")

                answer.click()

                sleep(3)
            else:
                # On ne connait pas la réponse
                save_answer = True
        else:
            data['solution']['click_on_word_mistake'][instructions] = {}
            save_answer = True

        if save_answer:
            sentence = self.browser.find_element(By.XPATH, "//div[@class='sentence']")
            span = sentence.find_element(By.XPATH, "//span[@class='pointAndClickSpan']")
            span.click()
            sleep(3)

            if self.browser.find_element(By.XPATH, "//div[@class='answerStatusBarLabel2']").text \
                    != "Il n'y a pas de faute.":

                div_answer = self.browser.find_element(By.XPATH, "//span[@class='answerWord']")

                data['solution']['click_on_word_mistake'][instructions][sentence.text] = div_answer.text
            else:
                data['solution']['click_on_word_mistake'][instructions][sentence.text] = ""

        with open("Solutions/data.json", "w") as jsonFile:
            json.dump(data, jsonFile)


    def resolve_drag_and_drop_v2(self)-> None:
        with open("Solutions/data.json", "r") as jsonFile:
            data = json.load(jsonFile)

        instructions = self.browser.find_element(By.CLASS_NAME, "instructions").text 

        btns_to_classify = self.browser.find_elements(By.XPATH, "//button[@class='classifyProposal "
                                                               "dragdrop-draggable dragdrop-handle']")

        headers = self.browser.find_elements(By.XPATH, "//button[@class='header']")

        action = ActionChains(self.browser)

        # Si question déjà connu
        if instructions in data['solution']['drag_and_drop']:
            for header in headers:
                # Si header est connu
                if header.text in data['solution']['drag_and_drop'][instructions]:
                    for btn in btns_to_classify:
                        # Si le bouton est connu
                        if btn.text in data['solution']['drag_and_drop'][instructions][header.text]:
                            drop_to = header.find_element(By.XPATH,'..')
                            action.drag_and_drop(btn, drop_to)

                # Si header inconnu, on l'ajoute
                else:
                    data['solution']['drag_and_drop'][instructions][header.text] = []
        # Si question pas encore connu
        else:
            # On enregistre l'instruction
            data['solution']['drag_and_drop'][instructions] = {}

            # On ajoute les headers
            for header in headers:
                data['solution']['drag_and_drop'][instructions][header.text] = []

        action.perform()

        btn_validate = self.browser.find_element(By.ID, 'btn_validate_answer')

        btn_validate.click()

        sleep(3)

        # Sauvegarde des nouvelles données si il y a
        btns_save_answer = self.browser.find_elements(By.XPATH, "//button[@class='classifyProposal "
                                                               "incorrect missingCategory']")

        # Pour chaque boutton qui n'est pas encore connu
        for btn in btns_save_answer:
            drop_to = btn.find_element(By.XPATH, '..')
            drop_to = drop_to.find_element(By.XPATH, '..')
            header_answer = drop_to.find_element(By.CLASS_NAME, "header")

            data['solution']['drag_and_drop'][instructions][header_answer.text].append(btn.text)

        with open("Solutions/data.json", "w") as jsonFile:
            json.dump(data, jsonFile)

    def next_question(self)-> None:
        btn_next = self.browser.find_element(By.XPATH, "//div[@class='nextButtonDiv']")

        # if self.check_exists_by_xpath("//button[@id='btn_question_suivante']"):
        #     btn_next = self.browser.find_element(By.ID, 'btn_question_suivante')
        # elif self.check_exists_by_xpath("//button[@class='nextButton']"):
        #     btn_next = self.browser.find_element(By.XPATH, "//button[@class='nextButton']")

        # if btn_next is None:
        #     sys.exit("Boutton suivant non trouvé")

        btn_next.click()

        sleep(3)

    def intensive_training(self)-> None:
        if self.check_exists_by_xpath("//div[@class='intensiveTrainingHeader']"):
            sleep(2)

            button = self.browser.find_element(By.XPATH, "//button[@class='understoodButton']")
            button.click()

            sleep(2)

            submit_button = self.browser.find_elements(By.CLASS_NAME, "buttonOk")

            if submit_button:
                submit_button[0].click()

                sleep(1)
                submit_button[1].click()

                sleep(1)
                submit_button[2].click()

                sleep(2)

                if self.check_exists_by_xpath("//button[@class='exitButton secondaryButton']"):
                    button = self.browser.find_element(By.XPATH, "//button[@class='exitButton secondaryButton']")
                    button.click()
                else:
                    button = self.browser.find_element(By.XPATH, "//button[@class='exitButton primaryButton']")
                    button.click()
    
    def end_module(self):
        if self.check_exists_by_xpath("//button[@id='btn_apprentissage_autres_niveaux']"):
            btn_next_module = self.browser.find_element(By.XPATH, "//button[@id='btn_apprentissage_autres_niveaux']")

            btn_next_module.click()

            sleep(10)

            self.find_module()
    