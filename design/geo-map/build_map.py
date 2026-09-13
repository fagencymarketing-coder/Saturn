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

W,H=1600,900; pad=70
# provisional fit (needs pin px for layout) -> compute transform first from polys+pins
raw=[("Ростовская обл.",47.24,39.70,False),("Краснодарский край",45.04,38.98,False),
     ("Ставропольский край",45.04,41.97,False),("Омская обл.",54.99,73.37,False),
     ("Новосибирская обл.",55.03,82.92,False),("Алтайский край · Барнаул",53.35,83.78,True),
     ("Красноярский край",56.01,92.85,False),("Амурская обл.",50.29,127.53,False)]
projpts=[(nm,)+proj(lo,la)+(off,) for (nm,la,lo,off) in raw]
xs=[x for p in polys for x,y in p]+[pp[1] for pp in projpts]
ys=[y for p in polys for x,y in p]+[pp[2] for pp in projpts]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
s=min((W-2*pad)/(maxx-minx),(H-2*pad)/(maxy-miny))
offx=(W-(maxx-minx)*s)/2; offy=(H-(maxy-miny)*s)/2
def T(x,y): return (offx+(x-minx)*s, offy+(maxy-y)*s)
def path(poly):
    return "".join(("M" if i==0 else "L")+f"{T(x,y)[0]:.1f} {T(x,y)[1]:.1f}" for i,(x,y) in enumerate(poly))+"Z"

# explicit label layout: (name, office, labelX, labelY, anchor, leaderEndX, leaderEndY)
LAB={
 "Ростовская обл.":       (False, 232,505,"start",226,500),
 "Краснодарский край":    (False, 232,547,"start",226,542),
 "Ставропольский край":   (False, 232,589,"start",226,584),
 "Омская обл.":           (False, 581,596,"middle",581,604),
 "Новосибирская обл.":    (False, 758,610,"start",752,614),
 "Алтайский край · Барнаул":(True, 683,734,"middle",683,726),
 "Красноярский край":     (False, 838,676,"start",832,672),
 "Амурская обл.":         (False,1236,715,"start",1230,715),
}

BG="#141210"; LAND="#26211C"; STROKE="rgba(255,255,255,.16)"; ORANGE="#FF4200"; TXT="#F3F1EE"; LEAD="rgba(255,255,255,.32)"
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Montserrat,Arial,sans-serif">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
for poly in polys:
    svg.append(f'<path d="{path(poly)}" fill="{LAND}" stroke="{STROKE}" stroke-width="1.2" stroke-linejoin="round"/>')

# draw leaders first (under pins), then pins, then labels
for nm,x,y,off in projpts:
    px,py=T(x,y); lblx,lbly,anc,ex,ey=LAB[nm][1:]
    svg.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{ex}" y2="{ey}" stroke="{LEAD}" stroke-width="1.2"/>')
for nm,x,y,off in projpts:
    px,py=T(x,y)
    if off:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="14" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#fff"/>')
    else:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="none" stroke="{ORANGE}" stroke-opacity=".22" stroke-width="7"/><circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{ORANGE}"/>')
for nm,x,y,off in projpts:
    lblx,lbly,anc,ex,ey=LAB[nm][1:]
    col="#fff" if off else TXT; fw="700" if off else "600"
    svg.append(f'<text x="{lblx}" y="{lbly}" fill="{col}" font-size="21" font-weight="{fw}" text-anchor="{anc}">{nm}</text>')

svg.append(f'<text x="70" y="70" fill="#fff" font-size="30" font-weight="800">География поставок</text>')
svg.append(f'<text x="70" y="102" fill="#B9B2AA" font-size="18">8 регионов · офис в Барнауле</text>')
lgx,lgy=1180,60
svg.append(f'<circle cx="{lgx}" cy="{lgy}" r="8" fill="{ORANGE}"/><text x="{lgx+18}" y="{lgy+6}" fill="{TXT}" font-size="19">регионы поставок</text>')
svg.append(f'<circle cx="{lgx}" cy="{lgy+34}" r="9" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="{lgx}" cy="{lgy+34}" r="4" fill="#fff"/><text x="{lgx+18}" y="{lgy+40}" fill="{TXT}" font-size="19">офис · Барнаул</text>')
svg.append('</svg>')
open("map_ref.svg","w").write("\n".join(svg))
print("ok")
