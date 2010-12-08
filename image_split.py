import Image, StringIO
HOME='/u/carlos/'
def right_size(im):
    w, h = im.size
    if w/5 > h:
        return h
    else:
        return w/5

def img_split(str):
    d = Image.open(StringIO.StringIO(str))
    s = right_size(d)
    r = []
    for i in range(5):
        r.append(d.crop((i*s,0,(i+1)*s,s)))
    return r

def m():
    f = open(HOME+'b.png','rb').read()
    r = img_split(f)
    i=0
    for a in r:
        i+=1
        a.save(HOME+'a%d.png'%i)

[m() for x in range(30)]

