package org.cocos2dx.testcpp;

import org.cocos2dx.lib.Cocos2dxActivity;

import android.os.Bundle;

public class MainActivity extends Cocos2dxActivity {
	static {
		System.loadLibrary("game");
	}
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
	}
}
