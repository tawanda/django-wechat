# django-wechat
Access WeChat functions using django views

tested in python 3.5 and django 1.8, but should work with lower versions of both

This is more a code snippet rather than an actual app

Currently this snippet is only for reading WeChat messages, but you can extend it, pull requests welcome


## useful videos

these videos give you an overview of how to setup WeChat. They are in PHP but the message is clear

[video 1](https://www.youtube.com/watch?v=kB20Zf51QWU)

[video 2](https://www.youtube.com/watch?v=_2FSzD2B2F0)


# 1) Project setup

To begin create your app and make your custom url point to our
wechat view

`http://mysite/wechat/`

subclass the view in the wechat directory of this project

```python
    
    import xml.etree.ElementTree as ET
    
    from wechat.views import WeChatView


    MyCustomView(WeChatView):
        token = "ad4sf65weG7Db6ddWE"
        
        on_message(self, message):
                
            root = ET.fromstring(message)

            from = root[1].text
            message_type = root[3].text
            content = root[4].text

            print('from: {}'.format(from))
            print('message type: {}'.format(message_type))
            print('content: {}'.format(content))
        
```


#### token

You need to set this yourself, use any alphanumeric string, if you use any special characters WeChat 
wont authenticate


#### on_message

The messages come as xml, so here we use an xml reader just to print out the message. to see all
the different message types check here

[WeChat Message Types](http://admin.wechat.com/wiki/index.php?title=Common_Messages)


# 2) Creating a WeChat Developer account

### Create developer account

* head over to [http://admin.wechat.com/debug/sandbox](http://admin.wechat.com/debug/sandbox)
* Click on Login
* Scan the QR code

You should see the sandbox developer page now

### Authenticate your app

In the developer page look for the heading `API config` there will be entry fields for URL and Token

* Ensure your web app is running and your custom view is accessible on http://mysite/wechat/
* If you are testing on localhost a good tool to use is [ngrok](https://ngrok.com/docs#expose)

URL: enter the url you chose for your view e.g. `http://mysite/wechat/` or the same url if you are using 
ngrok to expose your localhost to the outside world could be e.g. `http://bfwr41f123b.ngrok.io/wechat/`

TOKEN: enter the token you chose in step 1), remember it has to be the same as your views token and only alphanumeric

once you click ok you should see a message that says successful or something similar

### Add the sandbox account to your WeChat account

* Open WeChat on your mobile phone and go to Discover->Scan QR Code
* On your developer page scroll down to the heading `Test account QR Code` and scan that QR Code
* Now send a message to the account added to your phone under subscription accounts
* Smile as you see your message come in your console




