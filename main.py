from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from android.runnable import run_on_ui_thread
from kivy.event import EventDispatcher
from jnius import autoclass
from webviewclient import WebviewClient

# Load Native Modules
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.kivy.android.PythonActivity').mActivity
LayoutParams = autoclass('android.view.ViewGroup$LayoutParams')
View = autoclass('android.view.View')

with open("secret_user.txt", "r") as file:
    data = file.readlines()
print(data)

@run_on_ui_thread
def create_webview(*args):
    global webview
    # if the webview is created already, skip it
    if (WebviewEngine._webview_obj):
        return True

        # if we have reached this point, then mean the webview is not created
    webview = WebView(activity)

    settings = webview.getSettings()
    settings.setJavaScriptEnabled(True)
    settings.setUseWideViewPort(True)  # enables viewport html meta tags
    settings.setLoadWithOverviewMode(True)  # uses viewport
    settings.setSupportZoom(True)  # enables zoom
    settings.setBuiltInZoomControls(True)  # enables zoom controls

    # set java events
    webviewClient = WebviewClient(WebviewEngine)
    webview.setWebViewClient(webviewClient)
    activity.setContentView(webview)

    if data[1] == "secret_password":
        res = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 30))
        data[0] = str(res) + "\n"
        
        with open("secret_user.txt", "w") as file:
            for d in data:
                file.write(d)

        file.close()
        

        url = 'https://comohacerblog.net/user/user_signup.php?secret_user={}'.format(data[0])
    else:
        print("false", data[1])
        url = 'https://comohacerblog.net/user/user_login.php?secret_user={}&secret_password={}'.format(data[0], data[1])

    webview.loadUrl(url)
    WebviewEngine._webview_obj = webview


# hide - This will hide the webview widget
@run_on_ui_thread
def hide():
    if WebviewEngine._webview_obj is None and WebviewEngine.is_visible == False:
        return False

    WebviewEngine._webview_obj.setVisibility(View.GONE)


class WebviewEngine(Widget, EventDispatcher):
    is_visible = True

    _webview_obj = None

    _webview_events = ['on_should_override_url_loading', ]

    # initialize :D -- Sweet
    def __init__(self, **kwargs):
        # register Events
        self._register_events()
        print(dir(self._event_default_handler))

        super().__init__(**kwargs)
        Clock.schedule_once(create_webview, 0)


    # method for dispatching events
    def dispatch_event(self, event_name, webview, url, **kwargs):
        # dispatch
        self.dispatch(event_name, webview, url, **kwargs)
        print('--- Event %s dispatched \n' % event_name)

    # default event handler
    def _event_default_handler(self, **kwargs):
        print('--- Event Handler +++ \n')
        pass

    # Event registrar
    def _register_events(self):
        events = self._webview_events

        # loop and register them
        for event_name in events:

            # register the event
            self.register_event_type(event_name)

    def on_should_override_url_loading(self, *args):
        global data
        print("++++++++++on_should_override_url_loading-----------")
        print("------new url======", args[1])
        url = args[1]

        if "user_signup_successful.php" in url:
            print('----------------------------True')
            data[1] = str(url[-30:]) + "\n"
            webview.loadUrl(
                'https://comohacerblog.net/user/user_login.php?secret_user={}&secret_password={}'.format(data[0],
                                                                                                         data[1]))

        with open("secret_user.txt", "w") as user_file:
            for d in data:
                user_file.write(d)
        user_file.close()

        print("web url++++++++++++++++++++++", webview.getUrl())

class ServiceApp(App):
    webviewEngine = None

    # address box
    address_bar = ObjectProperty(None)

    # can Go Back
    can_go_back = BooleanProperty(False)

    # can go forward
    can_go_forward = BooleanProperty(False)

    def build(self):
        self.webviewEngine = WebviewEngine()
        # print(on_page_started)
        self.webviewEngine.bind(on_page_started=self.proccess_on_page_start)
        self.webviewEngine.bind(on_page_commit_visible=self.proccess_on_page_commit_visible)
        self.webviewEngine.bind(on_should_override_url_loading=self.on_should_override_url_loading)
        return self.webviewEngine

    # proccess back button
    def proccess_go_back(self):
        # if page can go back, then go back
        if (self.can_go_back == True):
            self.webviewEngine.goBack()

    # Proccess Go Back
    def proccess_go_forward(self):
        # if can go forward, then go
        if (self.can_go_forward == True):
            self.webviewEngine.goForward()

    # enable disable back and forward button
    def proccess_on_page_start(self, *args, **kwargs):
        # change the url to the new url
        new_url = kwargs.get('url')
        print("------new url======", new_url)
        # if (new_url is not None):
        #     self.update_address_bar_url(new_url)

    # proccess on Page Commit visible
    def proccess_on_page_commit_visible(self, *args, **kwargs):
        # if the webview can go back, update the button
        self.can_go_back = self.webviewEngine.canGoBack()
        # check if it can go forward
        self.can_go_forward = self.webviewEngine.canGoForward()

    # should_override_url_loading
    def on_should_override_url_loading(self, *args, **kwargs):
        # change the url to the new url
        new_url = kwargs.get('url')
        print("------new loading url======", new_url)


if __name__ == '__main__':
    ServiceApp().run()

