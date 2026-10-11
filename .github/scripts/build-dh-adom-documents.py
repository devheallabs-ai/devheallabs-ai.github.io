"""Build vector figures and print PDFs from the shared publication source."""
from pathlib import Path
import html,json,re,textwrap
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Flowable,KeepTogether
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import HexColor,white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT

ROOT=Path(__file__).resolve().parents[2]; SRC=ROOT/'dh-adom/source'; ART=ROOT/'dh-adom/assets'; OUT=ROOT/'dh-adom/releases/1.1.1'
OUT.mkdir(parents=True,exist_ok=True)
NAVY='#12305e'; BLUE='#1552b8'; INK='#111120'; MUTED='#53536a'
figures={
'01-dh-adom-hierarchy':('Governance and ownership',[
 ('Engineering constitution','Rules and precedence'),('AI-SDLC and ADLC','Software and agent lifecycle governance'),('Root agent','Planning, routing and cross-domain review'),('Feature A   |   Feature B   |   Feature C','Persistent owners of separate domains'),('Task-scoped specialists','Bounded work under each feature owner'),('Validation and handoff','Evidence returns to Feature and Root review')], 'Parallel feature owners share governance, not authority.'),
'02-lifecycle-integration':('Lifecycle integration',[
 ('Intent and requirements','Define the engineering outcome'),('Architecture, design and tasks','Translate intent into owned work'),('Implementation','Execute with scoped agents and tools'),('Validation, evaluation and security','Collect evidence against acceptance criteria'),('Certification and release','Internal approval gates before delivery'),('Production feedback','Inform the next intent and requirements cycle')], 'ADLC governs agents throughout the software lifecycle.'),
'03-delegation-sequence':('Delegation and return flow',[
 ('1  User to Root','Submit the engineering request'),('2  Root to Feature','Route and authorize the owned task'),('3  Feature to Specialist','Delegate scope, budget and permissions'),('4  Specialist to Validation','Execute work and produce checkable outputs'),('5  Validation to Evidence','Record checks, changes and remaining risks'),('6  Specialist to Feature','Return task evidence and handoff'),('7  Feature to Root','Review and submit the feature handoff'),('8  Root to User','Integrate and report the outcome')], 'Completion depends on validation and acceptance.'),
'04-agent-state-machine':('Agent lifecycle states',[
 ('PROPOSED to DESIGNED','Define intent, ownership and contract'),('DESIGNED to REGISTERED','Record a distinct agent identity'),('REGISTERED to VALIDATED','Evaluate capabilities and constraints'),('VALIDATED to CERTIFIED to ACTIVE','Internal approval followed by activation'),('ACTIVE to SUSPENDED','Pause execution for review'),('SUSPENDED to REVALIDATION to ACTIVE','Recheck the agent before resuming'),('ACTIVE to DEPRECATED to RETIRED','Withdraw and retire the agent'),('SUSPENDED to RETIRED','Terminate without resuming execution')], 'Transitions follow the supplied agent lifecycle model.'),
'05-ownership-boundaries':('Feature ownership boundaries',[
 ('Root coordinator','Routes and coordinates work across domains'),('Feature A owns features/a/**','Changes remain within the declared boundary'),('Feature B owns features/b/**','A separate owner governs this domain'),('Cross-feature change','Coordinate through Root and affected owners'),('Review and traceability','Record approvals, changes and handoffs')], 'Feature A and B are peers, not a delegation chain.'),
'06-security-delegation-controls':('Checks before side effects',[
 ('Agent identity','Establish who is requesting the action'),('Delegation contract','Identify the task and delegated authority'),('Policy evaluation','Check applicable governance constraints'),('Authorization','Decide whether the action is allowed'),('Budget enforcement','Check remaining execution limits'),('Side-effect control','Mediate writes and external actions'),('Tool or target','Execute only the authorized operation')], 'Host integrations must enforce these design controls.'),
'07-traceability':('Intent to production evidence',[
 ('Intent and requirement','State what must be achieved'),('Feature and agent','Identify accountable ownership'),('Task and delegated specialist','Record the approved work boundary'),('Implementation and tests','Connect code changes to validation'),('Evaluation and evidence','Preserve results and acceptance checks'),('Feature handoff and Root review','Review before integration'),('Certification and release','Record internal approvals and delivery'),('Production outcome','Link observed outcomes back to intent')], 'Certification here means an internal engineering gate.'),
'08-reference-architecture':('A DH-ADOM adoption architecture',[
 ('User or engineer','Defines intent and acceptance criteria'),('Root orchestrator','Coordinates routing and integration'),('Feature A   |   Feature B   |   Feature C','Parallel engineering ownership domains'),('Scoped specialists','Execute delegated tasks for feature owners'),('Validation and evidence','Shared checks and auditable outputs'),('Root review and integration','Accept reviewed changes'),('Release','Deliver with traceable approvals')], 'Registry, policy and audit services support all roles.')}

