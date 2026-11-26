"""Build index.html: shot list synced to the voice, hook, sfx, audio."""
import json
chips=json.load(open('assets/chips.json'))['chips']
X=0.25  # crossfade
# (file, media_start, start, end, object-position)
SHOTS=[  # (source id, source offset s, start, end, object-position)
 (20311,2,0,4.0,'50% 50%'),(22729,0,4.0,8.4,'50% 50%'),(1704,0,8.4,11.1,'50% 50%'),(4148,0,11.1,14.7,'50% 50%'),
 (2120,0,14.7,18.2,'50% 50%'),(21168,0,18.2,21.7,'50% 50%'),(17426,0,21.7,25.8,'50% 50%'),(25145,0,25.8,29.2,'15% 50%'),
 (42734,0,29.2,34.5,'50% 40%'),(29425,0,34.5,37.9,'50% 50%'),(4695,0,37.9,42.0,'50% 50%'),(4113,0,42.0,47.8,'40% 50%'),
 (4148,8,47.8,51.1,'50% 50%'),(6925,0,51.1,55.5,'50% 50%'),(32523,0,55.5,60.4,'50% 50%'),(1704,4,60.4,64.7,'50% 50%'),
 (7266,0,64.7,68.8,'50% 50%'),(21168,6,68.8,72.2,'50% 50%'),(20425,0,72.2,82.0,'50% 50%'),
]
import subprocess,os
RAW='/tmp/claude-0/-home-user-Havre-de-foi/dd6ab83a-30e0-5337-9da2-de387bfbbc38/scratchpad/raw3'
vids=[];js=[];slots=[]
for i,(f,m,s,e,pos) in enumerate(SHOTS):
    st=max(0,s-X);last=i==len(SHOTS)-1
    d=round(e-st,2)
    fn=f'p{i+1:02d}_{f}'
    if not os.path.exists(f'assets/{fn}.mp4'): subprocess.run(['ffmpeg','-v','error','-ss',str(m),'-t',str(d+0.3),'-i',f'{RAW}/{f}.mp4','-an','-c:v','libx264','-crf','19','-preset','fast','-pix_fmt','yuv420p','-r','30',f'assets/{fn}.mp4','-y'],check=True)
    m=0
    f=fn
    vids.append(f'      <video id="b{i+1}" class="clip bg" src="assets/{f}.mp4" style="object-position:{pos}" muted playsinline data-start="{st:.2f}" data-media-start="{m}" data-duration="{d}" data-track-index="0"></video>')
    slots.append([f"#b{i+1}",round(st,2),d,i%2])
sfx=[('sfx_whoosh',0.0,0.55),('sfx_pop',2.55,0.5)]+[('sfx_chime',round(s+0.05,2),0.5) for t,s,d in chips]+[('sfx_click',74.6,0.7),('sfx_click',76.2,0.7),('sfx_bell',78.4,0.55)]
DUR={'sfx_whoosh':0.9,'sfx_pop':0.25,'sfx_chime':1.6,'sfx_click':0.2,'sfx_bell':1.2}
auds=[]
for i,(f,s,v) in enumerate(sfx):
    auds.append(f'      <audio id="sx{i+1}" src="assets/{f}.wav" data-start="{s}" data-duration="{DUR[f]}" data-track-index="10" data-volume="{v}"></audio>')
html=f'''<!doctype html>
<html lang="fr" data-composition-variables='[{{"id":"hook1","type":"string","label":"Accroche 1 (0-2,6 s)","default":"PAS DE RÉPONSE ?"}},{{"id":"hook2","type":"string","label":"Accroche 2 (2,6-4,8 s)","default":"IL T’A ENTENDU"}},{{"id":"watermark","type":"string","label":"Filigrane","default":"HAVRE DE FOI"}}]'>
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:1080px; height:1920px; overflow:hidden; background:#1a1208; }}
      #root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:"Montserrat",sans-serif; }}
      .bg {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
      #scrim {{ position:absolute; inset:0; background:linear-gradient(to bottom,rgba(0,0,0,.3) 0%,rgba(0,0,0,.12) 22%,rgba(0,0,0,.4) 40%,rgba(0,0,0,.5) 55%,rgba(0,0,0,.28) 75%,rgba(0,0,0,.3) 100%); }}
      #logo {{ position:absolute; left:40px; top:70px; width:170px; height:170px; object-fit:contain; }}
      #wm {{ position:absolute; left:0; right:0; top:1370px; text-align:center; font-weight:600; font-size:64px; letter-spacing:.08em; color:rgba(255,255,255,.6); text-shadow:0 2px 12px rgba(0,0,0,.5); }}
      .hook {{ position:absolute; left:120px; width:768px; top:300px; text-align:center; font-weight:900; font-size:92px; line-height:1.1; color:#fff; text-shadow:0 4px 26px rgba(0,0,0,.65); }}
      #hook2 {{ color:#F6D58E; opacity:0; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="82" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="scrim" class="clip" data-start="0" data-duration="82" data-track-index="1"></div>

      <div id="hook1" class="clip hook" data-start="0" data-duration="2.9" data-track-index="2"><span data-var-text="hook1">PAS DE RÉPONSE ?</span></div>
      <div id="hook2" class="clip hook" data-start="2.5" data-duration="2.4" data-track-index="2"><span data-var-text="hook2">IL T’A ENTENDU</span></div>

      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="82" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      <div id="verses" data-composition-id="verses" data-composition-src="compositions/verses.html" data-start="0" data-duration="82" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="subscribe" data-composition-id="subscribe" data-composition-src="compositions/subscribe.html" data-start="72.2" data-duration="9.8" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920"></div>

      <img id="logo" class="clip" src="assets/logo.png" data-start="0" data-duration="82" data-track-index="6" />
      <div id="wm" class="clip" data-layout-allow-safe-zone data-start="0" data-duration="82" data-track-index="7"><span data-var-text="watermark">HAVRE DE FOI</span></div>

      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="80.57" data-track-index="8" data-volume="1"></audio>
      <audio id="music" src="assets/music_ducked.wav" data-start="0" data-duration="82" data-track-index="9" data-volume="1" data-fade-in="1.2" data-fade-out="3"></audio>
{chr(10).join(auds)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      const slots = {json.dumps(slots)};
      slots.forEach(([id,s,d,dir],i) => {{
        tl.fromTo(id, {{ scale: dir ? 1.14 : 1.0 }}, {{ scale: dir ? 1.0 : 1.14 }}, {{ duration: d, ease: "none" }}, s);
        if (i > 0) tl.fromTo(id, {{ opacity: 0 }}, {{ opacity: 1, duration: {X}, ease: "none" }}, s);
        if (i < slots.length - 1) tl.to(id, {{ opacity: 0, duration: {X}, ease: "none" }}, s + d - {X});
      }});
      tl.fromTo("#hook1", {{ scale: 1.12 }}, {{ scale: 1, duration: 0.35, ease: "power3.out" }}, 0);
      tl.to("#hook1", {{ opacity: 0, y: -24, duration: 0.3, ease: "power2.in" }}, 2.55);
      tl.fromTo("#hook2", {{ opacity: 0, scale: 0.8 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, 2.55);
      tl.to("#hook2", {{ opacity: 0, y: -20, duration: 0.3, ease: "power2.in" }}, 4.6);
      tl.fromTo("#logo", {{ opacity: 0 }}, {{ opacity: 0.95, duration: 0.6 }}, 0.2);
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
'''
open('index.html','w',encoding='utf8').write(html)
print(len(SHOTS),'shots')
