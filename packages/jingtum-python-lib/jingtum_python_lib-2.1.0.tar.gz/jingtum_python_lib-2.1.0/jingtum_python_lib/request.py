# coding=utf-8
"""
 * Created with PyCharm.
 * User: 彭诗杰
 * Date: 2018/5/7
 * Time: 16:44
 * Description: request类
"""
import json

from eventemitter import EventEmitter

from jingtum_python_lib.utils import *

class Request:
    def __init__(self, remote, command, filter):
        self.remote = remote
        self.command = command
        self.filter = filter

        self.message = {}
        self.emitter = EventEmitter()

    def submit(self):
        for key in self.message:
            if isinstance(self.message[key], Exception):
                callback = self.message[key]
                return callback

        return self.remote.submit(self.command, self.message)

    def select_ledger(self, ledger):
        """
        该方法用于选定ledger账本
        :param ledger:  账本的Index或者hash
        :return: Request对象
        """
        if ledger is None:
            self.message['ledger_index'] = 'validated'
            return self

        if isinstance(ledger, str) and ledger in LEDGER_STATES:
            self.message['ledger_index'] = ledger
        elif is_number(ledger):
            self.message['ledger_index'] = ledger
        elif re.search('^[A-F0-9]+$', ledger):
            self.message['ledger_index'] = ledger
        else:
            self.message['ledger_index'] = 'validated'
        return self
