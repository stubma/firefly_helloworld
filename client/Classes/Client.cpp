#include "Client.h"

Client* Client::s_instance = NULL;

Client::Client() {
    m_hub = CCTCPSocketHub::create();
    CC_SAFE_RETAIN(m_hub);
    m_buf = CCByteBuffer::create();
    CC_SAFE_RETAIN(m_buf);
}

Client::~Client() {
    CC_SAFE_RELEASE(m_buf);
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
    m_buf->clear();
    
    // magic
    m_buf->write<char>('H');
    m_buf->write<char>('E');
    m_buf->write<char>('L');
    m_buf->write<char>('O');
    
    // protocol version
    m_buf->write<char>(0);
    
    // server version
    m_buf->write<int>(htobe32(0));
    
    // length
    string bodyStr = body->toString();
    m_buf->write<int>(htobe32(bodyStr.length() + 4));
    
    // command id
    m_buf->write<int>(htobe32(cmd));
    
    // body
    m_buf->write((const uint8*)bodyStr.c_str(), bodyStr.length());
    
    // send
    CCTCPSocket* s = m_hub->getSocket(socketTag);
    s->sendData((void*)m_buf->getBuffer(), m_buf->available());
    s->flush();
}