#ifndef __FirstScene__
#define __FirstScene__

/**
 * First scene
 */
class First : public CCLayer {
public:
	virtual ~First();
    
    // there's no 'id' in cpp, so we recommend returning the class instance pointer
    static CCScene* scene();
	
    // Here's a difference. Method 'init' in cocos2d-x returns bool, instead of returning 'id' in cocos2d-iphone
    virtual bool init();
    
    // implement the "static node()" method manually
    CREATE_FUNC(First);
};

#endif /* defined(__FirstScene__) */
