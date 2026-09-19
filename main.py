from kivy.app import App
from kivy.uix.widget import Widget
from kivy.utils import platform
from kivy.core.window import Window

# Hide status bar for a true full-screen game experience
Window.fullscreen = 'auto'

class WebGameApp(App):
    def build(self):
        return Widget()

    def on_start(self):
        if platform == 'android':
            from jnius import autoclass
            from android.runnable import run_on_ui_thread

            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            Activity = autoclass('org.kivy.android.PythonActivity').mActivity

            @run_on_ui_thread
            def create_webview():
                webview = WebView(Activity)
                settings = webview.getSettings()
                
                # Zaroori settings taaki game theek se chale
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True) 
                
                webview.setWebViewClient(WebViewClient()) 
                
                # Yeh link aap change kar sakte hain
                webview.loadUrl('https://yyg.myfunmax.com/Pubg_Hack/index.html?st=13&miref=launcher') 
                
                Activity.setContentView(webview)

            create_webview()

if __name__ == '__main__':
    WebGameApp().run()