def svg(name,title,steps,note):
    h=110+len(steps)*96+55; peer=name in ('05-ownership-boundaries','04-agent-state-machine')
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{h}" viewBox="0 0 600 {h}" role="img" aria-labelledby="title description"><title id="title">{html.escape(title)}</title><desc id="description">{html.escape(". ".join(a+": "+b for a,b in steps)+". "+note)}</desc><rect width="600" height="{h}" rx="22" fill="#f6f7fb"/><text x="28" y="34" font-family="Arial,sans-serif" font-size="15" fill="{BLUE}" letter-spacing="2">DH-ADOM / ENGINEERING MODEL</text><text x="28" y="76" font-family="Arial,sans-serif" font-size="27" font-weight="700" fill="{NAVY}">{html.escape(title)}</text>']
    for i,(a,b) in enumerate(steps):
        y=108+i*96
        if i and not peer: parts.append(f'<path d="M300 {y-24}V{y-6}m-5 -5l5 5 5 -5" fill="none" stroke="#2b90ff" stroke-width="2"/>')
        fill=NAVY if i==0 else '#ffffff'; fg='#ffffff' if i==0 else NAVY; sub='#dceaff' if i==0 else MUTED
        parts.append(f'<rect x="24" y="{y}" width="552" height="72" rx="12" fill="{fill}" stroke="#d8e2f1"/><text x="42" y="{y+29}" font-family="Arial,sans-serif" font-size="21" font-weight="700" fill="{fg}">{html.escape(a)}</text><text x="42" y="{y+55}" font-family="Arial,sans-serif" font-size="18" fill="{sub}">{html.escape(b)}</text>')
    parts.append(f'<text x="28" y="{h-24}" font-family="Arial,sans-serif" font-size="16" fill="{MUTED}">{html.escape(note)}</text></svg>')
    (ART/(name+'.svg')).write_text(''.join(parts),encoding='utf-8')
    (SRC/'07-Architecture-Diagrams/svg'/ (name+'.svg')).write_text(''.join(parts),encoding='utf-8')
for name,(title,steps,note) in figures.items(): svg(name,title,steps,note)
(ART/'figures.json').write_text(json.dumps(figures,indent=2),encoding='utf-8')

