#ifndef __Client__
#define __Client__

class Client : public CCObject {
public:
    typedef enum {
        LOGIN = 101
    } Command;
    
private:
    // singleton
    static Client* s_instance;
    
    // hub
    CCTCPSocketHub* m_hub;
    
    // buffer
    CCByteBuffer* m_buf;
    
protected:
    Client();
    
public:
    virtual ~Client();
    static Client* sharedClient();
    static void dispose();
    
    void send(int socketTag, CCJSONObject* body, Command cmd);
    
    CCTCPSocketHub* getHub() { return m_hub; }
};

#endif /* defined(__Client__) */
