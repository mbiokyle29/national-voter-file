# file national-voter-file/src/main/python/settings.py
"""
General settings and constants for prepare scripts
"""

import logging

LOG_SETTINGS = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        }
    },
    'formatters': {
        'detailed': {
            'format': '[%(levelname)s]: %(module)s.%(funcName)s:  %(message)s',
        },
    },
    'loggers': {
        '': {
            'level': logging.INFO,
            'handlers': ['console']
        }
    }
}

NY_INPUT_FIELD_NAMES = ['LASTNAME',
                       'FIRSTNAME',
                       'MIDDLENAME',
                       'NAMESUFFIX',
                       'RADDNUMBER',
                       'RHALFCODE',
                       'RAPARTMENT',
                       'RPREDIRECTION',
                       'RSTREETNAME',
                       'RPOSTDIRECTION',
                       'RCITY',
                       'RZIP5',
                       'RZIP4',
                       'MAILADD1',
                       'MAILADD2',
                       'MAILADD3',
                       'MAILADD4',
                       'DOB',
                       'GENDER',
                       'ENROLLMENT',
                       'OTHERPARTY',
                       'COUNTYCODE',
                       'ED',
                       'LD',
                       'TOWNCITY',
                       'WARD',
                       'CD',
                       'SD',
                       'AD',
                       'LASTVOTEDDATE',
                       'PREVYEARVOTED',
                       'PREVCOUNTY',
                       'PREVADDRESS',
                       'PREVNAME',
                       'COUNTYVRNUMBER',
                       'REGDATE',
                       'VRSOURCE',
                       'IDREQUIRED',
                       'IDMET',
                       'STATUS',
                       'REASONCODE',
                       'INACT_DATE',
                       'PURGE_DATE',
                       'SBOEID',
                       'VoterHistory']
