#include "Client.h"

Client* Client::s_instance = NULL;

static const char* encode(const char* plain, size_t plainLen, size_t* outEncLen, int alg) {
	char* enc = (char*)plain;
	int encLen = plainLen;
	switch(alg) {
		case Client::NOT:
			encLen = plainLen;
			enc = (char*)malloc(plainLen * sizeof(char));
			for(int i = 0; i < plainLen; i++) {
				enc[i] = ~plain[i] & 0xff;
			}
			break;
		default:
			break;
	}
	
	if(outEncLen)
		*outEncLen = encLen;
	
	return enc;
}

static const char* decode(const char* enc, size_t encLen, size_t* outPlainLen, int alg) {
	char* plain = (char*)enc;
	int plainLen = encLen;
	switch(alg) {
		case Client::NOT:
			plainLen = encLen;
			plain = (char*)malloc(encLen * sizeof(char));
			for(int i = 0; i < encLen; i++) {
				plain[i] = ~enc[i] & 0xff;
			}
			break;
		default:
			break;
	}
	
	if(outPlainLen)
		*outPlainLen = plainLen;
	
	return plain;
}

Client::Client() {
    m_hub = CCTCPSocketHub::create(encode, decode);
    CC_SAFE_RETAIN(m_hub);
    
    checkSocket();
}

Client::~Client() {
    m_hub->stopAll();
    CC_SAFE_RELEASE(m_hub);
    s_instance = NULL;
}

Client* Client::sharedClient() {
    if(!s_instance) {
        s_instance = new Client();
    }
    
    // ensure socket
    s_instance->checkSocket();
    
    return s_instance;
}

void Client::checkSocket() {
    if(!m_hub->getSocket(1)) {
//		m_hub->createSocket("192.168.1.106", 11009, 1, kCCSocketDefaultTimeout, true);
        m_hub->createSocket("172.16.96.60", 11009, 1, kCCSocketDefaultTimeout, true);
    }
}

void Client::dispose() {
    if(s_instance) {
        CC_SAFE_RELEASE(s_instance);
    }
}

void Client::send(int socketTag, CCJSONObject* body, Command cmd, EncryptAlgorithm encAlg) {
    // send
    CCTCPSocket* s = m_hub->getSocket(socketTag);
    if(s) {
        s->sendPacket(CCPacket::createStandardPacket("HELO", cmd, body, encAlg));
    }
}