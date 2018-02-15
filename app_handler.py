from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
from selenium.common.exceptions import *
import os
import json


class AppHandlerException(Exception):

    def __init__(self, err_type='', message='', err_id='', err_img=''):
        self.err_type = err_type
        self.message = message
        self.err_id = err_id
        self.err_img = err_img


class CheckTabException(Exception):

    def __init__(self, err_type='', message='', err_id='', err_img=''):
        self.err_type = err_type
        self.message = message
        self.err_id = err_id
        self.err_img = err_img


class AppHandler(object):

    def __init__(self, app_url, wait_for, screen_dump_dir):
        self.browser_session = None
        self.browser_session_waiter = None
        self.is_tab_menu = False
        self.app_url = app_url
        self.wait_for = wait_for
        self.screen_dump_file = os.path.join(screen_dump_dir, 'qvw_dump.png')

    def open_app(self):
        try:
            chrome_driver = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'chromedriver.exe')
            self.browser_session = webdriver.Chrome(chrome_driver)
            self.browser_session.get(self.app_url)
            self.browser_session_waiter = WebDriverWait(self.browser_session, self.wait_for)
        except (WebDriverException, TimeoutException, UnexpectedAlertPresentException) as e:
            err_img = self.take_screenshot()
            err_msg = self.get_msg("ERROR", '110') + ' Exception: ' + str(e)
            raise AppHandlerException('ERROR', err_msg, '110', err_img)
        self.accept_any_alert()
        return self.browser_session

    def close_app(self):
        self.browser_session.quit()

    def get_tabs(self):
        try:
            tabs = self.get_tablist()
            self.is_tab_menu = True
        except:
            tabs = self.get_tabrow()
        return tabs, self.is_tab_menu

    def using_menu(self):
        return self.is_tab_menu

    def get_tabmenu(self):
        tab_area_waiter = WebDriverWait(self.browser_session, 600)
        try:
            tab_area = tab_area_waiter.until(ec.presence_of_element_located((By.ID, "Tabrow")))
            tab_area_waiter.until(ec.presence_of_element_located((By.CLASS_NAME, "qvtr-more")))
            tab_menu = tab_area.find_elements_by_class_name("qvtr-expand")
            return tab_menu
        except NoSuchElementException:
            raise AppHandlerException

    def get_tablist(self):
        try:
            tab_menu = self.get_tabmenu()
            items = []
            if len(tab_menu[0].text) <= 1:
                tab_menu[0].click()
                sleep(0.2)
            default_items = tab_menu[0].find_elements_by_tag_name("li")
            for i in default_items:
                if i.text != '':
                    items.append(i)
            return items
        except (NoSuchElementException, WebDriverException):
            raise AppHandlerException

    def get_tabrow(self):
        sleep(2)
        tab_row_waiter = WebDriverWait(self.browser_session, 600)
        while True:
            try:
                tab_row = tab_row_waiter.until(ec.presence_of_element_located((By.CLASS_NAME, "qvtr-tabs")))
                tab_row_waiter.until(ec.presence_of_element_located((By.TAG_NAME, "li")))
                all_tabs = tab_row.find_elements_by_tag_name("span")
                return all_tabs
            except StaleElementReferenceException:
                continue
            except (NoSuchElementException, TimeoutException, TypeError, WebDriverException, ConnectionRefusedError,
                    TimeoutError, UnexpectedAlertPresentException) as e:
                err_img = self.take_screenshot()
                err_msg = self.get_msg("ERROR", '116') + ' Exception: ' + str(e)
                raise AppHandlerException('ERROR', err_msg, '116', err_img)

    def accept_any_alert(self):
        sleep(2)
        try:
            alert_waiter = WebDriverWait(self.browser_session, 3)
            alert_waiter.until(ec.alert_is_present())
            alert = self.browser_session.switch_to.alert
            alert.accept()
        except TimeoutException:
            pass

    @staticmethod
    def get_tab_pos(tab):
        try:
            return tab.location
        except StaleElementReferenceException:
            return {'x':1, 'y':1}

    def scroll_tabrow(self, direction, steps):
        try:
            scroll_button_waiter = WebDriverWait(self.browser_session, 3)
            scroll_button_class = "qvtr-scroll-" + direction
            scroll_button = scroll_button_waiter.until(ec.presence_of_element_located((By.CLASS_NAME,
                                                                                       scroll_button_class)))
            for i in range(0, steps):
                scroll_button.click()
        except WebDriverException:
            pass

    def get_tab(self, tab_text):
        tab_waiter = WebDriverWait(self.browser_session, 10)
        try:
            tab = tab_waiter.until(ec.presence_of_element_located((By.LINK_TEXT, tab_text)))
        except WebDriverException as e:
            tab = tab_waiter.until(ec.presence_of_element_located((By.PARTIAL_LINK_TEXT, tab_text)))
        return tab

    def click_tab(self, tab_name):
        if self.using_menu():
            tab_list = self.get_tablist()
            for item in tab_list:
                if item.text == tab_name and len(item.text) > 0:
                    item.click()
                    break
        else:
            tab = self.get_tab(tab_name)
            if self.get_tab_pos(tab)["x"] <= 0:
                self.scroll_tabrow('left', 4)
            tab.click()
        try:
            sleep(2)
            while not self.check_tab_selected():
                sleep(1)
        except (NoSuchElementException, TimeoutException, TypeError, StaleElementReferenceException,
                ConnectionRefusedError, TimeoutError, UnexpectedAlertPresentException, CheckTabException) as e:
            err_img = self.take_screenshot()
            err_msg = self.get_msg("ERROR", '119') + tab_name + ' Exception: ' + str(e)
            raise AppHandlerException('ERROR', err_msg, '119', err_img)

    def check_tab_selected(self):
        try:
            tab_waiter = WebDriverWait(self.browser_session, 300)
            el_class = tab_waiter.until(ec.visibility_of_element_located((By.CLASS_NAME, "selectedtab")))
            el_class.get_attribute('id')
            self.browser_session_waiter.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "QvContent")), 600)
            return el_class
        except TimeoutException:
            raise CheckTabException

    def get_num_of_sheet_objects(self):
        try:
            main_container = self.browser_session_waiter.until(ec.presence_of_element_located((By.ID, "MainContainer"))
                                                               ,600)
            self.browser_session_waiter.until(ec.presence_of_all_elements_located((By.CLASS_NAME, "QvContent")), 600)
            all_divs = main_container.find_elements_by_tag_name("div")
            return all_divs.__len__()
        except (NoSuchElementException, TimeoutException, TypeError, StaleElementReferenceException, WebDriverException,
                ConnectionRefusedError, TimeoutError, UnexpectedAlertPresentException) as e:
            err_img = self.take_screenshot()
            err_msg = self.get_msg("ERROR", '118') + ' Exception: ' + str(e)
            raise AppHandlerException('ERROR', err_msg, '118', err_img)

    def take_screenshot(self):
        err_img = self.screen_dump_file
        try:
            self.browser_session.save_screenshot(err_img)
        except UnexpectedAlertPresentException:
            err_img = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'UnexpectedAlert.png')
            alert = self.browser_session.switch_to.alert
            alert.accept()
            err_msg = self.get_msg("ERROR", '120')
            raise AppHandlerException('ERROR', err_msg, '120', err_img)
        return err_img

    @staticmethod
    def get_msg(msg_type, msg_id):
        msg_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'messages.json')
        with open(msg_file) as msg_data:
            j_obj = json.load(msg_data)
            return j_obj[msg_type][msg_id]


class wait_for_page_load(object):

    def __init__(self, browser):
        self.browser = browser

    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')

    def page_has_loaded(self):
        new_page = self.browser.find_element_by_tag_name('html')
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        wait_for_page_load(self.page_has_loaded)