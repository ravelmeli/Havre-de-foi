import json,re,difflib,unicodedata
S="""Black Friday. Des promotions partout… et toi, tu as l'impression qu'il te manque tout. Écoute bien.
Dieu n'a pas attendu les soldes pour prendre soin de toi. Sa Parole dit : « Mon Dieu pourvoira à tous vos besoins selon sa richesse, avec gloire, en Jésus-Christ. » Philippiens 4:19.
Pas à tes envies du moment. À tes besoins. Et Lui connaît la différence mieux que toi. Il sait ce dont tu as besoin avant même que tu le demandes.
Jésus dit : « Regardez les oiseaux du ciel : ils ne sèment pas, ils ne moissonnent pas, et votre Père céleste les nourrit. N'avez-vous pas beaucoup plus de valeur qu'eux ? » Matthieu 6:26.
Prions ensemble. Père, je dépose devant toi la comparaison et la pression d'en avoir toujours plus. Je choisis la gratitude. Merci pour le toit, le pain, et ceux qui m'aiment. Là où je ressens un manque, je déclare ta provision. Tu es mon berger : je ne manquerai de rien. Au nom de Jésus, amen.
Si cette parole t'a touché, partage-la à quelqu'un qui en a besoin, abonne-toi et active la cloche. Que Dieu te bénisse."""
def norm(t):
    t=unicodedata.normalize('NFD',t.lower());t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    return re.sub(r"[^a-z0-9]","",t)
tw=json.load(open('assets/transcript.json'))
S=S.replace(" :",":")
sw=[t for t in re.sub(r"[«»]","",S).replace('…',' ').split() if t not in (':',)]
# keep punctuation attached; drop pure-punct tokens
sw=[t for t in sw if norm(t)]
a=[norm(w['text']) for w in tw]; b=[norm(t) for t in sw]
sm=difflib.SequenceMatcher(None,a,b,autojunk=False)
tm={}  # script idx -> transcript idx
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=='equal':
        for k in range(i2-i1): tm[j1+k]=i1+k
    elif tag in('replace',):
        n=min(i2-i1,j2-j1)
        for k in range(n): tm[j1+k]=i1+k
out=[]
n=len(sw)
# fill gaps by interpolation
known=sorted(tm)
for j in range(n):
    if j in tm:
        w=tw[tm[j]];out.append([sw[j],w['start'],w['end']]);continue
    p=max([k for k in known if k<j],default=None);q=min([k for k in known if k>j],default=None)
    if p is None: s=tw[0]['start'];e=tw[tm[q]]['start']
    elif q is None: s=tw[tm[p]]['end'];e=tw[-1]['end']
    else:
        s0=tw[tm[p]]['end'];e0=tw[tm[q]]['start'];s=s0+(e0-s0)*(j-p-1)/(q-p-1) if False else s0
        gap=[x for x in range(p+1,q)];m=len(gap);idx=gap.index(j)
        s=s0+(e0-s0)*idx/m;e=s0+(e0-s0)*(idx+1)/m
    out.append([sw[j],round(s,2),round(e,2)])
print(len(tw),len(sw),len(tm))
json.dump(out,open('assets/words.json','w'),ensure_ascii=False)
for i,(t,s,e) in enumerate(out):
    if re.search(r'[.?!:]$',t) or i==0: print(i,t,s,e)