for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf'),('Italic','ariali.ttf'),('Mono','consola.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(Path('C:/Windows/Fonts')/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
styles=getSampleStyleSheet()
for name in ['Normal','BodyText']: styles[name].fontName='Body';styles[name].fontSize=10.5;styles[name].leading=15;styles[name].spaceAfter=8
for name,size in [('Heading1',20),('Heading2',14)]:
    styles[name].fontName='Bold';styles[name].fontSize=size;styles[name].leading=size*1.25;styles[name].textColor=HexColor(NAVY);styles[name].spaceBefore=18;styles[name].spaceAfter=10
    styles[name].keepWithNext=True
styles.add(ParagraphStyle('Small',fontName='Body',fontSize=8.5,leading=12,textColor=HexColor(MUTED),spaceAfter=8))
styles.add(ParagraphStyle('CodeBlock',fontName='Mono',fontSize=9,leading=13,backColor=HexColor('#f3f6fa'),borderPadding=10,spaceBefore=8,spaceAfter=14))
styles.add(ParagraphStyle('Cell',fontName='Body',fontSize=9,leading=13,spaceAfter=0))
styles.add(ParagraphStyle('CellHead',parent=styles['Cell'],fontName='Bold',textColor=white))
styles.add(ParagraphStyle('Cover',fontName='Bold',fontSize=46,leading=52,textColor=HexColor(NAVY),spaceAfter=24))

def text(s):
    # Arial handles math arrows; keep dashes ASCII for portable publication text.
    s=s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    for a,b in {'∪':' union ','⊆':' subset-of ','≤':'<=','→':' -> ','↓':' -> '}.items():s=s.replace(a,b)
    return html.escape(s)
def para(s,style='Normal'): return Paragraph(text(s),styles[style])
class VectorFigure(Flowable):
    def __init__(self,name):
        super().__init__();self.name=name
        title,steps,note=figures[name];self.nativeH=110+len(steps)*96+55
        self.scale=min(480/600,520/self.nativeH);self.width=600*self.scale;self.height=self.nativeH*self.scale
    def draw(self):
        c=self.canv;c.saveState();c.scale(self.scale,self.scale)
        title,steps,note=figures[self.name];h=self.nativeH
        c.setFillColor(HexColor('#f6f7fb'));c.roundRect(0,0,600,h,18,stroke=0,fill=1)
        c.setFillColor(HexColor(BLUE));c.setFont('Bold',14);c.drawString(28,h-34,'DH-ADOM / ENGINEERING MODEL')
        c.setFillColor(HexColor(NAVY));c.setFont('Bold',25);c.drawString(28,h-76,title)
        for i,(a,b) in enumerate(steps):
            y=h-108-i*96
            if i and self.name not in ('05-ownership-boundaries','04-agent-state-machine'):
                c.setStrokeColor(HexColor('#2b90ff'));c.setLineWidth(2);c.line(300,y+24,300,y+6);c.line(295,y+11,300,y+6);c.line(305,y+11,300,y+6)
            c.setFillColor(HexColor(NAVY if i==0 else '#ffffff'));c.setStrokeColor(HexColor('#d8e2f1'));c.roundRect(24,y-72,552,72,12,stroke=1,fill=1)
            c.setFillColor(white if i==0 else HexColor(NAVY));c.setFont('Bold',21);c.drawString(42,y-29,a)
            c.setFillColor(HexColor('#dceaff' if i==0 else MUTED));c.setFont('Body',18);c.drawString(42,y-55,b)
        c.setFillColor(HexColor(MUTED));c.setFont('Body',16);c.drawString(28,24,note);c.restoreState()

class PaperDoc(SimpleDocTemplate):
    def afterFlowable(self,f):
        if isinstance(f,Paragraph) and f.style.name=='Heading1':
            key='section-'+str(self.seq.nextf('section'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,0,False)
def furniture(c,d):
    if d.page==1:return
    c.saveState();c.setStrokeColor(HexColor('#d8e2f1'));c.line(54,752,558,752);c.setFillColor(HexColor(MUTED));c.setFont('Body',8)
    c.drawString(54,763,'DEVHEAL LABS AI / DH-ADOM');c.drawRightString(558,763,d.publication)
    c.drawString(54,30,'devheallabs.com/dh-adom/');c.drawRightString(558,30,str(d.page));c.restoreState()
def table(rows):
    cols=len(rows[0]); widths=([64,366,74] if rows[0][0]=='ID' else [96,408] if cols==2 else [104,190,210] if cols==3 else [504/cols]*cols)
    t=Table([[para(s,'CellHead' if i==0 else 'Cell') for s in row] for i,row in enumerate(rows)],colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor(NAVY)),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#f4f7fb')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,0),(-1,0),.6,HexColor(BLUE))]));return t
def build(path,title,subtitle,version,blocks):
    story=[Spacer(1,72),para('DEVHEAL LABS AI','Small'),Spacer(1,30),para(title,'Cover'),para(subtitle,'Heading1'),Spacer(1,25),para(version),para('Sai Narender Nuckala / DevHeal Labs AI'),Spacer(1,30),para('An engineering operating model for repository ownership, bounded delegation and evidence-backed handoffs.'),para('Canonical publication: https://devheallabs.com/dh-adom/','Small'),Spacer(1,18),para('Copyright (c) 2026 DevHeal Labs AI Pvt. Ltd. Publication prose and diagrams: Creative Commons Attribution 4.0 International (CC BY 4.0). https://creativecommons.org/licenses/by/4.0/','Small'),para('Embedded code examples: Apache-2.0. Names and logos excluded. Full scope: https://devheallabs.com/dh-adom/licensing/ - licensing release 1.1.1.','Small'),PageBreak()]
    appendix=False;references=False
    for b in blocks:
        kind=b['type']
        if kind=='figure':
            if not appendix:
                number=int(b['name'][:2]);story.append(para(f'See Figure A{number} in Appendix A for the vector diagram.','Small'));continue
            if not (isinstance(story[-1],Paragraph) and story[-1].getPlainText().startswith('Appendix A')):story.append(PageBreak())
            story.extend([para(b['caption'],'Heading2'),VectorFigure(b['name'])]);continue
        if kind=='table':story.extend([table(b['rows']),Spacer(1,12)]);continue
        s=b['text']
        if kind=='h2':
            references=s=='References'
            if s.startswith('Appendix A'):appendix=True;story.append(PageBreak())
            if s.startswith('Appendix B'):appendix=False
            story.append(para(s,'Heading1'))
        elif kind=='h3':story.append(para(s,'Heading2'))
        elif kind=='code':
            # Wrap each logical line without collapsing newlines or altering symbols.
            lines=[]
            for line in s.splitlines():
                wrapped=textwrap.wrap(line,width=82,replace_whitespace=False,drop_whitespace=False) or [' ']
                lines.extend(wrapped)
            story.append(Paragraph('<br/>'.join(text(l).replace(' ','&#160;') for l in lines),styles['CodeBlock']))
        elif kind=='bullet':story.append(Paragraph(text(s),styles['Normal'],bulletText='•'))
        else:story.append(para(s,'Small' if references else 'Normal'))
    # Avoid consecutive page breaks around adjacent appendix figures.
    compact=[]
    for f in story:
        if isinstance(f,PageBreak) and compact and isinstance(compact[-1],PageBreak):continue
        compact.append(f)
    if isinstance(compact[-1],PageBreak): compact.pop()
    doc=PaperDoc(str(path),pagesize=(612,792),leftMargin=54,rightMargin=54,topMargin=58,bottomMargin=52,title=title+' '+subtitle,author='Sai Narender Nuckala / DevHeal Labs AI')
    doc.publication=version;doc.build(compact,onFirstPage=furniture,onLaterPages=furniture)
paper=json.loads((SRC/'01-White-Paper/paper.json').read_text(encoding='utf-8'))
build(OUT/'DH-ADOM_White_Paper_v1.1.pdf','DH-ADOM',paper['subtitle'],'White paper 1.1 | 7 October 2026',paper['blocks'])
spec=[]
for filename in ['DH-ADOM-Technical-Specification-v1.0.md','CONFORMANCE-REQUIREMENTS.md']:
    table_rows=[]
    for line in (SRC/'02-Specification'/filename).read_text(encoding='utf-8').splitlines():
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip('|').split('|')]
            if not all(set(c)<=set('-: ') for c in cells):table_rows.append(cells)
            continue
        if not line.strip():continue
        spec.append({'type':'h2' if line.startswith('#') else 'bullet' if line.startswith('- ') else 'p','text':line.lstrip('#- ')})
    if table_rows:spec.append({'type':'table','rows':table_rows})
build(OUT/'DH-ADOM_Specification_v1.0.pdf','DH-ADOM','Technical specification and conformance requirements','Specification 1.0 | Layout revised 7 October 2026',spec)
shutil=None
# Current source and ZIP use the revised documents; archived PDFs remain untouched.
import shutil
shutil.copyfile(OUT/'DH-ADOM_White_Paper_v1.1.pdf',SRC/'01-White-Paper/DH-ADOM_White_Paper_v1.1.pdf')
shutil.copyfile(OUT/'DH-ADOM_Specification_v1.0.pdf',SRC/'02-Specification/DH-ADOM_Specification_v1.0.pdf')
print('Built eight vector figures, revised white paper and specification PDF.')
