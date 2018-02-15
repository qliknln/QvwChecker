from time import time, sleep
import json
import os
import argparse
from app_handler import AppHandler, AppHandlerException
from logger import Logger


class QvwAjaxExercizer(object):
    app_meta_data = {}
    app_handler = None

    def __init__(self):
        config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
        with open(config_file) as json_data:
            d = json.load(json_data)
            self.test_log = Logger(d['LogFile'], d['email'], d['SystemName'])
            self.page_url = app_meta_data['pageUrl']
            self.page_title = app_meta_data['title']
            self.app_handler = AppHandler(self.page_url, app_meta_data['elementWait'], d['ScreenDump'])
            try:
                self.app_handler.open_app()
            except AppHandlerException as ex:
                self.test_log.write_to_log(ex.err_type, 'N/A', ex.message, 0, ex.err_id, self.page_title,
                                           self.page_url, ex.err_img)

    def test_tabs_in_app(self):
        try:
            tab_start = time()
            if self.app_meta_data["hasTabs"]:
                current_tab_name = ''
                tab_name_list = []
                tabs = self.app_handler.get_tabs()
                for t in tabs[0]:
                    tab_name_list.append(str(t.text))
                for tab_name in tab_name_list:
                    self.app_handler.click_tab(tab_name)
                    current_tab_name = tab_name
                if self.app_meta_data["hasSheetObjects"]:
                        if self.app_handler.get_num_of_sheet_objects() > 0:
                            tab_end = time()
                            self.test_log.write_to_log('SUCCESS', current_tab_name, self.app_handler.get_msg("SUCCESS", '0'),
                                                       str(tab_end - tab_start), 0, self.page_title, self.page_url)
                        else:
                            tab_end = time()
                            err_msg = self.app_handler.get_msg("ERROR", '118')
                            err_img = self.app_handler.take_screenshot()
                            self.test_log.write_to_log('ERROR', current_tab_name, err_msg, str(tab_end - tab_start), '118',
                                                       self.page_title, self.page_url, err_img)
                            return
                else:
                    tab_end = time()
                    self.test_log.write_to_log('SUCCESS', current_tab_name, self.app_handler.get_msg("SUCCESS", '0'),
                                               str(tab_end - tab_start), '0', self.page_title, self.page_url)
            else:
                tab = type('', (), {'text': ''})
                tab.text = 'No tabs in app'
                if self.app_meta_data["hasSheetObjects"]:
                    try:
                        if self.app_handler.get_num_of_sheet_objects() > 0:
                            tab_end = time()
                            self.test_log.write_to_log('SUCCESS', tab.text, self.app_handler.get_msg("SUCCESS", '0'),
                                                       str(tab_end - tab_start), 0, self.page_title, self.page_url)
                        else:
                            tab_end = time()
                            err_img = self.app_handler.take_screenshot()
                            err_msg = self.app_handler.get_msg("ERROR", '118')
                            self.test_log.write_to_log('ERROR', tab.text, err_msg, str(tab_end - tab_start), '118',
                                                       self.page_title, self.page_url, err_img)
                            return
                    except AppHandlerException as ex:
                        self.test_log.write_to_log(ex.err_type, 'N/A', ex.message, 0, ex.err_id, self.page_title,
                                                   self.page_url, ex.err_img)
                    return
        except AppHandlerException as ex:
            self.test_log.write_to_log(ex.err_type, 'N/A', ex.message, 0, ex.err_id, self.page_title,
                                       self.page_url, ex.err_img)

    def tear_down(self):
        self.app_handler.close_app()


if __name__ == '__main__':
    app_full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apps')
    parser = argparse.ArgumentParser()
    parser.add_argument('--groups', help='Application groups to run. Use --groups All or skip arguments to run all '
                                         'groups or --groups "grp1, grp2" to run a subset')
    grp_arg = parser.parse_args()

    if type(grp_arg.groups) is str:
        grp_list = str.split(grp_arg.groups, ',')
    else:
        grp_list = ['ALL']
    for app_file in os.listdir(app_full_path):
        app_file_path = os.path.join(app_full_path, app_file)
        with open(app_file_path) as current_app:
            app_meta_data = json.load(current_app)
            QvwAjaxExercizer.app_meta_data = app_meta_data
            if str.upper(grp_list[0]) == 'ALL':
                print(app_file)
                qae = QvwAjaxExercizer()
                qae.test_tabs_in_app()
                qae.tear_down()
            else:
                for grp in grp_list:
                    if str.upper(grp) == str.upper(app_meta_data['group']):
                        print(app_file)
                        qae = QvwAjaxExercizer()
                        qae.test_tabs_in_app()
                        qae.tear_down()

