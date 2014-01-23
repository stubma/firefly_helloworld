#ifndef __Packet__
#define __Packet__

#define HEADER_LENGTH 17

class Packet : public CCObject {
public:
    typedef struct {
        char magic[4];
        char protocolVersion;
        int serverVersion;
        int length;
        int command;
    } Header;
    
public:
    Packet();
    virtual ~Packet();
    static Packet* create();
    
    // allocate memory for body
    void allocateBody(size_t len);
    
    CC_SYNTHESIZE_PASS_BY_REF_NC(Header, m_header, Header);
    CC_SYNTHESIZE(char*, m_body, Body);
};

#endif /* defined(__Packet__) */
