#coding:utf8

ENC_ALG_NONE = 0
ENC_ALG_NOT = 1

class PackCodec(object):
    '''
    codec of packet
    '''

    def __init__(self):
        pass

    def decode(self, data, encryptAlgorithm):
        plain = data

        if encryptAlgorithm == ENC_ALG_NOT:
            plain = ''.join([chr(~ord(b) & 0xff) for b in data])

        return plain

    def encode(self, data, encryptAlgorithm):
        enc = data

        if encryptAlgorithm == ENC_ALG_NOT:
            enc = ''.join([chr(~ord(b) & 0xff) for b in data])

        return enc

    def selectAlgorithm(self, command, response):
        # for demo purpose, use not for all command
        return ENC_ALG_NOT

    def verifyAlgorithm(self, command, encryptAlgorithm):
        '''
        check whether given encrypt algorithm is valid for a command
        @param command: command id
        @param encryptAlgorithm: algorithm id
        @return: True if algorithm is acceptable, False if not
        '''
        return True
