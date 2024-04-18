import eel
import os
import sys
import string
import base64

@eel.expose
def generate_svg(filename, strings, frets, openps, closeps, fretnums):
    cd:str
    svg:str
    tpl:str
    line:str
    w:str
    h:str
    x:str
    y:str
    f:str
    n:str

    # get current dir
    cd=os.path.dirname(os.path.abspath(sys.argv[0]))
    
    # mkdir svgs
    if(not os.path.isdir(cd+'/images')):
        os.mkdir(cd+'/images')
    
    # set svg path
    svg=cd+'/images/'+filename+'.svg'

    # remove svg 
    if(os.path.isfile(svg)):
        os.remove(svg)
    
    with open(svg,'a',encoding='utf-8')as file:
        # svg
        tpl=string.Template('<svg width="${w}" height="${h}" viewBox="0, 0, ${w}, 35" xmlns="http://www.w3.org/2000/svg">\n')
        w=str(20+(10*frets))
        h=str(5+(5*strings))
        line=tpl.substitute(w=w,h=h)
        file.write(line)

        # fingerboard(rect)
        for f in range(frets):
            for s in range(strings-1):
                tpl=string.Template('<rect x="${x}" y="${y}"  width="10" height="5" rx="0" ry="0" fill="none" stroke="#000"/>\n')
                x=str(13+(10*f))
                y=str(3+(5*s))
                line=tpl.substitute(x=x, y=y)
                file.write(line)

        # open_position
        for op in openps.split(','):
            if op != '':
                s=op.replace('s','').split('-')[0]
                ox=op.replace('s','').split('-')[1]

                if ox == 'o':
                    tpl=string.Template('<circle cx="8" cy="${cy}" r="2" fill="none" stroke="#000"/>\n')
                    cy=str(3+(5*(int(s)-1)))
                    line=tpl.substitute(cy=cy)
                elif ox == 'x':
                    tpl=string.Template('<line x1="6" y1="${l1y1}" x2="10" y2="${l1y2}" stroke="#000"/><line x1="10" y1="${l2y1}" x2="6" y2="${l2y2}" stroke="#000"/>\n')
                    l1y1=str(1+(5*(int(s)-1)))
                    l1y2=str(5*int(s))
                    l2y1=str(1+(5*(int(s)-1)))
                    l2y2=str(5*int(s))
                    line=tpl.substitute(l1y1=l1y1, l1y2=l1y2,l2y1=l2y1, l2y2=l2y2)
                
                file.write(line)

        # close_position
        for cp in closeps.split(','):
            if cp != '':
                tpl=string.Template('<circle cx="${cx}" cy="${cy}" r="2" fill="#000" stroke="#000"/>\n')
                s=cp.replace('s','').replace('f','').split('-')[0]
                f=cp.replace('s','').replace('f','').split('-')[1]
                cx=str(18+(10*(int(f)-1)))
                cy=str(3+(5*(int(s)-1)))
                line=tpl.substitute(cx=cx,cy=cy)
                file.write(line)
        
        # fret_nums
        for fn in fretnums.split(','):
            if fn != '':
                tpl=string.Template('<text x="${x}" y="34" font-size="4">${n}</text>\n')
                f=fn.split('f')[0]
                n=fn.split('f')[1]
                x=str(6+(10*int(f)))
                n=n.zfill(2)
                line=tpl.substitute(x=x,n=n)
                file.write(line)

        # svg
        file.write('</svg>\n')
    
    with open(svg,'rb')as file:
        data = base64.b64encode(file.read())

    # call js set_image
    eel.set_image(data.decode('utf-8'))

eel.init("web")
eel.start("index.html", size=(1500, 800),port=8000)
