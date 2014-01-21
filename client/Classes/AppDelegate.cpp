#include "AppDelegate.h"
#include "LoginScene.h"
#include "AppGlobal.h"

AppDelegate::AppDelegate() {
}

AppDelegate::~AppDelegate() {
    CC_SAFE_RELEASE(gHub);
    gHub = NULL;
}

bool AppDelegate::applicationDidFinishLaunching() {
    // initialize director
    CCDirector* pDirector = CCDirector::sharedDirector();
    CCEGLView* pEGLView = CCEGLView::sharedOpenGLView();
    pDirector->setOpenGLView(pEGLView);

    // Set the design resolution
    pEGLView->setDesignResolutionSize(designResolutionSize.width, designResolutionSize.height, kResolutionNoBorder);
    
    // search path
    vector<string> searchPath;
    searchPath.push_back(R.directory);
    CCFileUtils::sharedFileUtils()->setSearchPaths(searchPath);
	
    // turn on display FPS
#ifdef COCOS2D_DEBUG
//    pDirector->setDisplayStats(true);
//    Helper::setHelpShown(false);
#endif
    
    // init
    initHub();

    // create a scene. it's an autorelease object
    CCScene* pScene = Login::scene();

    // run
    pDirector->runWithScene(pScene);

    return true;
}

// This function will be called when the app is inactive. When comes a phone call,it's be invoked too
void AppDelegate::applicationDidEnterBackground() {
    CCDirector::sharedDirector()->stopAnimation();
}

// this function will be called when the app is active again
void AppDelegate::applicationWillEnterForeground() {
    CCDirector::sharedDirector()->startAnimation();
}
