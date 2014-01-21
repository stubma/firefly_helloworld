#include "AppGlobal.h"

CCTCPSocketHub* gHub = NULL;

void initHub() {
    gHub = CCTCPSocketHub::create();
    CC_SAFE_RETAIN(gHub);
}