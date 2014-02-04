#include "Client.h"

Client* Client::s_instance = NULL;

Client::Client() {
    m_hub = CCTCPSocketHub::create();
    CC_SAFE_RETAIN(m_hub);
    
    checkSocket();
}

Client::~Client() {
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
		m_hub->createSocket("192.168.1.104", 11009, 1, kCCSocketDefaultTimeout, true);
//        m_hub->createSocket("172.16.96.60", 11009, 1, kCCSocketDefaultTimeout, true);
    }
}

void Client::dispose() {
    if(s_instance) {
        CC_SAFE_RELEASE(s_instance);
    }
}

void Client::send(int socketTag, CCJSONObject* body, Command cmd, EncryptAlgorithm encAlg) {
    // clear
    m_sendBuf.clear();
    
    // magic
    m_sendBuf.write<char>('H');
    m_sendBuf.write<char>('E');
    m_sendBuf.write<char>('L');
    m_sendBuf.write<char>('O');
    
    // protocol version
    m_sendBuf.write<int>(0);
    
    // server version
    m_sendBuf.write<int>(htobe32(0));
    
	// command id
    m_sendBuf.write<int>(htobe32(cmd));
	
	// no encrypt
	m_sendBuf.write<int>(htobe32(encAlg));
    
    // body
	string bodyStr = body->toString();
	char* plain = (char*)bodyStr.c_str();
	int bodyLen = bodyStr.length();
	int encLen;
	char* enc = encode(plain, bodyLen, encAlg, &encLen);
	m_sendBuf.write<int>(htobe32(encLen));
    m_sendBuf.write((const uint8*)enc, encLen);
	if(enc != plain)
		free(enc);
    
    // send
    CCTCPSocket* s = m_hub->getSocket(socketTag);
    if(s) {
        s->sendData((void*)m_sendBuf.getBuffer(), m_sendBuf.available());
        s->flush();
    }
}

char* Client::encode(const char* plain, int plainLen, EncryptAlgorithm alg, int* outEncLen) {
	char* enc = (char*)plain;
	int encLen = plainLen;
	switch(alg) {
		case NOT:
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

char* Client::decode(const char* enc, int encLen, EncryptAlgorithm alg, int* outPlainLen) {
	char* plain = (char*)enc;
	int plainLen = encLen;
	switch(alg) {
		case NOT:
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

const CCArray& Client::addData(CCByteBuffer& buf) {
    // append data to recv buffer
    m_recvBuf.write(buf.getBuffer(), buf.available());

    // clear old array
    m_packets.removeAllObjects();
    
    // check if has any completed packet
    while(m_recvBuf.available() >= HEADER_LENGTH) {
        Packet* p = Packet::create();
        Packet::Header& h = p->getHeader();
        h.magic[0] = m_recvBuf.read<char>();
        h.magic[1] = m_recvBuf.read<char>();
        h.magic[2] = m_recvBuf.read<char>();
        h.magic[3] = m_recvBuf.read<char>();
        h.protocolVersion = betoh32(m_recvBuf.read<int>());
        h.serverVersion = betoh32(m_recvBuf.read<int>());
		h.command = betoh32(m_recvBuf.read<int>());
		h.encryptAlgorithm = betoh32(m_recvBuf.read<int>());
        h.length = betoh32(m_recvBuf.read<int>());
        
        if(m_recvBuf.available() >= h.length) {
			// read body and try to decode
			char* body = (char*)malloc(h.length * sizeof(char));
			m_recvBuf.read((uint8*)body, h.length);
			int plainLen;
			char* plain = decode(body, h.length, (EncryptAlgorithm)h.encryptAlgorithm, &plainLen);
			if(plain != body)
				free(body);
			
			// copy to body
            p->allocateBody(plainLen + 1); // one more 0 bytes make it a c string
			memcpy(p->getBody(), plain, plainLen);
			h.length = plainLen;
			free(plain);

			// push packet to queue
            m_packets.addObject(p);
        } else {
            m_recvBuf.revoke(HEADER_LENGTH);
            break;
        }
    }
    
    // compact
    m_recvBuf.compact();
    
    return m_packets;
}