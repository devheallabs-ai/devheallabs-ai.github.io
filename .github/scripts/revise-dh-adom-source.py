"""One-time editorial migration from the supplied publication to edition 1.1."""
from pathlib import Path
import json, shutil, re
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

root=Path(__file__).resolve().parents[2]
old=root/'.github/dh-adom/source'; src=root/'dh-adom/source'
if not old.exists():
    print('Source migration already completed; use the document and website builders for updates.')
    raise SystemExit(0)
archive=root/'.github/dh-adom/originals'; archive.mkdir(exist_ok=True)
if old.exists():
    assert old.resolve().is_relative_to(root.resolve()) and src.resolve().is_relative_to(root.resolve())
    shutil.move(str(old),str(src))
papers=src/'01-White-Paper'
for p in list(papers.iterdir()):
    if p.suffix in ('.pdf','.docx'): shutil.move(str(p),str(archive/p.name))
original=archive/'DH-ADOM_White_Paper_v1.1-illustrated.docx'
def clean(s):
    return s.replace('devheallabs.in','devheallabs.com').replace('16. Reference Architecture for DevHeal Autonomous Twin','16. Reference Architecture for DH-ADOM Adoption').replace('Construct a representative Autonomous Twin feature request set across small, medium, and cross-domain tasks.','Construct a representative software-engineering task corpus covering isolated feature work, cross-domain changes, maintenance, security changes, refactoring, and release tasks.').replace('White Paper v1.0','White Paper v1.1').replace('The DH-ADOM v1.0 release','The DH-ADOM publication package 1.1.0')
doc=Document(original); blocks=[]; started=False; appendix=False; image=0
figures={26:'01-dh-adom-hierarchy',47:'01-dh-adom-hierarchy',68:'02-lifecycle-integration',89:'07-traceability',102:'08-reference-architecture'}
index=-1
for el in doc.element.body:
    if el.tag.endswith('}p'):
        index+=1; p=Paragraph(el,doc); text=clean(p.text)
        if text=='Publication Note': started=True
        if not started: continue
        if text.startswith('Appendix A'): appendix=True
        if text.startswith('Appendix B'): appendix=False
        if p._p.xpath('.//a:blip'): continue
        if appendix and text.startswith('Figure A'):
            n=int(re.match(r'Figure A(\d+)',text).group(1))-1
            names=['01-dh-adom-hierarchy','02-lifecycle-integration','03-delegation-sequence','04-agent-state-machine','05-ownership-boundaries','06-security-delegation-controls','07-traceability','08-reference-architecture']
            blocks.append({'type':'figure','name':names[n],'caption':text}); continue
        if not text.strip(): continue
        kind={'Heading 1':'h2','Heading 2':'h3','Code DH':'code','List Bullet':'bullet'}.get(p.style.name,'p')
        if index in figures:
            blocks.append({'type':'figure','name':figures[index],'caption':'DH-ADOM '+figures[index][3:].replace('-',' ')+'. Editorial diagram, revised for clarity.'})
            # Preserve detailed lifecycle/traceability chains as readable text as well.
            if index in (26,68,89): blocks.append({'type':'p','text':' '.join(text.split())})
        else: blocks.append({'type':kind,'text':text})
    elif el.tag.endswith('}tbl') and started:
        table=Table(el,doc); blocks.append({'type':'table','rows':[[clean(c.text) for c in row.cells] for row in table.rows]})
blocks.insert(0,{'type':'p','text':'Edition 1.1 · 7 October 2026. Editorial revision: generic adoption examples, canonical .com links, readable vector figures and refreshed layout. The model and normative specification remain version 1.0. No new empirical results are asserted.'})
content={'title':'DH-ADOM','subtitle':'DevHeal Hierarchical Agent Development & Orchestration Model','version':'1.1','date':'2026-10-07','author':'Sai Narender Nuckala','blocks':blocks}
(papers/'paper.json').write_text(json.dumps(content,ensure_ascii=False,indent=2),encoding='utf-8')
lines=[]
for b in blocks:
    if b['type']=='table': lines.extend(' | '.join(r) for r in b['rows'])
    elif b['type']=='figure': lines.append('Figure: '+b['caption'])
    else: lines.append(('# ' if b['type']=='h2' else '## ' if b['type']=='h3' else '')+b['text'])
(papers/'DH-ADOM_White_Paper_v1.1.md').write_text('\n\n'.join(lines),encoding='utf-8')
# Canonical URLs in current source metadata; archived 1.0 downloads stay immutable.
for p in src.rglob('*'):
    if p.is_file() and p.suffix in ('.md','.json','.yaml','.bib','.cff','.html','.txt'):
        s=p.read_text(encoding='utf-8'); t=s.replace('devheallabs.in','devheallabs.com')
        if t!=s: p.write_text(t,encoding='utf-8')
for p in (src/'02-Specification/Schema-Definitions').glob('*.json'):
    data=json.loads(p.read_text()); data['$id']='https://devheallabs.com/dh-adom/source/02-Specification/Schema-Definitions/'+p.name
    p.write_text(json.dumps(data,indent=2),encoding='utf-8')
# Historical generated website and manifests belong to the source archive, not current pages.
for name in ('10-Website','PACKAGE-MANIFEST.json','reports'):
    p=src/name
    if p.exists(): shutil.move(str(p),str(archive/name))
spec=src/'02-Specification'
for p in list(spec.glob('*.pdf'))+list(spec.glob('*.docx')):
    shutil.move(str(p),str(archive/p.name))
print('Current publication source organized in dh-adom/source; original artifacts archived internally.')
