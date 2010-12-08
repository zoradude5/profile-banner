from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import images
from google.appengine.ext.webapp import template
import StringIO,os
import facebook,logging,utils
from facebook_private import *

class Upload(webapp.RequestHandler):
    def get(self):
        index = os.path.join(os.path.dirname(__file__), 'pages/index.html')
        self.response.out.write(template.render(index, {}))

    def post(self):
        import_str = str(self.request.get("import_file"))
        imgs = mul_img(import_str)#img_split(import_str)
        user = facebook.get_user_from_cookie(self.request.cookies, id, secret)
        if user:
            graph = facebook.GraphAPI(user["access_token"])
#            logging.error(graph.multipart_request("me/photos", post_args={'message': 'test'}, files={'source': import_str}))
            #graph.put_wall_post('test')
            for i in imgs:
                logging.error(i)
                out = utils.posturl('https://graph.facebook.com/me/photos', [('access_token', user['access_token'])], 
                            [('myfile', 'myimage.jpg', i)])#request.files['import_file'].stream.read()
#            graph.put_event(name='test', start_time='1272718027', location='someplace')
        self.response.out.write(self.request.cookies)


def right_proportion(im):
    w, h = im.width, im.height
    if w/5 > h:
#        return 1.0, 1.0
        return float(h)/w, 1.0
    else:
#        return 1.0/5, 1.0/5
        return float(1)/5, (float(w)/5)/h

"""def img_split(str):
    d = images.Image(str)
    wp, hp = right_proportion(d)
    logging.error(wp)
    logging.error(hp)
    r = []
    for i in range(5):
        r.append(d.crop(i*wp,0.0,(i+1)*wp,hp))
    return r"""

def mul_img(str):
    r = []
    for i in range(5):
        d = images.Image(str)
        wp, hp = right_proportion(d)
        d.crop(i*wp,0.0,(i+1)*wp,hp)
        r.append(d.execute_transforms())
    return r
    

app = webapp.WSGIApplication([('/', Upload)])


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
