from jnius import autoclass,PythonJavaClass,java_method   
CustomJavaWebviewClient = autoclass('org.test.CustomWebviewClient')


#Webview Client  
def WebviewClient(WebviewEngineObj):
	
	#lets get the inflector class which will be the input
	#of the CustomJavaWebviewClient's constructor
	WebviewClientCoreClass = WebviewClientCore(WebviewEngineObj)

	WebviewClientResults = CustomJavaWebviewClient(WebviewClientCoreClass)

	return WebviewClientResults


#This is for the callback , we will create classes for the interface
class WebviewClientCore(PythonJavaClass):

	__javacontext__ = 'app'

	__javainterfaces__ = ['org.test.CustomWebviewClientInterface']

	 
	#Constructor 
	def __init__(self,webview_engine_obj):
		super(WebviewClientCore,self).__init__()

		self._webviewEngine = webview_engine_obj()


	##On Page Finished Loading 
	@java_method('(Landroid/webkit/WebView;Ljava/lang/String;)Z')
	def shouldOverrideUrlLoading(self,view,url):

		#dispatch event 
		self._webviewEngine.dispatch_event(event_name='on_should_override_url_loading', webview=view, url=url)


	#On page Started Loading
	#@java_method('(Landroid/webkit/WebView;Ljava/lang/String;Landroid/graphics/Bitmap;)V')
	#def onPageStarted(self,view,url,favicon):
	
		#dispatch event 
		#self._webviewEngine.dispatch_event(event_name='on_page_started', webview=view, url=url, favicon=favicon)

	##On Page Finished Loading 
	#@java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
	#def onPageFinished(self,view,url):

		#dispatch event 
		#self._webviewEngine.dispatch_event(event_name='on_page_finished', webview=view, url=url)
	 
	#onPageCommitVisible
	#@java_method('(Landroid/webkit/WebView;Ljava/lang/String;)V')
	#def onPageCommitVisible(self,view,url):

		#dispatch event 
		#self._webviewEngine.dispatch_event(event_name='on_page_commit_visible', webview=view, url=url)
		
	
	#onKeyDown
	#@java_method('(Landroid/webkit/WebView;Ljava/lang/String;)Z')
	#def onKeyDown(self, keyCode, KeyEvent):
		#dispatch event
		#sel._webviewEngine.dispatch_keydown_event(event_name='on_key_down', keyCode=keycode, KeyEvent=event)


	#OnReceivedError 
	#@java_method('(Landroid/webkit/WebView;Ljava/lang/Integer;Ljava/lang/String;Ljava/lang/String;)V')
	#def onReceivedError(self,view, errorCode, description, url):

		#dispatch event 
		#self._webviewEngine.dispatch_event(event_name='on_received_error', webview=view, error_code=errorCode, description=description, failing_url=url)
