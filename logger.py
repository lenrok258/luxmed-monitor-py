from datetime import datetime


class Logger:
    __SCREENSHOTS_DIR = 'screenshots'

    def __init__(self, webdriver=None):
        self.webdriver = webdriver

    def info(self, message, *args):
        self.__print('INFO', message, *args)

    def error(self, message, *args):
        self.__print('ERROR', message, *args)

    def warn(self, message, *args):
        self.__print('WARN', message, *args)

    def screenshot(self, screen_name):
        filepath = "{}/{}.png".format(self.__SCREENSHOTS_DIR, screen_name)
        self.webdriver.save_screenshot(filepath)

    def __print(self, level, message, *args):
        now_string = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message_formatted = message.format(*args)
        print('{0} [{1}]: {2}'.format(now_string,
                                      level,
                                      message_formatted))
