import hashlib
import logging

from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import View


logger = logging.getLogger('wechat.api')


class WeChatView(View):
    """
    WeChat API
    """
    token = ""

    def get(self, request, *args, **kwargs):
        logger.info('- New GET From WeChat -')

        authenticated, data = self.authenticate(request, kwargs)

        if authenticated:
            if data['echostr']:
                    logger.info('sending response..')
                    logger.info('echostr: {}'.format(data['echostr']))
                    return HttpResponse(data['echostr'])
            else:
                logger.info('WeChat Authenticated, but nonce is missing in a GET request, signature:{} timestamp:{} '
                            'nonce:{}'.format(data['signature'], data['timestamp'], data['nonce']))
                return HttpResponse(status=200)

        return HttpResponse(status=403)

    def post(self, request, *args, **kwargs):
        logger.info('- New POST From WeChat -')

        authenticated, data = self.authenticate(request, kwargs)

        if authenticated:
            # This is what we send to the message processing task
            logger.info('New message received: {}'.format(request.body))

            self.on_message(message=request.body)
            return HttpResponse(status=201)

        return HttpResponse(status=403)

    def authenticate(self, request, kwargs):
        data = dict()

        try:
            signature = request.GET['signature']
            timestamp = request.GET['timestamp']
            nonce = request.GET['nonce']
            echostr = request.GET.get('echostr', '')

        except MultiValueDictKeyError:
            logger.error('missing parameters in WeChat request')
            return False, data

        if not self.token:
            logger.error('Token not set on class instance')
            return False, data

        params = [self.token, timestamp, nonce]
        params.sort()
        auth_string = ''.join(params)

        if self.validate_signature(auth_string, signature):
            data.update({
               'signature': signature,
               'timestamp': timestamp,
               'nonce': nonce,
               'echostr': echostr,
               'token': self.token,
            })
            return True, data
        else:
            logger.info('WeChat Authentication failed, signature:{} timestamp:{} nonce:{}'
                        .format(signature, timestamp, nonce))
            return False, data

    @staticmethod
    def validate_signature(auth_string, signature):
        return hashlib.sha1(auth_string.encode()).hexdigest() == signature

    def on_message(self, message):
        # do something with the message here
        raise NotImplementedError('You need to do something with the message from WeChat')
