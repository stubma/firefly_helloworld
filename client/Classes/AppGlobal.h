#ifndef __AppGlobal_h__
#define __AppGlobal_h__

typedef struct {
	/// resource base size
    CCSize size;
	
	/// resource base dir
    char directory[100];
} Resource;

static Resource _mediumResource = {
	CCSizeMake(480, 800),
	"480x800"
};

static Resource& R = _mediumResource;
static CCSize designResolutionSize = CCSizeMake(480, 800);

#endif /* __AppGlobal_h__ */
