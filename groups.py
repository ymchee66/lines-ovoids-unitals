import re,glob
def all_groups():
    """list of (file, name, v, tmax)"""
    G=[]
    for f in glob.glob('[SGP]2_*.txt'):
        kind=f[0]; q=int(f[3:-4])
        if kind=='S': tm=3 if (q%2==0 or q%4==3) else 2; name=f'PSL(2,{q})'
        elif kind=='G': tm=3; name=f'PGL(2,{q})'
        else: tm=4 if q in (8,32) else 3; name=f'PGammaL(2,{q})'
        G.append((f,name,q+1,tm))
    for f,name,v in [('L33.txt','PSL(3,3)',13),('L37.txt','PSL(3,7)',57),('L43.txt','PSL(4,3)',40),('L38.txt','PSL(3,8)',73),
                     ('U33.txt','PSU(3,3)',28),('U34.txt','PSU(3,4)',65),('Sz8.txt','Sz(8)',65),('R3.txt','2G2(3)',28)]:
        G.append((f,name,v,2))
    hom={}
    for line in open('hom2.txt'):
        m=re.match(r'(\d+) (\d+) (\d+) (\d+) "(.*)"',line); hom[(int(m[1]),int(m[2]))]=(int(m[4]),m[5])
    for f in glob.glob('aff/A_*.txt'):
        d,i=map(int,re.findall(r'A_(\d+)_(\d+)',f)[0]); tm,name=hom[(d,i)]
        G.append((f,name,d,tm))
    return G
