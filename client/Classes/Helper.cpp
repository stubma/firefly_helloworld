#include "Helper.h"

void Helper::showToast(const string& msg, CCNode* owner) {
	CCSize visibleSize = CCDirector::sharedDirector()->getVisibleSize();
	CCPoint origin = CCDirector::sharedDirector()->getVisibleOrigin();
	CCToast* t = CCToast::create(owner, CCLabelTTF::create(msg.c_str(), "Helvetica", 40 / CC_CONTENT_SCALE_FACTOR()));
	t->setPosition(ccp(origin.x + visibleSize.width / 2,
					   origin.y + visibleSize.height / 5));
}