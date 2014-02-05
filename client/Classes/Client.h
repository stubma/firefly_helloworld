#ifndef __Client__
#define __Client__

#include "Packet.h"

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
    
    // buffer
    CCByteBuffer m_sendBuf;
    
    // receive buffer
    CCByteBuffer m_recvBuf;
    
    // packet array received
    CCArray m_packets;
    
protected:
    Client();
    
    // ensure socket are all there
    void checkSocket();
	
	// encode
	char* encode(const char* plain, int plainLen, EncryptAlgorithm alg, int* outEncLen);
	
	// decode
	char* decode(const char* enc, int encLen, EncryptAlgorithm alg, int* outPlainLen);
    
public:
    virtual ~Client();
    static Client* sharedClient();
    static void dispose();
    
	void send(int socketTag, CCJSONObject* body, Command cmd, EncryptAlgorithm encAlg = NONE);
    const CCArray& addData(CCByteBuffer& buf);
    
    CCTCPSocketHub* getHub() { return m_hub; }
};

#endif /* defined(__Client__) */
