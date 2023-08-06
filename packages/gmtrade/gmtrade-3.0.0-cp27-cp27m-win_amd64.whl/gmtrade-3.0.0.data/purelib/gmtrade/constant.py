# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

"""
c-sdk回调的类型
"""
CALLBACK_TYPE_CASH = 'core.api.Cash'
CALLBACK_TYPE_POSITION = 'core.api.Position'
CALLBACK_TYPE_ORDER = 'core.api.Order'
CALLBACK_TYPE_EXECRPT = 'core.api.ExecRpt'
CALLBACK_TYPE_INDICATOR = 'core.api.Indicator'
CALLBACK_TYPE_ERROR = 'error'
CALLBACK_TYPE_TIMER = 'timer'
CALLBACK_TYPE_STOP = 'stop'
CALLBACK_TYPE_TRADE_CONNECTED = 'td-connected'
CALLBACK_TYPE_TRADE_DISCONNECTED = 'td-disconnected'
CALLBACK_TYPE_ACCOUNTSTATUS = 'core.api.AccountStatus'

TRADE_CONNECTED = 1
DATA_CONNECTED = 2

CSDK_OPERATE_SUCCESS = 0  # c-sdk 操作成功
