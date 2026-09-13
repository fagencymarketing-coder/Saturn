import json, math
D = json.load(open("regions.geojson"))

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

TARGETS = ["Ростовская область","Краснодарский край","Ставропольский край","Омская область",
           "Новосибирская область","Алтайский край","Красноярский край","Амурская область"]
LABEL = {"Ростовская область":"Ростовская обл.","Краснодарский край":"Краснодарский край",
         "Ставропольский край":"Ставропольский край","Омская область":"Омская обл.",
         "Новосибирская область":"Новосибирская обл.","Алтайский край":"Алтайский край · Барнаул",
         "Красноярский край":"Красноярский край","Амурская область":"Амурская обл."}
OFFICE = "Алтайский край"

def rings_of(geom):
    t=geom["type"]; cs=geom["coordinates"]
    return cs if t=="Polygon" else [ring for poly in cs for ring in poly]

def area_centroid(ring):  # projected ring -> (cx,cy,area)
    A=cx=cy=0.0
    for i in range(len(ring)-1):
        x0,y0=ring[i]; x1,y1=ring[i+1]
        cr=x0*y1-x1*y0; A+=cr; cx+=(x0+x1)*cr; cy+=(y0+y1)*cr
    if A==0: 
        xs=[p[0] for p in ring]; ys=[p[1] for p in ring]; return sum(xs)/len(xs),sum(ys)/len(ys),0
    A*=0.5; return cx/(6*A), cy/(6*A), abs(A)

all_regions=[]   # (name, [projected rings], is_target)
centroids={}     # name -> (cx,cy) projected
for f in D["features"]:
    nm=f["properties"].get("name")
    pr=[[proj(x,y) for x,y in ring] for ring in rings_of(f["geometry"])]
    is_t = nm in TARGETS
    all_regions.append((nm,pr,is_t))
    if is_t:
        best=max(pr,key=lambda rr:area_centroid(rr)[2]); cx,cy,_=area_centroid(best)
        centroids[nm]=(cx,cy)

W,H=1600,900; pad=70
xs=[p[0] for _,rr,_ in all_regions for ring in rr for p in ring]
ys=[p[1] for _,rr,_ in all_regions for ring in rr for p in ring]
minx,maxx,miny,maxy=min(xs),max(xs),min(ys),max(ys)
s=min((W-2*pad)/(maxx-minx),(H-2*pad)/(maxy-miny))
offx=(W-(maxx-minx)*s)/2; offy=(H-(maxy-miny)*s)/2
def T(x,y): return (offx+(x-minx)*s, offy+(maxy-y)*s)
def path(ring): return "".join(("M" if i==0 else "L")+f"{T(x,y)[0]:.1f} {T(x,y)[1]:.1f}" for i,(x,y) in enumerate(ring))+"Z"

# print pin px + %
print("PINS (px / %):")
PIN={}
for nm in TARGETS:
    px,py=T(*centroids[nm]); PIN[nm]=(px,py)
    print(f"  {nm:22s} {px:6.1f},{py:6.1f}   {px/W*100:4.1f} / {py/H*100:4.1f}")

# --- label layout (tuned to centroid pins; will adjust after first look) ---
LAB={
 "Ростовская область":   (232,505,"start"),
 "Краснодарский край":   (232,547,"start"),
 "Ставропольский край":  (232,589,"start"),
 "Омская область":       (470,690,"end"),
 "Новосибирская область":(690,600,"start"),
 "Алтайский край":       (560,780,"end"),
 "Красноярский край":    (900,470,"start"),
 "Амурская область":     (1200,720,"start"),
}

BG="#141210"; LAND="#211C18"; LANDS="rgba(255,255,255,.07)"
HIL="#3A2A20"; HILS="rgba(255,66,0,.55)"; ORANGE="#FF4200"; TXT="#F3F1EE"; LEAD="rgba(255,255,255,.35)"
svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Montserrat,Arial,sans-serif">']
svg.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
# base regions
for nm,rr,is_t in all_regions:
    if is_t: continue
    for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width="0.8" stroke-linejoin="round"/>')
# highlighted target regions (contour)
for nm,rr,is_t in all_regions:
    if not is_t: continue
    for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{HIL}" stroke="{HILS}" stroke-width="1.8" stroke-linejoin="round"/>')
# leaders
for nm in TARGETS:
    px,py=PIN[nm]; lx,ly,anc=LAB[nm]
    ex = lx-6 if anc=="start" else (lx+6 if anc=="end" else lx)
    svg.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{ex}" y2="{ly-5}" stroke="{LEAD}" stroke-width="1.2"/>')
# pins
for nm in TARGETS:
    px,py=PIN[nm]
    if nm==OFFICE:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="14" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="{px:.1f}" cy="{py:.1f}" r="5.5" fill="#fff"/>')
    else:
        svg.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="none" stroke="{ORANGE}" stroke-opacity=".22" stroke-width="7"/><circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{ORANGE}"/>')
# labels
for nm in TARGETS:
    lx,ly,anc=LAB[nm]; col="#fff" if nm==OFFICE else TXT; fw="700" if nm==OFFICE else "600"
    svg.append(f'<text x="{lx}" y="{ly}" fill="{col}" font-size="21" font-weight="{fw}" text-anchor="{anc}">{LABEL[nm]}</text>')
# title + legend
svg.append(f'<text x="70" y="70" fill="#fff" font-size="30" font-weight="800">География поставок</text>')
svg.append(f'<text x="70" y="102" fill="#B9B2AA" font-size="18">8 регионов · офис в Барнауле</text>')
lgx,lgy=1180,60
svg.append(f'<circle cx="{lgx}" cy="{lgy}" r="8" fill="{ORANGE}"/><text x="{lgx+18}" y="{lgy+6}" fill="{TXT}" font-size="19">регионы поставок</text>')
svg.append(f'<circle cx="{lgx}" cy="{lgy+34}" r="9" fill="none" stroke="#fff" stroke-width="2.5"/><circle cx="{lgx}" cy="{lgy+34}" r="4" fill="#fff"/><text x="{lgx+18}" y="{lgy+40}" fill="{TXT}" font-size="19">офис · Барнаул</text>')
svg.append('</svg>')
open("map_ref.svg","w").write("\n".join(svg))
print("wrote map_ref.svg")
