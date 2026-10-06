import json, statistics, sys
from pathlib import Path

path=Path(sys.argv[1]) if len(sys.argv)>1 else Path('results/results.json')
data=json.loads(path.read_text())
for group in sorted({r['system'] for r in data}):
    rows=[r for r in data if r['system']==group]
    completion=[r['completion_quality'] for r in rows]
    cost=[r['cost'] for r in rows]
    bypass=[r['governance_bypass'] for r in rows]
    print(group)
    print('  mean_completion_quality=', round(statistics.mean(completion),3))
    print('  mean_cost=', round(statistics.mean(cost),3))
    print('  governance_bypass_rate=', round(statistics.mean(bypass),3))
