#include "FirstScene.h"

First::~First() {
}

CCScene* First::scene() {
    // 'scene' is an autorelease object
    CCScene* scene = CCScene::create();
    
    // 'layer' is an autorelease object
    First* layer = First::create();
	
    // add layer as a child to scene
    scene->addChild(layer);
	
    // return the scene
    return scene;
}

bool First::init() {
    // super init first
    if (!CCLayer::init()) {
        return false;
    }
    
    // surface size
    CCSize visibleSize = CCDirector::sharedDirector()->getVisibleSize();
    CCPoint origin = CCDirector::sharedDirector()->getVisibleOrigin();
    
    CCLabelTTF* label = CCLabelTTF::create("Hello", "Helvetica", 22 / CC_CONTENT_SCALE_FACTOR());
    label->setPosition(ccp(origin.x + visibleSize.width / 2,
                           origin.y + visibleSize.height / 2));
    addChild(label);
    
    return true;
}