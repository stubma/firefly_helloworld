#include "Client.h"

Client* Client::s_instance = NULL;

Client::Client() {
    m_hub = CCTCPSocketHub::create();
    CC_SAFE_RETAIN(m_hub);
}

Client::~Client() {
    CC_SAFE_RELEASE(m_hub);
    s_instance = NULL;
}

Client* Client::sharedClient() {
    if(!s_instance) {
        s_instance = new Client();
    }
    return s_instance;
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
    m_sendBuf.write<char>(0);
    
    // server version
    m_sendBuf.write<int>(htobe32(0));
    
    // length
    string bodyStr = body->toString();
    m_sendBuf.write<int>(htobe32(bodyStr.length() + 4));
    
    // command id
    m_sendBuf.write<int>(htobe32(cmd));
    
    // body
    m_sendBuf.write((const uint8*)bodyStr.c_str(), bodyStr.length());
    
    // send
    CCTCPSocket* s = m_hub->getSocket(socketTag);
    s->sendData((void*)m_sendBuf.getBuffer(), m_sendBuf.available());
    s->flush();
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
        h.protocolVersion = m_recvBuf.read<char>();
        h.serverVersion = betoh32(m_recvBuf.read<int>());
        h.length = betoh32(m_recvBuf.read<int>());
        h.command = betoh32(m_recvBuf.read<int>());
        
        if(m_recvBuf.available() >= h.length - 4) {
            p->allocateBody(h.length - 3); // one more 0 bytes make it a c string
            m_recvBuf.read((uint8*)p->getBody(), h.length - 4);
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