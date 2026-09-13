import json, math
geo = json.load(open("RUS.geo.json"))

# Albers equal-area conic, tuned for Russia
lon0, lat0 = 100.0, 56.0
lat1, lat2 = 50.0, 65.0
r = math.radians
n = (math.sin(r(lat1)) + math.sin(r(lat2))) / 2
C = math.cos(r(lat1))**2 + 2*n*math.sin(r(lat1))
rho0 = math.sqrt(C - 2*n*math.sin(r(lat0)))/n
def proj(lon, lat):
    if lon < -100: lon += 360
    rho = math.sqrt(C - 2*n*math.sin(r(lat)))/n
    th = n*r(lon-lon0)
    return rho*math.sin(th), rho0 - rho*math.cos(th)

polys=[]
for f in geo["features"]:
    g=f["geometry"]; t=g["type"]; cs=g["coordinates"]
    rings = cs if t=="Polygon" else [ring for poly in cs for ring in poly]
    for ring in rings:
        polys.append([proj(x,y) for x,y in ring])

# (name, lat, lon, office?, label anchor, label dx, label dy, leader?)
regions = [
    ("Ростовская обл.",        47.24, 39.70, False, "start",  60, -8,  True),
    ("Краснодарский край",     45.04, 38.98, False, "start",  60,  24, True),
    ("Ставропольский край",    45.04, 41.97, False, "start",  60,  56, True),
    ("Омская обл.",            54.99, 73.37, False, "middle",  0, -20, False),
    ("Новосибирская обл.",     55.03, 82.92, False, "middle",  0, -20, False),
    ("Алтайский край · Барнаул",53.35, 83.78, True, "middle",  0,  34, False),
    ("Красноярский край",      56.01, 92.85, False, "start",  18,  5,  False),
    ("Амурская обл.",          50.29,127.53, False, "start",  18,  5,  False),
]
pts=[(name,)+proj(lon,lat)+(off,anc,dx,dy,ld) for (name,lat,lon,off,anc,dx,dy,ld) in regions]

xs=[x for p in polys for x,y in p]+[x for r in pts for x in (r[1],)]
ys=[y for p in polys for x,y in p]+[y for r in pts for y in (r[2],)]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
W,H=1600,900; pad=70
s=min((W-2*pad)/(maxx-minx),(H-2*pad)/(maxy-miny))
offx=(W-(maxx-minx)*s)/2; offy=(H-(maxy-miny)*s)/2
def T(x,y): return (offx+(x-minx)*s, offy+(maxy-y)*s)
def path(poly):
    return "".join(("M" if i==0 else "L")+f"{T(x,y)[0]:.1f} {T(x,y)[1]:.1f}" for i,(x,y) in enumerate(poly))+"Z"

BG="#141210"; LAND="#26211C"; STROKE="rgba(255,255,255,.16)"; ORANGE="#FF4200"; TXT="#F3F1EE"
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Montserrat,Arial,sans-serif">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
for poly in polys:
    svg.append(f'<path d="{path(poly)}" fill="{LAND}" stroke="{STROKE}" stroke-width="1.2" stroke-linejoin="round"/>')
for name,x,y,off,anc,dx,dy,ld in pts:
    px,py=T(x,y); lx,ly=px+dx,py+dy
    if ld:
        svg.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{lx-6:.1f}" y2="{ly-5:.1f}" stroke="rgba(255,255,255,.28)" stroke-width="1"/>')
    if off:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="14" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#fff"/>')
        col="#fff"; fw="700"
    else:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{ORANGE}"/><circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="none" stroke="{ORANGE}" stroke-opacity=".25" stroke-width="7"/>')
        col=TXT; fw="600"
    svg.append(f'<text x="{lx:.1f}" y="{ly:.1f}" fill="{col}" font-size="21" font-weight="{fw}" text-anchor="{anc}">{name}</text>')
# title + legend
svg.append(f'<text x="70" y="70" fill="#fff" font-size="30" font-weight="800">География поставок</text>')
svg.append(f'<text x="70" y="102" fill="#B9B2AA" font-size="18">8 регионов · офис в Барнауле</text>')
lgx,lgy=1180,60
svg.append(f'<circle cx="{lgx}" cy="{lgy}" r="8" fill="{ORANGE}"/><text x="{lgx+18}" y="{lgy+6}" fill="{TXT}" font-size="19">регионы поставок</text>')
svg.append(f'<circle cx="{lgx}" cy="{lgy+34}" r="9" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="{lgx}" cy="{lgy+34}" r="4" fill="#fff"/><text x="{lgx+18}" y="{lgy+40}" fill="{TXT}" font-size="19">офис · Барнаул</text>')
svg.append('</svg>')
open("map_ref.svg","w").write("\n".join(svg))
print("wrote map_ref.svg")
