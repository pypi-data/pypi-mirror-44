import requests

class Backend():
    def __init__(self,*args,**kargs):
        self.url = kargs.get("url")

    def __call__(self,classObj):
        def constructor(*args,**kargs):
            selfOrig = args[0]
            selfOrig.headers = {}
            selfOrig.url = self.url

        def addHeader(selfOrig,name,value):
            selfOrig.headers.update({name:value})

        def send(*args,**kargs):
            selfOrig = args[0]
            selfOrig.finalize()
            response = requests.request(kargs.get("method"),kargs.get("url"),headers = selfOrig.headers,data=kargs.get("data"))
            if response.ok:
                return response.json()
            else:
                raise Exception("backend error")

        def getUrl(*args,**kargs):
            selfOrig = args[0]
            return selfOrig.url

        def finalize(*args,**kargs):
            pass

        classObj.__init__ = constructor
        classObj.addHeader = addHeader
        classObj.send = send
        classObj.getUrl = getUrl
        classObj.finalize = finalize

        return classObj
