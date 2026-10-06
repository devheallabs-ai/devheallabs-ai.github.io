from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
checks = []

def check(name, ok, detail=""):
    checks.append({"name":name,"status":"PASS" if ok else "FAIL","detail":detail})

required=[
    ROOT/'03-Reference-Templates/ENGINEERING_CONSTITUTION.md',
    ROOT/'03-Reference-Templates/AGENTS.md',
    ROOT/'03-Reference-Templates/ROOT_AGENT.md',
    ROOT/'03-Reference-Templates/FEATURE_AGENT.md',
    ROOT/'03-Reference-Templates/SPECIALIST_AGENT.md',
    ROOT/'03-Reference-Templates/DELEGATION_CONTRACT.yaml',
    ROOT/'02-Specification/CONFORMANCE-REQUIREMENTS.md',
]
for p in required:
    check(f"exists:{p.name}", p.exists(), str(p))

out={"version":"1.0.0","checks":checks,"summary":{"passed":sum(c['status']=='PASS' for c in checks),"failed":sum(c['status']=='FAIL' for c in checks)}}
report=ROOT/'reports/conformance-results.json'
report.parent.mkdir(parents=True,exist_ok=True)
report.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
raise SystemExit(1 if out['summary']['failed'] else 0)
