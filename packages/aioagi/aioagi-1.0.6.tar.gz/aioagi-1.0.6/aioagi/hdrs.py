from enum import Enum


class AGIMethod(str, Enum):
    ANY = '*'
    LOCAL = 'LOCAL'
    SIP = 'SIP'
    DAHDI = 'DAHDI'
    IAX2 = 'IAX2'
    MOTIF = 'MOTIF'
    MISDN = 'MISDN'
    USTM = 'USTM'
    SKINNY = 'SKINNY'
    H323 = 'H323'
    OOH323 = 'OOH323'
    GTALK = 'GTALK'
    JINGLE = 'JINGLE'

    @classmethod
    def all(cls):
        return {
            cls.LOCAL, cls.SIP, cls.DAHDI, cls.IAX2,
            cls.MOTIF, cls.MISDN, cls.USTM, cls.SKINNY,
            cls.H323, cls.OOH323, cls.GTALK, cls.JINGLE,
        }
