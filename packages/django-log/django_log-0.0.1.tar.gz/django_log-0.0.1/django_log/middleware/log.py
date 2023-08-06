import datetime
import pprint
import json
import traceback
from django.conf import settings

class LogRequestResponseData:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        self.text_file = ''

    def __call__(self, request):
        try:
            # Code to be executed for each request before
            # the view (and later middleware) are called.
            self.collect_request(request)
            response = self.get_response(request)
            # Code to be executed for each request/response after
            # the view is called.
            self.collect_response(response)
            self.append_in_file()
            return response
        except Exception as e:
            print(str(e))
            response = self.get_response(request)
            return response


    def collect_request(self,request):
        """
        Build output data from request
        request: WSGIRequest
        return: 
        """
        self.add_line('___REQUEST___')
        #user id of request
        self.add_line('User token: {}'.format(self.get_info_user(request)))
        #path url
        self.add_line('url: {}'.format(request.path))
        #add method
        self.add_line('Method: {}'.format(request.method))
        #time
        self.add_line('Time: {}'.format(datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')))
        #get paramnets
        self.add_line('GET Paraments:')
        self.add_line(pprint.pformat(request.GET,indent=1))
        #post data
        self.add_line('POST data:')
        if request.body:
            body_request = json.loads(request.body)
        else:
            body_request = '{}'
        self.add_line(pprint.pformat(body_request,indent=1))          
        
    def add_line(self,text):
        """
        Add one line in output
        text: str
        return:
        """
        self.text_file += '{}\n'.format(text)
        
    def collect_response(self,response):
        """
        Build output data from response
        response: Response
        return:
        """
        self.add_line('___RESPONSE___')
        #code http of response
        self.add_line('status_code: {}'.format(response.status_code))
        #body
        self.add_line('body data:')
        self.add_line(pprint.pformat(response.data,indent=2))
    
    def append_in_file(self):
        """
        Append info in file of log
        """
        self.add_line('')
        self.add_line('---------------------------------------------------------------------')
        self.add_line('')
        with open(getattr(settings,'LOG_FILE','/logs/request_response.txt'),'a') as f:
            f.write(self.text_file)
    
    def process_exception(self,request,exception):
        """
        handle with errors
        """
        self.add_line('ERRORS:')
        self.add_line(traceback.format_exc())
        self.append_in_file()
    
    def get_info_user(self,request):
        """
        Check if have user in request and get info about his
        request: WSGIRequest
        """
        try:
            user_token = request.META['HTTP_AUTHORIZATION']
        except:
            user_token = ''
        else:
            return user_token