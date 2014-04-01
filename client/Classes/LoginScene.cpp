#include "LoginScene.h"
#include "Client.h"
#include "SendMsgScene.h"

Login::~Login() {
}

CCScene* Login::scene() {
    // 'scene' is an autorelease object
    CCScene* scene = CCScene::create();
    
    // 'layer' is an autorelease object
    Login* layer = Login::create();
	
    // add layer as a child to scene
    scene->addChild(layer);
	
    // return the scene
    return scene;
}

bool Login::init() {
    // super init first
    if (!CCLayer::init()) {
        return false;
    }
    
    // surface size
    CCSize visibleSize = CCDirector::sharedDirector()->getVisibleSize();
    CCPoint origin = CCDirector::sharedDirector()->getVisibleOrigin();
    
    // login item
    CCLabelTTF* label = CCLabelTTF::create("Login", "Helvetica", 40 / CC_CONTENT_SCALE_FACTOR());
    CCMenuItemLabel* loginItem = CCMenuItemLabel::create(label, this, menu_selector(Login::onLoginClicked));
    loginItem->setPosition(ccp(origin.x + visibleSize.width / 2,
                               origin.y + visibleSize.height * 6 / 10));

    // menu
    CCMenu* menu = CCMenu::create(loginItem, NULL);
    menu->setPosition(CCPointZero);
    addChild(menu);
    
    // user name edit
    CCSprite* frame = CCSprite::create("images/textbox_normal.png");
    CCRect rect = CCRectMake(0,
                             0,
                             frame->getContentSize().width,
                             frame->getContentSize().height);
    CCRect insets = CCRectMake(11 / CC_CONTENT_SCALE_FACTOR(),
                               21 / CC_CONTENT_SCALE_FACTOR(),
                               1 / CC_CONTENT_SCALE_FACTOR(),
                               1 / CC_CONTENT_SCALE_FACTOR());
    CCSize editSize = CCSizeMake(visibleSize.width * 4 / 5, 50 / CC_CONTENT_SCALE_FACTOR());
    {
        CCScale9Sprite* editNormal = CCScale9Sprite::create("images/textbox_normal.png",
                                                            rect,
                                                            insets);
        CCScale9Sprite* editPressed = CCScale9Sprite::create("images/textbox_pressed.png",
                                                             rect,
                                                             insets);
        m_usernameEdit = CCEditBox::create(editSize, editNormal, editPressed);
        m_usernameEdit->setReturnType(kKeyboardReturnTypeDone);
        m_usernameEdit->setFontSize(12);
        m_usernameEdit->setText("");
        m_usernameEdit->setFontColor(ccc3(158, 122, 83));
        m_usernameEdit->setMaxLength(8);
        m_usernameEdit->setPosition(ccp(origin.x + visibleSize.width / 2,
                                        origin.y + visibleSize.height * 8 / 10));
        addChild(m_usernameEdit);
    }
    
    // password edit box
    {
        CCScale9Sprite* editNormal = CCScale9Sprite::create("images/textbox_normal.png",
                                                            rect,
                                                            insets);
        CCScale9Sprite* editPressed = CCScale9Sprite::create("images/textbox_pressed.png",
                                                             rect,
                                                             insets);
        m_passwordEdit = CCEditBox::create(editSize, editNormal, editPressed);
        m_passwordEdit->setReturnType(kKeyboardReturnTypeDone);
        m_passwordEdit->setInputFlag(kEditBoxInputFlagPassword);
        m_passwordEdit->setFontColor(ccc3(158, 122, 83));
        m_passwordEdit->setMaxLength(8);
        m_passwordEdit->setFontSize(8);
        m_passwordEdit->setText("");
        m_passwordEdit->setPosition(ccp(origin.x + visibleSize.width / 2,
                                        origin.y + visibleSize.height * 7 / 10));
        addChild(m_passwordEdit);
    }
    
    // add notification observer
    CCNotificationCenter* nc = CCNotificationCenter::sharedNotificationCenter();
    nc->addObserver(this, callfuncO_selector(Login::onTCPSocketConnected), kCCNotificationTCPSocketConnected, NULL);
    nc->addObserver(this, callfuncO_selector(Login::onTCPSocketDisonnected), kCCNotificationTCPSocketDisconnected, NULL);
    nc->addObserver(this, callfuncO_selector(Login::onPacketReceived), kCCNotificationPacketReceived, NULL);
    
    // ensure socket is created
    Client::sharedClient();
    
    return true;
}

void Login::onExit() {
    CCLayer::onExit();
    
    CCNotificationCenter* nc = CCNotificationCenter::sharedNotificationCenter();
    nc->removeObserver(this, kCCNotificationPacketReceived);
    nc->removeObserver(this, kCCNotificationTCPSocketConnected);
    nc->removeObserver(this, kCCNotificationTCPSocketDisconnected);
}

void Login::onTCPSocketConnected(CCTCPSocket* s) {
    CCLOG("connected: %d", s->getTag());
}

void Login::onTCPSocketDisonnected(CCTCPSocket* s) {
    CCLOG("disconnected: %d", s->getTag());
}

void Login::onPacketReceived(CCPacket* p) {
    switch (p->getHeader().command) {
        case Client::LOGIN:
        {
            CCJSONObject* json = CCJSONObject::create(p->getBody(), p->getBodyLength());
            Client::ErrCode err = (Client::ErrCode)json->optInt("errno");
            if(err != Client::E_OK) {
                string errMsg = json->optString("errmsg");
                errMsg = CCUtils::decodeHtmlEntities(errMsg);
                CCLOG("error message: %s", errMsg.c_str());
                Helper::showToast(errMsg, this);
                
                break;
            } else {
                // to send msg scene
                CCDirector::sharedDirector()->replaceScene(SendMsg::scene());
            }
            break;
        }
        case Client::QUERY_BIND:
        {
            CCJSONObject* json = CCJSONObject::create(p->getBody(), p->getBodyLength());
            CCJSONObject* data = json->optJSONObject("data");
            CCJSONArray* usernames = data->optJSONArray("usernames");
            if(usernames && usernames->getLength() > 0) {
                string firstName = usernames->optString(0);
                m_usernameEdit->setText(firstName.c_str());
            }
            break;
        }
        case Client::TEST_PUSH:
        {
            CCJSONObject* json = CCJSONObject::create(p->getBody(), p->getBodyLength());
            CCJSONObject* data = json->optJSONObject("data");
            string msg = data->optString("message");
            msg = CCUtils::decodeHtmlEntities(msg);
            CCLOG("server push: %s", msg.c_str());
            Helper::showToast(msg, this);
            break;
        }
        default:
            break;
    }
}

void Login::onLoginClicked(CCObject *sender) {
    CCJSONObject* json = CCJSONObject::create();
    json->addString("username", m_usernameEdit->getText());
    json->addString("password", CCMD5::md5(m_passwordEdit->getText()).c_str());
	json->addString("device_id", gUDID.c_str());
    Client::sharedClient()->send(1, json, Client::LOGIN, Client::NONE);
}

void Login::queryBind() {
	CCJSONObject* json = CCJSONObject::create();
	json->addString("device_id", gUDID.c_str());
	Client::sharedClient()->send(1, json, Client::QUERY_BIND, Client::NONE);
}