from pathlib import Path
p=Path('output/reference-style-build/author.mjs');s=p.read_text(encoding='utf8');s=s.replace("lines.forEach((t,i)=>label(s,n+'-line-'+i,t,x+24,y+77+i*32,w-48,21,light?'#333333':C.white,false,'left',31));}","lines.forEach((t,i)=>label(s,n+'-line-'+i,t,x+24,y+77+i*(lines.length>6?27:32),w-48,lines.length>6?20:21,light?'#333333':C.white,false,'left',lines.length>6?27:31));}")
s='\n'.join(l for l in s.splitlines() if not l.startswith('const lines=s.shapes.items.filter'))
s=s.replace("x+15,y+71,w-30,h-100,large?34:25","x+15,y+71,w-30,Math.max(h-100,45),w<250?18:large?34:25")
p.write_text(s,encoding='utf8')
