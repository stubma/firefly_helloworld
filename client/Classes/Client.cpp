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

void Client::send(int socketTag, CCJSONObject* body, Command cmd) {
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
	
    // length
    string bodyStr = body->toString();
    m_sendBuf.write<int>(htobe32(bodyStr.length()));
    
    // body
    m_sendBuf.write((const uint8*)bodyStr.c_str(), bodyStr.length());
    
    // send
    CCTCPSocket* s = m_hub->getSocket(socketTag);
    if(s) {
        s->sendData((void*)m_sendBuf.getBuffer(), m_sendBuf.available());
        s->flush();
    }
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
        h.length = betoh32(m_recvBuf.read<int>());
        
        if(m_recvBuf.available() >= h.length) {
            p->allocateBody(h.length - 3); // one more 0 bytes make it a c string
            m_recvBuf.read((uint8*)p->getBody(), h.length);
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