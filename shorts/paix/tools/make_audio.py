"""Synthesize soft SFX and build the voice-ducked music bed (assets/music_ducked.wav)."""
import numpy as np, wave, subprocess
SR=44100
def save(name,x):
    x=np.clip(x,-1,1);w=wave.open(f'assets/{name}.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(SR)
    w.writeframes((x*32767).astype('<i2').tobytes());w.close()
def t(d): return np.arange(int(SR*d))/SR
rng=np.random.default_rng(7)
# soft chime: two bell partials, long decay
x=t(1.6);c=sum(a*np.sin(2*np.pi*f*x)*np.exp(-x*k) for f,a,k in [(1318.5,.5,3.2),(1975.5,.28,4.0),(2637,.12,5.5)])
c*=np.minimum(1,x/0.005);save('sfx_chime',c*0.55)
# whoosh: filtered noise swell
x=t(0.9);n=rng.standard_normal(len(x));k=np.ones(60)/60;n=np.convolve(n,k,'same')-np.convolve(n,np.ones(600)/600,'same')
env=np.sin(np.pi*np.clip(x/0.9,0,1))**2;save('sfx_whoosh',n*env*2.2)
# pop: short low sine blip
x=t(0.25);p=np.sin(2*np.pi*(520-380*x/0.25*0.5)*x)*np.exp(-x*22);save('sfx_pop',p*0.6)
# click: tiny noise tick + thud
x=t(0.2);cl=rng.standard_normal(len(x))*np.exp(-x*160)*0.35+np.sin(2*np.pi*180*x)*np.exp(-x*40)*0.5;save('sfx_click',cl)
# bell ding (notification-like)
x=t(1.2);b=sum(a*np.sin(2*np.pi*f*x)*np.exp(-x*k) for f,a,k in [(1568,.5,4),(2093,.35,5),(3136,.15,7)]);save('sfx_bell',b*np.minimum(1,x/0.003)*0.5)
# ducked music: key = voice
subprocess.run(['ffmpeg','-v','error','-y','-i','assets/music.mp3','-i','assets/voice.wav','-filter_complex',
 '[0:a]atrim=0:81,asetpts=PTS-STARTPTS,aformat=sample_rates=44100:channel_layouts=stereo,volume=0.50[m];'
 '[1:a]aformat=sample_rates=44100:channel_layouts=stereo,apad=whole_dur=81[v1];'
 '[m][v1]sidechaincompress=threshold=0.015:ratio=9:attack=25:release=800:makeup=1[d]',
 '-map','[d]','-t','81','assets/music_ducked.wav'],check=True)
print('ok')
