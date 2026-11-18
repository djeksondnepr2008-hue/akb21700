import sys
from PIL import Image, ImageDraw
def draw(S, full_bleed):
    bg=(23,33,43,255)
    im=Image.new("RGBA",(S,S),bg if full_bleed else (0,0,0,0)); d=ImageDraw.Draw(im); s=S/256
    if not full_bleed: d.rounded_rectangle([8*s,8*s,248*s,248*s],radius=44*s,fill=bg)
    k = 0.86 if full_bleed else 1.0   # для повного квадрата трохи зменшуємо малюнок (безпечна зона)
    off = (1-k)*128*s
    def P(x,y): return (off+x*k*s, off+y*k*s)
    cols=[(31,111,178),(208,97,42),(47,158,91)]; r=30*k*s
    for i in range(3):
        for j in range(2):
            cx,cy=P(70+58*i,92+60*j)
            d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=cols[i])
            d.ellipse([cx-r*0.8,cy-r*0.8,cx+r*0.8,cy+r*0.8],fill=(196,204,210,255))
            d.ellipse([cx-r*0.45,cy-r*0.45,cx+r*0.45,cy+r*0.45],fill=(238,241,243,255))
    w=12*k*s
    for i in range(3):
        cx,_=P(70+58*i,0); _,y1=P(0,66); _,y2=P(0,178)
        d.rounded_rectangle([cx-w/2,y1,cx+w/2,y2],radius=2*s,fill=(168,176,183,255))
    for j in range(2):
        _,cy=P(0,92+60*j); x1,_=P(70,0); x2,_=P(128,0)
        d.rounded_rectangle([x1,cy-w/2,x2,cy+w/2],radius=2*s,fill=(168,176,183,255))
    a=P(40,196); b=P(216,222); d.rounded_rectangle([a[0],a[1],b[0],b[1]],radius=8*k*s,fill=(31,111,178,255))
    a=P(210,203); b=P(226,215); d.rectangle([a[0],a[1],b[0],b[1]],fill=(31,111,178,255))
    return im
out=sys.argv[1]
draw(180,True).convert("RGB").save(out+"/apple-touch-icon.png")
draw(192,False).save(out+"/icon-192.png")
draw(512,False).save(out+"/icon-512.png")
draw(512,True).convert("RGB").save(out+"/icon-maskable-512.png")
draw(64,False).save(out+"/favicon.png")
