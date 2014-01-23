#include "Packet.h"

Packet::Packet() :
m_body(NULL) {
    memset(&m_header, 0, sizeof(Header));
}

Packet::~Packet() {
    CC_SAFE_FREE(m_body);
}

Packet* Packet::create() {
    Packet* p = new Packet();
    return (Packet*)p->autorelease();
}

void Packet::allocateBody(size_t len) {
    m_body = (char*)calloc(len, sizeof(char));
}