#ifndef __AppGlobal_h__
#define __AppGlobal_h__

typedef struct {
	/// resource base size
    CCSize size;
	
	/// resource base dir
    char directory[100];
} Resource;

static Resource _mediumResource = {
	CCSizeMake(800, 480),
	"800x480"
};

static Resource& R = _mediumResource;
static CCSize designResolutionSize = CCSizeMake(800, 480);

#endif /* __AppGlobal_h__ */
