import six

class PartWrapper(object):
    def __init__(self, part, response):
        self.__part = part
        self.__response = response
        
        #The requests-toolbelt multipart parser creates headers as byte strings (b'...') but the requests library
        #uses ordinary strings ('...'). To get around this we convert any non-string headers to strings by calling convert_to_str.
        #Both sets of headers are converted this way in case the behaviour of the requests library varies between versions
        self.headers = PartWrapper.convert_to_str(response.headers)
        self.headers.update(PartWrapper.convert_to_str(part.headers))
    
    def __getattr__(self, name):
        if (hasattr(self.__part, name)):
            return getattr(self.__part, name)
        else:
            return getattr(self.__response, name)
       
    @staticmethod 
    def convert_to_str(d):
        return {  k if isinstance(k, six.string_types) else str(k, 'utf-8') 
                : v if isinstance(v, six.string_types) else str(v, 'utf-8') 
                        for (k,v) in d.items()}