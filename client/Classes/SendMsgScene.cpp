#include "SendMsgScene.h"
#include "Client.h"

SendMsg::~SendMsg() {
}

CCScene* SendMsg::scene() {
    // 'scene' is an autorelease object
    CCScene* scene = CCScene::create();
    
    // 'layer' is an autorelease object
    SendMsg* layer = SendMsg::create();
	
    // add layer as a child to scene
    scene->addChild(layer);
	
    // return the scene
    return scene;
}

bool SendMsg::init() {
    // super init first
    if (!CCLayer::init()) {
        return false;
    }
    
    // surface size
    CCSize visibleSize = CCDirector::sharedDirector()->getVisibleSize();
    CCPoint origin = CCDirector::sharedDirector()->getVisibleOrigin();
    
    // login item
    CCLabelTTF* label = CCLabelTTF::create("Send", "Helvetica", 40 / CC_CONTENT_SCALE_FACTOR());
    CCMenuItemLabel* sendItem = CCMenuItemLabel::create(label, this, menu_selector(SendMsg::onSendClicked));
    sendItem->setPosition(ccp(origin.x + visibleSize.width / 2,
                              origin.y + visibleSize.height * 6 / 10));
    
    // menu
    CCMenu* menu = CCMenu::create(sendItem, NULL);
    menu->setPosition(CCPointZero);
    addChild(menu);
    
    // message edit
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
        m_msgEdit = CCEditBox::create(editSize, editNormal, editPressed);
        m_msgEdit->setReturnType(kKeyboardReturnTypeDone);
        m_msgEdit->setFontSize(12);
        m_msgEdit->setText("");
        m_msgEdit->setMaxLength(8);
        m_msgEdit->setFontColor(ccc3(158, 122, 83));
        m_msgEdit->setPosition(ccp(origin.x + visibleSize.width / 2,
                                   origin.y + visibleSize.height * 8 / 10));
        addChild(m_msgEdit);
    }
    
    // add hub
    CCTCPSocketHub* hub = Client::sharedClient()->getHub();
    hub->registerCallback(1, this);
    addChild(hub);
    
    return true;
}

void SendMsg::onSendClicked(CCObject* sender) {
    CCJSONObject* json = CCJSONObject::create();
    json->addString("message", m_msgEdit->getText());
    Client::sharedClient()->send(1, json, Client::TEST);
}

void SendMsg::onTCPSocketConnected(int tag) {
}

void SendMsg::onTCPSocketDisconnected(int tag) {
}

void SendMsg::onTCPSocketData(int tag, CCByteBuffer& bb) {
    const CCArray& packets = Client::sharedClient()->addData(bb);
    CCObject* obj = NULL;
    CCARRAY_FOREACH(&packets, obj) {
        Packet* p = (Packet*)obj;
        CCLOG("cmd: %d, data: %s", p->getHeader().command, p->getBody());
        CCJSONObject* json = CCJSONObject::create(p->getBody(), p->getBodyLength());
        Client::ErrCode err = (Client::ErrCode)json->optInt("errno");
        if(err != Client::E_OK) {
            string errMsg = json->optString("errmsg");
            CCLOG("error message: %s", errMsg.c_str());
        }
    }
}