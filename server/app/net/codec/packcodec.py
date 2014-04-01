#coding:utf8

# encrypt algorithm definition, extend it as you need
ENC_ALG_NONE = 0
ENC_ALG_NOT = 1

class PackCodec(object):
    '''
    codec of packet, you should extend it to add custom encryption
    '''

    def decode(self, data, encryptAlgorithm):
        '''
        decode data based on algorithm
        @param data: encoded data string
        @param encryptAlgorithm: algorithm id
        @return: decoded content, string
        '''
        plain = data
        if encryptAlgorithm == ENC_ALG_NOT:
            plain = ''.join([chr(~ord(b) & 0xff) for b in data])

        return plain

    def encode(self, data, encryptAlgorithm):
        '''
        encode data based on algorithm, return a string encoded
        @param data: original data string
        @param encryptAlgorithm: algorithm id
        @return: encoded content, string
        '''
        enc = data
        if encryptAlgorithm == ENC_ALG_NOT:
            enc = ''.join([chr(~ord(b) & 0xff) for b in data])

        return enc

    def selectAlgorithm(self, command, response):
        # for demo purpose, use not for all command
        return ENC_ALG_NONE

    def verifyAlgorithm(self, command, encryptAlgorithm):
        '''
        check whether given encrypt algorithm is valid for a command
        @param command: command id
        @param encryptAlgorithm: algorithm id
        @return: True if algorithm is acceptable, False if not
        '''
        return True
