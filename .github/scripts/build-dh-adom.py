"""Build the source-backed DH-ADOM publication pages (Python standard library only)."""
from pathlib import Path
import hashlib, html, json, re, shutil, zipfile
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'dh-adom/source'
OUT = ROOT / 'dh-adom'
REL = OUT / 'releases/1.1.0'
ASSETS = OUT / 'assets'
for p in (REL, ASSETS): p.mkdir(parents=True, exist_ok=True)
esc = html.escape
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')

# Repackage the supplied numbered layout; keep publication bytes unchanged.
# Replace machine-local inventory/report paths with portable release metadata.
files = [p for p in sorted(SRC.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc' and p.name not in ('PACKAGE-MANIFEST.json', 'conformance-results.json')]
inventory = {p.relative_to(SRC).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
manifest = json.dumps({'release':'1.1.0','packaging':'Numbered source layout; caches omitted; inventory regenerated; paper editorial edition 1.1; specification and runtime remain 1.0. Revised figures and canonical URLs. Portable file-presence report.','sha256':inventory}, indent=2)
checks = ['ENGINEERING_CONSTITUTION.md','AGENTS.md','ROOT_AGENT.md','FEATURE_AGENT.md','SPECIALIST_AGENT.md','DELEGATION_CONTRACT.yaml']
report = {'version':'1.0.0','scope':'Seven file-presence checks; not full normative conformance','checks':[{'path':'03-Reference-Templates/'+n,'exists':(SRC/'03-Reference-Templates'/n).exists()} for n in checks] + [{'path':'02-Specification/CONFORMANCE-REQUIREMENTS.md','exists':(SRC/'02-Specification/CONFORMANCE-REQUIREMENTS.md').exists()}]}
with zipfile.ZipFile(REL/'DH-ADOM-1.1.0-publication.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in files:
        info=zipfile.ZipInfo('DH-ADOM/'+p.relative_to(SRC).as_posix(), (2026,10,6,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED
        z.writestr(info,p.read_bytes())
    for name, content in [('PACKAGE-MANIFEST.json',manifest),('reports/conformance-results.json',json.dumps(report,indent=2))]:
        info=zipfile.ZipInfo('DH-ADOM/'+name,(2026,10,6,0,0,0)); info.compress_type=zipfile.ZIP_DEFLATED; z.writestr(info,content)
for rel in ['01-White-Paper/DH-ADOM_White_Paper_v1.1.pdf','01-White-Paper/DH-ADOM_White_Paper_v1.1.md','02-Specification/DH-ADOM_Specification_v1.0.pdf','11-Licensing-and-Citation/LICENSE.md']:
    shutil.copyfile(SRC/rel,REL/Path(rel).name)
write(REL/'manifest.json',manifest)
citation = (SRC/'11-Licensing-and-Citation/BIBTEX.bib').read_text().replace('https://devheallabs.in','https://devheallabs.com')
write(REL/'citation.bib',citation)
write(REL/'verification.json',json.dumps(report,indent=2))
write(REL/'checksums.json',json.dumps({p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(REL.iterdir()) if p.is_file() and p.name!='checksums.json'},indent=2))

# Bespoke vector artwork: shared site palette, large type and one reading direction.
def diagram(name,title,subtitle,steps,footer):
    h=190+len(steps)*112
    svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="{h}" viewBox="0 0 600 {h}" role="img" aria-labelledby="title desc"><title id="title">{esc(title)}</title><desc id="desc">{esc(subtitle+' '+'. '.join(a+': '+b for a,b in steps)+'. '+footer)}</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#12305e"/><stop offset="1" stop-color="#1552b8"/></linearGradient><marker id="arrow" markerWidth="8" markerHeight="8" refX="4" refY="4" orient="auto"><path d="M1 1L6 4L1 7" fill="none" stroke="#2b90ff" stroke-width="1.5"/></marker></defs><rect width="600" height="{h}" rx="28" fill="#f6f7fb"/><text x="32" y="43" font-family="Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="2" fill="#1552b8">DH-ADOM / ENGINEERING METHOD</text><text x="32" y="83" font-family="Arial,sans-serif" font-size="30" font-weight="700" fill="#111120">{esc(title)}</text>'''
    for i,(label,detail) in enumerate(steps):
        y=112+i*112
        if i: svg+=f'<path d="M300 {y-28}V{y-9}" stroke="#2b90ff" stroke-width="2" marker-end="url(#arrow)"/>'
        svg+=f'<rect x="24" y="{y}" width="552" height="84" rx="16" fill="{ "url(#bg)" if i==0 else "#ffffff"}" stroke="{ "#1552b8" if i==0 else "#d8e2f1"}"/><text x="44" y="{y+31}" font-family="Arial,sans-serif" font-size="23" font-weight="700" fill="{ "#ffffff" if i==0 else "#12305e"}">{esc(label)}</text><text x="44" y="{y+60}" font-family="Arial,sans-serif" font-size="19" fill="{ "#dceaff" if i==0 else "#53536a"}">{esc(detail)}</text>'
    svg+=f'<text x="32" y="{h-27}" font-family="Arial,sans-serif" font-size="18" fill="#53536a">{esc(footer)}</text></svg>'
    write(ASSETS/(name+'.svg'),svg)
diagram('hierarchy','Clear ownership. Bounded work.','Governance flows into accountable agent roles.', [('Engineering constitution','Shared rules and authority boundaries'),('AI-SDLC + ADLC','Software and agent lifecycle governance'),('Root agent','Route work and coordinate across domains'),('Feature agents','Own bounded engineering domains'),('Specialist agents','Execute scoped tasks and return evidence')],'Evidence returns through the ownership hierarchy.')
diagram('delegation','From intent to evidence.','Delegation and review flow.', [('Root routes the request','Identify the responsible feature owner'),('Feature defines the contract','Scope, permissions, budget and acceptance'),('Specialist performs the task','Operate within delegated authority'),('Validate and collect evidence','Record changes, checks and remaining risks'),('Handoff and integration','Feature reviews; Root coordinates delivery')],'Every handoff keeps the next session informed.')
diagram('boundaries','Authority stays explicit.','Design controls for bounded delegation.', [('Parent authority','Declared scope, tools and permissions'),('Delegation contract','Task, lifetime, budget and evidence'),('Child authority','Subset of authorized delegated permissions'),('Execution controls','Enforce limits in the host runtime'),('Reviewable outcome','Validation, audit trail and handoff')],'Design requirements; enforcement depends on runtime.')
originals=SRC/'07-Architecture-Diagrams/svg'
for p in originals.glob('*.svg'): shutil.copyfile(p,ASSETS/p.name)

base=(ROOT/'research/index.html').read_text(encoding='utf-8')
header=base[base.index('<body>'):base.index('<main')]
footer=base[base.index('<footer>'):]
navlink='<li><a href="/dh-adom/">DH-ADOM engineering method</a></li>'
header=header.replace('Dummu<span','Dummu <span')
header=header.replace('<li><a href="/research/">Research publications</a></li>','<li><a href="/research/">Research publications</a></li>'+navlink)
pages=[('', 'Overview'),('whitepaper','White paper'),('specification','Specification'),('architecture','Architecture'),('implementation','Implementation'),('evaluation','Evaluation'),('security','Security'),('research','Research'),('downloads','Downloads'),('conformance','Conformance'),('schemas','Schemas & API'),('adoption','Adoption')]
def link(file,label): return f'<a href="/dh-adom/releases/1.1.0/{file}">{label}</a>'
def section(title,body): return '<section class="dh-section"><h2>'+title+'</h2>'+body+'</section>'
def cards(items): return '<div class="dh-grid">'+''.join(f'<a class="dh-card" href="/dh-adom/{slug}/"><span class="dh-kicker">{esc(kicker)}</span><h3>{esc(title)}</h3><p>{esc(desc)}</p><span aria-hidden="true">Explore →</span></a>' for slug,kicker,title,desc in items)+'</div>'
def fig(name,alt,caption):
    catalog=json.loads((ASSETS/'figures.json').read_text(encoding='utf-8'))
    equivalent=''
    if name in catalog:
        _,steps,note=catalog[name]
        equivalent='<details class="dh-equivalent"><summary>Text equivalent</summary><ul>'+''.join('<li><strong>'+esc(a)+'</strong>: '+esc(b)+'</li>' for a,b in steps)+'</ul><p>'+esc(note)+'</p></details>'
    return f'<figure class="dh-figure"><img src="/dh-adom/assets/{name}.svg?v=20261007-adom11" alt="{esc(alt)}" loading="lazy"><figcaption>{caption}<div class="dh-actions"><button type="button" class="dh-enlarge" data-diagram="/dh-adom/assets/{name}.svg?v=20261007-adom11" data-title="{esc(alt)}">Enlarge diagram</button><a href="/dh-adom/assets/{name}.svg?v=20261007-adom11">Open SVG ↗</a></div>{equivalent}</figcaption></figure>'
def page(slug,title,desc,body):
    route='/dh-adom/'+(slug+'/' if slug else '')
    nav='<nav class="dh-nav" aria-label="DH-ADOM publication">'+''.join(f'<a href="/dh-adom/{s+"/" if s else ""}"'+(' aria-current="page"' if s==slug else '')+'>'+n+'</a>' for s,n in pages)+'</nav>'
    structured={"@context":"https://schema.org","@type":"TechArticle","headline":title,"description":desc,"url":"https://devheallabs.com"+route,"datePublished":"2026-10-06","dateModified":"2026-10-07","author":{"@type":"Person","name":"Sai Narender Nuckala"},"publisher":{"@type":"Organization","name":"DevHeal Labs AI","url":"https://devheallabs.com/"},"version":"1.1"}
    metadata='<meta name="robots" content="index,follow"><meta name="twitter:card" content="summary"><meta name="author" content="Sai Narender Nuckala"><script type="application/ld+json">'+json.dumps(structured).replace('<','\\u003c')+'</script>'
    text=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} — DH-ADOM — DevHeal Labs</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="https://devheallabs.com{route}"><link rel="icon" href="/favicon.png"><meta property="og:title" content="{esc(title)} — DH-ADOM"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="https://devheallabs.com{route}"><meta property="og:type" content="article"><meta property="og:image" content="https://devheallabs.com/logo.png"><link rel="stylesheet" href="/assets/style.css?v=20261005-premium"><link rel="stylesheet" href="/dh-adom/assets/publication.css?v=20261007-adom11">{metadata}</head>{header}<main id="main-content" class="dh-main"><div class="container"><header class="dh-heading"><a class="dh-kicker" href="/research/">DevHeal Research / DH-ADOM</a><h1>{title}</h1><p>{desc}</p><div class="dh-meta">White paper 1.1 · Publication package 1.1.0 · 7 October 2026</div></header>{nav}{body}<aside class="dh-source">Source: DH-ADOM publication package 1.1.0. Specification and runtime 1.0. <a href="/dh-adom/downloads/">Original documents, citation and source inventory →</a></aside></div></main>{footer}'''
    viewer='<dialog id="diagram-viewer" aria-labelledby="diagram-title"><header><h2 id="diagram-title">Diagram</h2><div class="dh-actions"><button type="button" data-zoom="out" aria-label="Zoom out">−</button><output id="diagram-scale">100%</output><button type="button" data-zoom="in" aria-label="Zoom in">+</button><button type="button" id="diagram-close">Close</button></div></header><div class="diagram-scroll" tabindex="0" aria-label="Scrollable diagram"><img id="diagram-image" alt=""></div></dialog><script src="/dh-adom/assets/publication.js?v=20261007-adom11"></script>'
    text=text.replace('</body>',viewer+'</body>')
    write(OUT/slug/'index.html',text)

page('', 'An operating model for agent-led engineering.', 'DH-ADOM connects engineering governance, domain ownership and bounded delegation so teams can organize AI-assisted software work with clear accountability.', '<div class="dh-hero"><div><span class="dh-kicker">DevHeal Hierarchical Agent Development &amp; Orchestration Model</span><h2>Give every agent a purpose. Give every change an owner.</h2><p>Coordinate a Root agent, persistent Feature agents and task-scoped Specialists through explicit contracts, validation and evidence-backed handoffs.</p><div class="dh-actions"><a class="btn btn-primary" href="/dh-adom/whitepaper/">Read the white paper →</a><a class="btn btn-secondary" href="/dh-adom/implementation/">Explore the implementation</a></div><p class="dh-note">An engineering method for organizing agent work, with a specification and a Python reference package.</p></div>'+fig('hierarchy','Constitution and lifecycle governance guide Root, Feature and Specialist agents.','Governance flows down; evidence and review return through the hierarchy.')+'</div>'+section('Start with the problem you need to solve.',cards([('architecture','Organization','Who owns the work?','Separate global coordination, durable domain ownership and bounded task execution.'),('specification','Contracts','What can an agent do?','Define scope, authority, budgets, lifecycle and acceptance requirements.'),('implementation','Engineering','How do I apply it?','Inspect the reference library, repository templates and reproducible demo.'),('evaluation','Evidence','How do I assess it?','Review the supplied checks and a controlled comparison protocol.')])) )

# The PDF and browser reader share ordered paragraphs, tables and figures.
paper=[];toc=[];count=0
paper_data=json.loads((SRC/'01-White-Paper/paper.json').read_text(encoding='utf-8'))
for block in paper_data['blocks']:
    kind=block['type']
    if kind in ('h2','h3'):
        count+=1;anchor='paper-'+str(count)
        paper.append(f'<{kind} id="{anchor}">{esc(block["text"])}</{kind}>')
        if kind=='h2':toc.append(f'<a href="#{anchor}">{esc(block["text"])}</a>')
    elif kind=='table':
        rows=block['rows'];paper.append('<div class="dh-table"><table><thead><tr>'+''.join('<th scope="col">'+esc(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>')
    elif kind=='figure':paper.append(fig(block['name'],block['caption'],block['caption']))
    elif kind=='code':paper.append('<pre>'+esc(block['text'])+'</pre>')
    elif kind=='bullet':paper.append('<ul><li>'+esc(block['text'])+'</li></ul>')
    else:paper.append('<p>'+esc(block['text'])+'</p>')
page('whitepaper','The DH-ADOM white paper.', 'An engineering operating model for repository ownership, bounded delegation and evidence-backed handoffs.', '<div class="dh-actions">'+link('DH-ADOM_White_Paper_v1.1.pdf','Download white paper 1.1 / PDF')+' '+link('DH-ADOM_White_Paper_v1.1.md','Download text source / Markdown')+'</div><p class="dh-note">Edition 1.1 updates adoption examples, canonical links and presentation. The technical model remains version 1.0. <a href="/dh-adom/downloads/#archive">Earlier edition →</a></p><details class="dh-toc"><summary>Contents</summary>'+''.join(toc)+'</details><article class="dh-paper">'+''.join(paper)+'</article>')

def md(text):
    result=[]
    rows=[]
    for line in text.splitlines():
        if line.startswith('|'):
            cells=[c.strip() for c in line.strip('|').split('|')]
            if not all(set(c)<=set('-: ') for c in cells):rows.append(cells)
            continue
        if rows:
            result.append('<div class="dh-table"><table><thead><tr>'+''.join('<th scope="col">'+esc(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>');rows=[]
        if not line.strip(): continue
        line=esc(line)
        line=re.sub(r'`([^`]+)`',r'<code>\1</code>',line)
        line=re.sub(r'\*\*([^*]+)\*\*',r'<strong>\1</strong>',line)
        if line.startswith('#'):
            n=min(len(line)-len(line.lstrip('#'))+1,4); result.append(f'<h{n}>'+line.lstrip('# ') + f'</h{n}>')
        elif line.startswith('- '): result.append('<ul><li>'+line[2:]+'</li></ul>')
        else: result.append('<p>'+line+'</p>')
    if rows:result.append('<div class="dh-table"><table><thead><tr>'+''.join('<th scope="col">'+esc(c)+'</th>' for c in rows[0])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(c)+'</td>' for c in row)+'</tr>' for row in rows[1:])+'</tbody></table></div>')
    return ''.join(result)
page('specification','Contracts that make ownership explicit.', 'The normative specification defines roles, delegation boundaries, lifecycle integration, evidence and conformance requirements.', '<article class="dh-paper">'+md((SRC/'02-Specification/DH-ADOM-Technical-Specification-v1.0.md').read_text())+md((SRC/'02-Specification/CONFORMANCE-REQUIREMENTS.md').read_text())+'</article>'+section('Machine-readable definitions','<p>The publication ZIP includes four JSON schemas, three lifecycle state machines and an OpenAPI interface outline. The outline describes intended interfaces; the package does not provide an HTTP service.</p><a href="/dh-adom/downloads/">Get the specification and schemas →</a>'))
captions=[('01-dh-adom-hierarchy','Governance hierarchy','Constitution and lifecycle governance lead into Root, Feature and Specialist responsibilities.'),('02-lifecycle-integration','Lifecycle integration','Intent moves through requirements, architecture, implementation, validation, evidence and release; production feedback informs the next cycle.'),('03-delegation-sequence','Delegation sequence','A request is routed to a feature owner, delegated to a specialist, validated and returned with evidence.'),('04-agent-state-machine','Agent lifecycle','Agent lifecycle states separate creation, operation and retirement.'),('05-ownership-boundaries','Ownership boundaries','Feature ownership provides coordination boundaries for engineering work.'),('06-security-delegation-controls','Delegation controls','Permissions and budgets constrain delegated authority.'),('07-traceability','Traceability','Evidence connects the engineering intent, implementation and review.'),('08-reference-architecture','Reference architecture','A conceptual arrangement of governance, orchestration and execution components.')]
page('architecture','See how the model fits together.', 'Purpose-built diagrams show the method at a glance. The detailed figures below can be enlarged and zoomed without losing clarity.', '<div class="dh-grid dh-visuals">'+fig('hierarchy','Governance hierarchy from constitution to specialists.','01 / Ownership hierarchy')+fig('delegation','Request, contract, execution, validation and handoff.','02 / Work and evidence flow')+fig('boundaries','Parent authority bounds the contract and child authority.','03 / Delegation boundaries')+'</div>'+section('Detailed model diagrams.','<div class="dh-originals">'+''.join('<details><summary>'+title+'</summary><p>'+desc+'</p>'+fig(name,desc,'Revised vector figure.')+'</details>' for name,title,desc in captions)+'</div>'))
page('implementation','Inspect it. Run it. Adapt it.', 'A small Python reference library makes the core routing and delegation concepts executable, alongside repository templates and machine-readable contracts.', section('Run the included example.','<p>Download and extract the publication ZIP. From its <code>DH-ADOM/04-Reference-Implementation</code> directory, use Python 3.11 or later:</p><pre>python -m unittest discover -s tests -v\npython -m examples.demo</pre><p>The demo returns <code>COMPLETE</code> for <code>TASK-DEMO</code> and records four audit events. It demonstrates control flow using deterministic specialist execution.</p><a href="/dh-adom/downloads/">Download the source package →</a>')+section('What the reference library demonstrates.','<div class="dh-table"><table><thead><tr><th>Component</th><th>Included behavior</th><th>Integration boundary</th></tr></thead><tbody><tr><td>Registry</td><td>Agent identity records and feature-owner lookup</td><td>In-memory storage</td></tr><tr><td>Policy</td><td>Identity, declared depth, step/cost budgets and permission checks</td><td>Runtime metering and filesystem containment require host enforcement</td></tr><tr><td>Specialist</td><td>Deterministic completion and audit events</td><td>Connect model and tool execution in the host</td></tr><tr><td>Audit</td><td>In-memory timestamped event records</td><td>Durable storage and denied-attempt logging require integration</td></tr><tr><td>Interfaces</td><td>JSON schemas and OpenAPI outline</td><td>No HTTP server is bundled</td></tr></tbody></table></div>')+section('Bring the method into a repository.','<ol><li>Define engineering rules in the constitution.</li><li>Assign a Root coordinator and one owner for each meaningful feature domain.</li><li>Declare agent capabilities, permissions, budgets and lifecycle state.</li><li>Use the supplied delegation contract for task scope and acceptance criteria.</li><li>Persist implementation evidence and a handoff that another session can use.</li><li>Evaluate the normative requirements against the actual host runtime.</li></ol><p>Templates are in <code>03-Reference-Templates</code>. Library source and tests are in <code>04-Reference-Implementation</code>.</p>'))
page('evaluation','Measure the engineering outcome.', 'Evaluation separates executable example checks, artifact completeness and comparative engineering performance.', section('Verified package checks.','<div class="dh-grid"><div class="dh-card"><h3>3 supplied unit tests pass</h3><p>Feature routing, valid delegation and permission-escalation rejection. Executed during this publication review.</p></div><div class="dh-card"><h3>7 required files present</h3><p>The supplied conformance script checks file presence. Full normative conformance requires assessing all 20 requirements.</p></div><div class="dh-card"><h3>4 demo audit events</h3><p>The deterministic example traces routing, authorization and specialist execution. This is an example, not a production benchmark.</p></div></div>')+section('A controlled comparison protocol.',md((SRC/'06-Benchmarks-Experiments/experiments/experiment-protocol.md').read_text())+'<p>The package includes a task catalog, result schema and analysis script. Comparative result datasets are not included in this release.</p>'))
page('security','Bound authority at every handoff.', 'The method requires least privilege, explicit delegation and reviewable evidence. Runtime integrations are responsible for enforcing those requirements.', '<div class="dh-hero"><div>'+section('Design controls.','<ul><li>Keep identity distinct from the underlying model.</li><li>Limit child authority to the approved delegation.</li><li>Bound depth, parallelism, time, cost and tool access.</li><li>Require policy approval for production actions and authority changes.</li><li>Validate outputs and preserve evidence before integration.</li></ul>')+section('Implementation boundary.','<p>The reference policy demonstrates a subset of these checks. Production adoption needs sandboxing, filesystem scope enforcement, runtime metering, durable audit storage, timeout handling and review of denied actions.</p><p>Evaluate these controls in your deployment environment; the source package is not a security certification.</p>')+'</div>'+fig('boundaries','Authority passes through a bounded delegation contract to the child agent.','Controls describe the intended design, not a claim of complete runtime enforcement.')+'</div>')
research=section('The contribution.','<p>DH-ADOM brings established agent patterns into a repository-level operating model: persistent feature ownership, Root orchestration, bounded Specialist delegation, lifecycle governance and resumable handoffs. Its contribution is the composition of these practices into an explicit engineering method.</p><p>Hierarchy adds coordination overhead. Benefits depend on task structure, clear ownership boundaries and effective runtime enforcement. Comparative performance remains an empirical question.</p>')
research+=section('Related work.',md((SRC/'08-Research-Publications/related-work.md').read_text(encoding='utf-8')))
bib=(SRC/'08-Research-Publications/bibliography.bib').read_text()
refs=re.findall(r'title\s*=\s*\{([^}]+)\}[\s\S]*?url\s*=\s*\{([^}]+)\}',bib)
research+=section('References.','<ul>'+''.join(f'<li><a href="{esc(url)}">{esc(title)}</a></li>' for title,url in refs)+'</ul>')
research+=section('Questions for evaluation.','<ul><li>When does persistent feature ownership improve handoff quality?</li><li>How does delegation depth affect cost, latency and validation coverage?</li><li>Which controls prevent scope drift across sessions?</li><li>How reliably can a new session resume from recorded evidence?</li></ul><p><a href="/dh-adom/evaluation/">Review the comparison protocol →</a></p>')
research+=section('Release 1.0.0 · 6 October 2026.','<p>The initial package includes the paper, normative specification, four JSON schemas, role templates, Python demonstration library, file-presence checks, experiment tooling and architecture diagrams.</p>')
research+=section('Future research.','<p>The supplied roadmap explores interoperability with MCP and A2A, runtime policy validation, cross-session evaluation, standards profiles and evidence-driven autonomy. These are research directions; release dates and delivery commitments are not assigned.</p>')
page('research','An engineering model, open to examination.', 'Explore the contribution, related work and research questions behind DH-ADOM. Future directions describe research intent rather than delivered capabilities.', '<article class="dh-paper">'+research+'</article>')
downloads=[('DH-ADOM_White_Paper_v1.1.pdf','White paper 1.1 / PDF','Revised layout, generic adoption examples and vector figures.'),('DH-ADOM_White_Paper_v1.1.md','Paper text / Markdown','Editable text source of the current paper.'),('DH-ADOM_Specification_v1.0.pdf','Specification 1.0 / PDF','Normative requirements with refreshed typography and tables.'),('DH-ADOM-1.1.0-publication.zip','Publication 1.1.0 / ZIP','Current paper, specification, reference code, templates and diagrams.')]
page('downloads','The publication, in full.', 'Download the current publication and inspect its source, licensing and integrity metadata.', '<div class="dh-grid">'+''.join('<div class="dh-card"><h2>'+title+'</h2><p>'+desc+'</p>'+link(file,'Download →')+f'<p class="dh-note">{(REL/file).stat().st_size:,} bytes</p></div>' for file,title,desc in downloads)+'</div>'+section('Versions and source.','<p>White paper 1.1 and publication package 1.1.0 were revised on 7 October 2026. Specification and Python runtime remain 1.0. This editorial release adds readable diagrams, generic examples, direct schemas and conformance guidance; it does not introduce new runtime enforcement or empirical results.</p><p><a href="https://github.com/devheallabs-ai/devheallabs-ai.github.io/tree/main/dh-adom/source">Browse the publication source on GitHub →</a></p><div class="dh-actions">'+link('checksums.json','SHA-256 checksums')+link('manifest.json','Source inventory')+link('verification.json','File-presence report')+'</div>')+section('Cite DH-ADOM.','<p>Sai Narender Nuckala. <em>DH-ADOM: DevHeal Hierarchical Agent Development &amp; Orchestration Model.</em> DevHeal Labs AI, 2026. White paper 1.1.</p><pre>'+esc(citation)+'</pre>'+link('citation.bib','Download BibTeX'))+section('Licensing.','<p>The Python reference implementation carries an Apache-2.0 notice. Publication materials, including templates and diagrams, retain the supplied research-and-evaluation terms. These terms differ by component; the whole publication is not offered under a single open-source license.</p>'+link('LICENSE.md','Read publication terms')+' · <a href="/dh-adom/source/04-Reference-Implementation/LICENSE">Read reference code license</a>')+'<section class="dh-section" id="archive"><h2>Archived first edition.</h2><p>The first release remains unchanged for citation and reproducibility. It contains historical naming and layout that are superseded by edition 1.1.</p><div class="dh-actions"><a href="/dh-adom/releases/1.0.0/DH-ADOM_White_Paper_v1.0.pdf">Original PDF 1.0</a><a href="/dh-adom/releases/1.0.0/DH-ADOM_White_Paper_v1.1-illustrated.docx">Original illustrated DOCX (cover 1.0)</a><a href="/dh-adom/releases/1.0.0/DH-ADOM-1.0.0-publication.zip">Original package 1.0.0</a></div></section>')

import dh_adom_adoption
dh_adom_adoption.build(globals())

# Existing discovery routes, without changing the business homepage or product positioning.
for p in ROOT.rglob('*.html'):
    if '.github' in p.parts or 'dh-adom' in p.parts or '.git' in p.parts: continue
    text=p.read_text(encoding='utf-8').replace('Dummu<span','Dummu <span')
    needle='<li><a href="/research/">Research publications</a></li>'
    if needle in text and navlink not in text: text=text.replace(needle,needle+navlink)
    if p.relative_to(ROOT).as_posix() in ('research/index.html','whitepaper/index.html','developers/index.html','technology/index.html') and 'id="dh-adom-publication"' not in text:
        block='<section id="dh-adom-publication"><div class="container"><div class="sec-label">Engineering method</div><h2 class="sec-title">DH-ADOM</h2><p class="sec-desc">A hierarchical operating model for agent-led engineering: clear domain ownership, bounded delegation and evidence-backed handoffs.</p><a class="btn btn-primary" href="/dh-adom/">Explore the paper, diagrams and source →</a></div></section>'
        text=text.replace('</main>',block+'</main>')
    write(p,text)
sitemap=ROOT/'sitemap.xml'; text=sitemap.read_text()
for slug,_ in pages:
    url='https://devheallabs.com/dh-adom/'+(slug+'/' if slug else '')
    if '<loc>'+url+'</loc>' not in text: text=text.replace('</urlset>',f'<url><loc>{url}</loc></url>\n</urlset>')
write(sitemap,text)
print('Built 12 DH-ADOM pages with revised figures, adoption guidance and versioned downloads.')
