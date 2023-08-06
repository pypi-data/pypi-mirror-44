# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from marshmallow import fields
from polyaxon_deploy.schemas.base import BaseConfig, BaseSchema


class IntervalsSchema(BaseSchema):
    experimentsScheduler = fields.Int(default=None)
    experimentsSync = fields.Int(default=None)
    clustersUpdateSystemInfo = fields.Int(default=None)
    clustersUpdateSystemNodes = fields.Int(default=None)
    pipelinesScheduler = fields.Int(default=None)
    operationsDefaultRetryDelay = fields.Int(default=None)
    operationsMaxRetryDelay = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return IntervalsConfig


class IntervalsConfig(BaseConfig):
    SCHEMA = IntervalsSchema
    REDUCED_ATTRIBUTES = [
        'experimentsScheduler',
        'experimentsSync',
        'clustersUpdateSystemInfo',
        'clustersUpdateSystemNodes',
        'pipelinesScheduler',
        'operationsDefaultRetryDelay',
        'operationsMaxRetryDelay',
    ]

    def __init__(self,  # noqa
                 experimentsScheduler=None,
                 experimentsSync=None,
                 clustersUpdateSystemInfo=None,
                 clustersUpdateSystemNodes=None,
                 pipelinesScheduler=None,
                 operationsDefaultRetryDelay=None,
                 operationsMaxRetryDelay=None):
        self.experimentsScheduler = experimentsScheduler
        self.experimentsSync = experimentsSync
        self.clustersUpdateSystemInfo = clustersUpdateSystemInfo
        self.clustersUpdateSystemNodes = clustersUpdateSystemNodes
        self.pipelinesScheduler = pipelinesScheduler
        self.operationsDefaultRetryDelay = operationsDefaultRetryDelay
        self.operationsMaxRetryDelay = operationsMaxRetryDelay


class CleaningIntervalsSchema(BaseSchema):
    archived = fields.Int(default=None)

    @staticmethod
    def schema_config():
        return CleaningIntervalsConfig


class CleaningIntervalsConfig(BaseConfig):
    SCHEMA = CleaningIntervalsSchema
    REDUCED_ATTRIBUTES = ['archived']

    def __init__(self, archived=None):
        self.archived = archived


class TTLSchema(BaseSchema):
    token = fields.Int(allow_none=True)
    ephemeralToken = fields.Int(allow_none=True)
    heartbeat = fields.Int(allow_none=True)
    watchStatuses = fields.Int(allow_none=True)

    @staticmethod
    def schema_config():
        return TTLConfig


class TTLConfig(BaseConfig):
    SCHEMA = TTLSchema
    REDUCED_ATTRIBUTES = ['token', 'ephemeralToken', 'heartbeat', 'watchStatuses']

    def __init__(self,  # noqa
                 token=None,
                 ephemeralToken=None,
                 heartbeat=None,
                 watchStatuses=None):
        self.token = token
        self.ephemeralToken = ephemeralToken
        self.heartbeat = heartbeat
        self.watchStatuses = watchStatuses
