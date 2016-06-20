from scrapy.http import Request,FormRequest,HtmlResponse
import gtk
import webkit
import jswebkit
import settings

class WebkitDownloader(object):
    def process_request(self,request,spider):
        if spider.name in settings.WEBKIT_DOWNLOADER:
            if(type(request)is not FormRequest):
                webview=webkit.WebView()
                webview.connect('load-finished',lambda v,f:gtk.main_quit())
                webview.load_url(request.url)
                gtk.main()
                js=jswebkit.JSContext(webview.get_main_frame().get_global_context())
                renderedBody=str(js.EvaluateScript('document.body.innerHTML'))
                return HtmlResponse(resquest.url,body=renderedBody)

