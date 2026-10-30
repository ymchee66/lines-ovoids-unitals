import sys,re
P=int(sys.argv[1]); TARGET=tuple(map(int,sys.argv[2:5]))
sys.argv=['close.py',str(P),'2000','4']
src=open('close.py').read().split("known=sorted")[0]
exec(src)
x=TARGET
for _ in range(10):
    w=L.E.get(x); print(x,w)
    m=re.search(r'\((\d+),(\d+),(\d+)\)',w or '')
    if not m: break
    x=tuple(map(int,m.groups()))
