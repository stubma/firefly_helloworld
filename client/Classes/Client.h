#ifndef __Client__
#define __Client__

class Client : public CCObject {
public:
    typedef enum {
        TEST = 1,
		TEST_PUSH = 2,
		QUERY_BIND = 100,
        LOGIN = 101
    } Command;
    
    typedef enum {
        E_OK,
        E_UNKNOWN,
        E_WRONG_PASSWORD,
        E_BLOCKED,
        E_DB_ERROR
    } ErrCode;
    
    typedef enum {
        NONE,
        NOT
    } EncryptAlgorithm;
    
private:
    // singleton
    static Client* s_instance;
    
    // hub
    CCTCPSocketHub* m_hub;
    
protected:
    Client();
    
    // ensure socket are all there
    void checkSocket();
    
public:
    virtual ~Client();
    static Client* sharedClient();
    static void dispose();
    
	void send(int socketTag, CCJSONObject* body, Command cmd, EncryptAlgorithm encAlg = NONE);
    
    CCTCPSocketHub* getHub() { return m_hub; }
};

#endif /* defined(__Client__) */
