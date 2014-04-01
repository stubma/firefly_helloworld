#ifndef __LoginScene__
#define __LoginScene__

/**
 * Login scene
 */
class Login : public CCLayer {
private:
    CCEditBox* m_usernameEdit;
    CCEditBox* m_passwordEdit;
    
private:
    void onLoginClicked(CCObject* sender);
	void queryBind();
    
    // notification
    void onTCPSocketConnected(CCTCPSocket* s);
    void onTCPSocketDisonnected(CCTCPSocket* s);
    void onPacketReceived(CCPacket* p);
    
public:
	virtual ~Login();
    
    // there's no 'id' in cpp, so we recommend returning the class instance pointer
    static CCScene* scene();
	
    // Here's a difference. Method 'init' in cocos2d-x returns bool, instead of returning 'id' in cocos2d-iphone
    virtual bool init();
    virtual void onExit();
    
    // implement the "static node()" method manually
    CREATE_FUNC(Login);
};

#endif /* defined(__LoginScene__) */
