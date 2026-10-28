from PIL import Image
import numpy as np, math, sys, json
from scipy import ndimage
def fit(a,rowguess,xlo,xhi):
    W=(a.min(axis=2)>215)
    band=W[rowguess-25:rowguess+25, xlo:xhi].sum(1); row=rowguess-25+np.argmax(band)
    ys,xs=np.where(W[row-95:row+95,:]); ys=ys+row-95
    m=(abs(ys-row)>6)&(xs>xlo)&(xs<xhi); xs2,ys2=xs[m].astype(float),ys[m].astype(float)
    A=np.c_[2*xs2,2*ys2,np.ones(len(xs2))]; b=xs2**2+ys2**2; c=np.linalg.lstsq(A,b,rcond=None)[0]; R=math.sqrt(max(0,c[2]+c[0]**2+c[1]**2))
    return c[0],c[1],R,row
def ball(a,bx0,by0,h=14):
    x0,y0=bx0-h,by0-h; s=a[y0:y0+2*h,x0:x0+2*h]; g=(s[:,:,1]-s[:,:,0]>60)
    lab,n=ndimage.label(~g); best=None
    for k in range(1,n+1):
        Y,X=np.where(lab==k)
        if len(X)>8 and (best is None or len(X)>best[2]): best=(X.mean()+x0,Y.mean()+y0,len(X))
    return best[0],best[1]
cfg=json.loads(sys.argv[1]); out={}
for n,(rowg,(xl,xh),(bx,by)) in cfg.items():
    a=np.array(Image.open('../figuras/capturas/%s_capturas.png'%n).convert('RGB')).astype(int)
    cx,cy,R,row=fit(a,rowg,xl,xh); bx,by=ball(a,bx,by)
    d=math.hypot(bx-cx,by-cy)/(2*R); ang=math.degrees(math.atan2(by-cy,-(bx-cx)))
    print(n,'circle %.0f %.0f R %.1f row %d | ball %.0f %.0f | dist %.2f D | ang(+izq) %.0f'%(cx,cy,R,row,bx,by,d,ang)); out[n]=(round(d,2),round(ang))
print(json.dumps(out))
