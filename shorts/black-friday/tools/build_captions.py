"""Build compositions/captions.html from assets/words.json (script words + Whisper timings)."""
import json,re,html
W=json.load(open('assets/words.json'))
VOICE_END=73.7
words=[]
for t,s,e in W:
    s=min(s,VOICE_END-0.05);e=min(max(e,s+0.12),VOICE_END)
    words.append([t,s,e])
groups=[];cur=[]
def flush():
    global cur
    if cur: groups.append(cur);cur=[]
for i,w in enumerate(words):
    cur.append(w)
    end_sentence=bool(re.search(r'[.?!:]$',w[0]))
    nxt=words[i+1] if i+1<len(words) else None
    pause=nxt and nxt[1]-w[2]>=0.25
    comma=w[0].endswith(',') and len(cur)>=3
    if end_sentence or pause or comma or len(cur)>=5: flush()
flush()
# merge tiny groups (<2 words) into previous when same sentence
merged=[]
for g in groups:
    if merged and len(g)==1 and not re.search(r'[.?!:]$',merged[-1][-1][0]) and len(merged[-1])<5: merged[-1]+=g
    else: merged.append(g)
groups=merged
out=[];js=[]
for gi,g in enumerate(groups):
    start=max(0.1,g[0][1]-0.05)
    nxt=groups[gi+1][0][1]-0.05 if gi+1<len(groups) else VOICE_END+0.3
    end=min(g[-1][2]+0.3,nxt-0.02)
    end=max(end,start+0.5)
    dur=round(end-start,2)
    ws=''.join(f'<span class="w" id="c{gi}w{wi}">{html.escape(w[0])}</span> ' for wi,w in enumerate(g)).strip()
    out.append(f'    <div id="cg{gi}" class="clip cg" data-start="{start:.2f}" data-duration="{dur}" data-track-index="1"><p>{ws}</p></div>')
    js.append({"id":gi,"start":round(start,2),"end":round(end,2),"w":[[round(w[1]-start,2)] for w in g]})
html_out='''<template>
  <style>
    #root { position:absolute; inset:0; font-family:"Montserrat",sans-serif; }
    .cg { position:absolute; left:120px; width:660px; top:860px; display:flex; justify-content:center; opacity:0; }
    .cg p { margin:0; max-width:660px; text-align:center; font-weight:800; font-size:66px; line-height:1.18; color:#fff; letter-spacing:-0.01em;
      text-shadow:0 3px 18px rgba(0,0,0,.65),0 1px 3px rgba(0,0,0,.7); }
    .w { display:inline-block; color:#fff; }
  </style>
  <div id="root" data-composition-id="captions" data-width="1080" data-height="1920">
'''+'\n'.join(out)+'''
  </div>
  <script>
    const G = '''+json.dumps(js)+''';
    const tl = gsap.timeline({ paused: true });
    G.forEach((g) => {
      const grp = "#cg" + g.id, len = g.end - g.start;
      tl.fromTo(grp, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.18, ease: "power2.out" }, g.start);
      g.w.forEach((t, i) => {
        const w = "#c" + g.id + "w" + i;
        tl.set(w, { color: "#fff" }, g.start);
        tl.to(w, { color: "#F6D58E", duration: 0.08 }, g.start + t[0]);
      });
      tl.to(grp, { opacity: 0, duration: 0.12, ease: "power2.in" }, g.end - 0.12);
      tl.set(grp, { opacity: 0, visibility: "hidden" }, g.end);
    });
    window.__timelines["captions"] = tl;
  </script>
</template>
'''
open('compositions/captions.html','w',encoding='utf8').write(html_out)
print(len(groups),'groups')
