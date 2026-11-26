"""Build index.html: shot list synced to the voice, hook, sfx, audio."""
import json
chips=json.load(open('assets/chips.json'))['chips']
X=0.25  # crossfade
# (file, media_start, start, end, object-position)
SHOTS=[
 ('s_1_wheat_sunrise',0,0,4.2,'50% 50%'),
 ('s_5_clouds',0,4.2,8.0,'50% 50%'),
 ('n_sunrays',0,8.0,12.3,'35% 50%'),
 ('s_2_wheat_sunset',0,12.3,16.8,'50% 50%'),
 ('s_6_golden_sky',0,16.8,20.6,'50% 50%'),
 ('n_hand_wheat',0,20.6,25.0,'85% 50%'),
 ('s_3_wheat_gold',0,25.0,30.4,'50% 50%'),
 ('s_4_birds',0,30.4,35.4,'50% 50%'),
 ('s_4_birds',7,35.4,40.0,'50% 50%'),
 ('n_river',0,40.0,44.4,'50% 50%'),
 ('s_6_golden_sky',6,44.4,49.6,'50% 50%'),
 ('n_family_pray',0,49.6,52.7,'78% 50%'),
 ('n_house',0,52.7,53.9,'72% 50%'),
 ('n_bread',0,53.9,55.0,'50% 50%'),
 ('n_family_sil',0,55.0,58.7,'42% 50%'),
 ('n_sheep',0,58.7,63.0,'25% 50%'),
 ('s_5_clouds',8,63.0,66.4,'50% 50%'),
 ('s_7_sun_rise',0.8,66.4,80.0,'50% 50%'),
]
vids=[];js=[];slots=[]
for i,(f,m,s,e,pos) in enumerate(SHOTS):
    st=max(0,s-X);last=i==len(SHOTS)-1
    d=round(e-st,2)
    vids.append(f'      <video id="b{i+1}" class="clip bg" src="assets/{f}.mp4" style="object-position:{pos}" muted playsinline data-start="{st:.2f}" data-media-start="{m}" data-duration="{d}" data-track-index="0"></video>')
    slots.append([f"#b{i+1}",round(st,2),d,i%2])
sfx=[('sfx_whoosh',0.0,0.55),('sfx_pop',2.55,0.5)]+[('sfx_chime',round(s+0.05,2),0.5) for t,s,d in chips]+[('sfx_click',68.4,0.7),('sfx_click',70.0,0.7),('sfx_bell',72.2,0.55)]
DUR={'sfx_whoosh':0.9,'sfx_pop':0.25,'sfx_chime':1.6,'sfx_click':0.2,'sfx_bell':1.2}
auds=[]
for i,(f,s,v) in enumerate(sfx):
    auds.append(f'      <audio id="sx{i+1}" src="assets/{f}.wav" data-start="{s}" data-duration="{DUR[f]}" data-track-index="10" data-volume="{v}"></audio>')
html=f'''<!doctype html>
<html lang="fr" data-composition-variables='[{{"id":"hook1","type":"string","label":"Accroche 1 (0-2,6 s)","default":"TOUT TE MANQUE ?"}},{{"id":"hook2","type":"string","label":"Accroche 2 (2,6-4,8 s)","default":"DIEU POURVOIT"}},{{"id":"watermark","type":"string","label":"Filigrane","default":"HAVRE DE FOI"}}]'>
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
    <div id="root" data-composition-id="main" data-start="0" data-duration="80" data-width="1080" data-height="1920">
{chr(10).join(vids)}
      <div id="scrim" class="clip" data-start="0" data-duration="80" data-track-index="1"></div>

      <div id="hook1" class="clip hook" data-start="0" data-duration="2.9" data-track-index="2"><span data-var-text="hook1">TOUT TE MANQUE ?</span></div>
      <div id="hook2" class="clip hook" data-start="2.5" data-duration="2.4" data-track-index="2"><span data-var-text="hook2">DIEU POURVOIT</span></div>

      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="80" data-track-index="3" data-track-kind="captions" data-width="1080" data-height="1920"></div>
      <div id="verses" data-composition-id="verses" data-composition-src="compositions/verses.html" data-start="0" data-duration="80" data-track-index="4" data-track-kind="graphics" data-width="1080" data-height="1920"></div>
      <div id="subscribe" data-composition-id="subscribe" data-composition-src="compositions/subscribe.html" data-start="66.0" data-duration="14" data-track-index="5" data-track-kind="graphics" data-width="1080" data-height="1920"></div>

      <img id="logo" class="clip" src="assets/logo.png" data-start="0" data-duration="80" data-track-index="6" />
      <div id="wm" class="clip" data-layout-allow-safe-zone data-start="0" data-duration="80" data-track-index="7"><span data-var-text="watermark">HAVRE DE FOI</span></div>

      <audio id="voice" src="assets/voice.wav" data-start="0" data-duration="73.7" data-track-index="8" data-volume="1"></audio>
      <audio id="music" src="assets/music_ducked.wav" data-start="0" data-duration="80" data-track-index="9" data-volume="1" data-fade-in="1.2" data-fade-out="3"></audio>
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
