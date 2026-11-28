"""Build compositions/captions.html and compositions/verses.html from assets/words.json."""
import json,re,html
W=json.load(open('assets/words.json'))
VOICE_END=79.33
KEY={'téléphone','bruit','peur','peurs','nouvelles','paix','besoins','grâces','cœurs','pensées','confiance','respire','monde','cloche','bénisse','inquiétez','serré'}
def n(t): return re.sub(r"[^a-zàâçéèêëîïôûùüÿœ]","",t.lower())
words=[]
for t,s,e in W:
    s=min(s,VOICE_END-0.05);e=min(max(e,s+0.12),VOICE_END);words.append([t,s,e])
def find(tok,start=0):
    for i in range(start,len(words)):
        if n(words[i][0])==n(tok): return i
    raise SystemExit('missing '+tok)
# verse ranges (word indices), spoken quotations
v1a=find('Ne',find('Bible'));v1b=find('Jésus-Christ.')
v2a=find('Je',find('Jésus'));v2b=find('point.',v2a)
v3a=v3b=0
verse=set()
for a,b in ((v1a,v1b),(v2a,v2b)): verse|=set(range(a,b+1))
# groups: max 4 words, break at sentence end / pause / comma / verse boundary
groups=[];cur=[]
def flush():
    global cur
    if cur: groups.append(cur);cur=[]
for i,w in enumerate(words):
    if cur and ((i in verse)!=(cur[-1][3] in verse)): flush()
    cur.append(w+[i])
    nxt=words[i+1] if i+1<len(words) else None
    if re.search(r'[.?!:]$',w[0]) or (nxt and nxt[1]-w[2]>=0.25) or (w[0].endswith(',') and len(cur)>=2) or len(cur)>=4: flush()
flush()
merged=[]
for g in groups:
    if merged and len(g)==1 and not re.search(r'[.?!:]$',merged[-1][-1][0]) and len(merged[-1])<4 and (g[0][3] in verse)==(merged[-1][-1][3] in verse): merged[-1]+=g
    else: merged.append(g)
groups=merged
out=[];js=[]
for gi,g in enumerate(groups):
    start=max(0.1,g[0][1]-0.05)
    nxt=groups[gi+1][0][1]-0.05 if gi+1<len(groups) else VOICE_END+0.3
    end=max(min(g[-1][2]+0.3,nxt-0.02),start+0.5)
    isv=g[0][3] in verse
    spans=''.join(f'<span class="w{" k" if n(w[0]) in KEY else ""}" id="c{gi}w{wi}">{html.escape(w[0])}</span> ' for wi,w in enumerate(g)).strip()
    out.append(f'    <div id="cg{gi}" class="clip cg{" vs" if isv else ""}" data-start="{start:.2f}" data-duration="{round(end-start,2)}" data-track-index="1"><p>{spans}</p></div>')
    js.append({"id":gi,"start":round(start,2),"end":round(end,2),"w":[[round(w[1]-start,2),1 if n(w[0]) in KEY else 0] for w in g]})
cap='''<template>
  <style>
    #root { position:absolute; inset:0; font-family:"Montserrat",sans-serif; }
    .cg { position:absolute; left:120px; width:768px; top:600px; display:flex; justify-content:center; opacity:0; }
    .cg p { margin:0; text-align:center; font-weight:800; font-size:86px; line-height:1.14; color:#fff; letter-spacing:-0.01em;
      text-shadow:0 3px 20px rgba(0,0,0,.7),0 1px 3px rgba(0,0,0,.75); }
    .cg.vs p { font-family:"Playfair Display",serif; font-weight:700; font-size:80px; line-height:1.18; letter-spacing:0; }
    .w { display:inline-block; color:#fff; } .w.k { margin:0 .16em; }
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
'''+'\n'.join(out)+'''
  </div>
  <script>
    const G = '''+json.dumps(js)+''';
    const tl = gsap.timeline({ paused: true });
    G.forEach((g) => {
      const grp = "#cg" + g.id;
      tl.fromTo(grp, { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: 0.16, ease: "power2.out" }, g.start);
      g.w.forEach((t, i) => {
        const w = "#c" + g.id + "w" + i;
        tl.set(w, { color: "#fff", scale: 1 }, g.start);
        tl.to(w, { color: "#F6D58E", duration: 0.08 }, g.start + t[0]);
        if (t[1]) tl.fromTo(w, { scale: 1 }, { scale: 1.1, duration: 0.18, ease: "back.out(2.4)" }, g.start + t[0]);
      });
      tl.to(grp, { opacity: 0, duration: 0.12, ease: "power2.in" }, g.end - 0.12);
      tl.set(grp, { opacity: 0, visibility: "hidden" }, g.end);
    });
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open('compositions/captions.html','w',encoding='utf8').write(cap)
# verse reference chips, timed on the spoken reference
p=find('Philippiens');m=find('Jean')
chips=[('Philippiens 4:6-7',words[p][1]-0.2,3.8),('Jean 14:27',words[m][1]-0.2,3.8)]
body=''.join(f'    <div id="v{i+1}" class="clip chip" data-start="{s:.2f}" data-duration="{d}" data-track-index="1"><span>{t}</span></div>\n' for i,(t,s,d) in enumerate(chips))
js2=json.dumps([[f"#v{i+1}",round(s,2),d] for i,(t,s,d) in enumerate(chips)])
ver='''<template>
  <style>
    #root { position:absolute; inset:0; font-family:"Playfair Display",serif; }
    .chip { position:absolute; left:0; right:0; top:330px; display:flex; justify-content:center; opacity:0; }
    .chip span { padding:18px 44px; border-radius:60px; background:rgba(20,14,6,.62); border:2px solid rgba(246,213,142,.9);
      color:#F6D58E; font-size:56px; font-weight:700; letter-spacing:.02em; text-shadow:0 2px 10px rgba(0,0,0,.5); }
  </style>
  <div id="root" data-composition-id="verses" data-width="1080" data-height="1920">
'''+body+'''  </div>
  <script>
    const tl = gsap.timeline({ paused: true });
    '''+js2+'''.forEach(([id,s,d]) => {
      tl.fromTo(id, { opacity: 0, y: 24, scale: .94 }, { opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(1.7)" }, s);
      tl.to(id, { opacity: 0, duration: 0.3, ease: "power2.in" }, s + d - 0.3);
    });
    window.__timelines["verses"] = tl;
  </script>
</template>
'''
open('compositions/verses.html','w',encoding='utf8').write(ver)
json.dump({"chips":[[t,round(s,2),d] for t,s,d in chips]},open('assets/chips.json','w'))
print(len(groups),'groups',chips)
