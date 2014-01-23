#ifndef __Client__
#define __Client__

#include "Packet.h"

class Client : public CCObject {
public:
    typedef enum {
        LOGIN = 101
    } Command;
    
    typedef enum {
        E_OK,
        E_UNKNOWN,
        E_WRONG_PASSWORD,
        E_BLOCKED,
        E_DB_ERROR
    } ErrCode;
    
private:
    // singleton
    static Client* s_instance;
    
    // hub
    CCTCPSocketHub* m_hub;
    
    // buffer
    CCByteBuffer m_sendBuf;
    
    // receive buffer
    CCByteBuffer m_recvBuf;
    
    // packet array received
    CCArray m_packets;
    
protected:
    Client();
    
public:
    virtual ~Client();
    static Client* sharedClient();
    static void dispose();
    
    void send(int socketTag, CCJSONObject* body, Command cmd);
    const CCArray& addData(CCByteBuffer& buf);
    
    CCTCPSocketHub* getHub() { return m_hub; }
};

#endif /* defined(__Client__) */
