# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

import struct
import sys
import sysconfig

import attr
from typing import NoReturn, Text, Dict, Union

from gmtrade.__version__ import __version__
from gmtrade.pb.account_pb2 import AccountStatus, ExecRpt, Order


@attr.s(frozen=True, slots=True)
class Account(object):
    account_id = attr.ib(type=str)
    account_alias = attr.ib(type=str)


class DefaultFileModule(object):
    def on_execution_report(self, rpt):
        # type: (ExecRpt) -> NoReturn
        print('请初始化on_execution_report方法')

    def on_order_status(self, order):
        # type: (Order) -> NoReturn
        print('请初始化on_order_status方法')

    def on_trade_data_connected(self):
        print('请初始化on_trade_data_connected方法')

    def on_trade_data_disconnected(self):
        print('请初始化on_trade_data_disconnected方法')

    def on_account_status(self, account_status):
        # type: (AccountStatus) -> NoReturn
        print('请初始化on_account_status方法')


class Context(object):
    """
    策略运行的上下文类. 这在整个进程中要保证是单一实例
    注意: 一个运行的python进程只能运行一个策略.
    警告: 客户写的策略代码不要直接使用这个类来实例化, 而是使用 sdk 实例化好的 context 实例
    """
    inside_file_module = DefaultFileModule()

    on_error_fun = None
    on_shutdown_fun = None

    on_execution_report_fun = None
    on_order_status_fun = None
    on_account_status_fun = None

    on_trade_data_connected_fun = None
    on_trade_data_disconnected_fun = None

    token = None  # type: Text
    sdk_lang = "python{}.{}".format(sys.version_info.major, sys.version_info.minor)  # type: Text
    sdk_version = __version__  # type: Text
    sdk_arch = str(struct.calcsize("P") * 8)  # type: Text
    sdk_os = sysconfig.get_platform()  # type: Text

    # 已登陆的所有帐号, 用accountid或account_alias做为key值
    logined_accounts = {}  # type: Dict[Text, Account]
    # 默认帐号
    default_account = None  # type: Union[Account, None]


# 提供给API的唯一上下文实例
ctx = Context()
