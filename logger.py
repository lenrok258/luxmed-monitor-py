from datetime import datetime


class Logger:
    def info(self, message, *args):
        self.__print('INFO', message, *args)

    def error(self, message, *args):
        self.__print('ERROR', message, *args)

    def warn(self, message, *args):
        self.__print('WARN', message, *args)

    def __print(self, level, message, *args):
        nowString = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        messageFormatted = message.format(*args)
        print '{0} [{1}]: {2}'.format(nowString,
                                      level,
                                      messageFormatted)
