"""Validate evidence provenance and render a compact source-linked evidence register."""
import argparse
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

def validate(sources,evidence):
    ids=set()
    for s in sources:
        if not re.fullmatch(r'S[0-9]{1,3}',s['id']) or s['id'] in ids: raise ValueError('duplicate/invalid source id')
        ids.add(s['id'])
        u=urlsplit(s['url'])
        if u.scheme!='https' or not u.hostname or u.username or u.password: raise ValueError('invalid source URL')
        accessed=date.fromisoformat(s['accessed'])
        if s['published'] and date.fromisoformat(s['published'])>accessed: raise ValueError('source dates reversed')
        for k in ('title','type','locator','limitation'):
            if not s[k]: raise ValueError('missing source field')
    seen=set()
    for e in evidence:
        if not re.fullmatch(r'E[0-9]{1,3}',e['id']) or e['id'] in seen: raise ValueError('duplicate/invalid evidence id')
        seen.add(e['id'])
        if not e['source_ids'] or not set(e['source_ids'])<=ids: raise ValueError('unknown source')
        if not e['claim'] or not e['locator']: raise ValueError('missing evidence')
        if e['kind'] not in ('reported_observation','analyst_inference'): raise ValueError('invalid evidence kind')
        if e['confidence'] not in ('low','medium','high'): raise ValueError('invalid confidence')
        if e['technique']:
            if not re.fullmatch(r'T[0-9]{4}(?:\.[0-9]{3})?',e['technique']) or e['technique_source'] not in ids:
                raise ValueError('invalid ATT&CK reference')
    return True

def render(sources,evidence):
    validate(sources,evidence)
    by_id={s['id']:s for s in sources}
    lines=['# Evidence register','',
        'Secondary-source portfolio analysis. ATT&CK mappings are analyst judgments.',
        'Confidence concerns our claim, not a numerical probability.','']
    for e in evidence:
        links=', '.join('['+sid+']('+by_id[sid]['url']+')' for sid in e['source_ids'])
        mapping=('['+e['technique']+']('+by_id[e['technique_source']]['url']+')') if e['technique'] else 'not mapped'
        lines += ['## '+e['id'],e['claim'],'',
            'Source: '+links+'; section: '+e['locator']+'.',
            'Kind: '+e['kind']+'; confidence: '+e['confidence']+'; mapping: '+mapping+'.','']
    lines+=['## Source register','']
    for s in sources:
        lines+=['- ['+s['id']+' — '+s['title']+']('+s['url']+'); published: '+str(s['published'] or 'not recorded')+'; accessed: '+s['accessed']+'. '+s['limitation']]
    return '\n'.join(lines)+'\n'

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--data',type=Path,default=Path('data'))
    a=p.parse_args()
    try:
        sources=json.loads((a.data/'sources.json').read_text(encoding='utf-8'))
        evidence=json.loads((a.data/'evidence.json').read_text(encoding='utf-8'))
        print(render(sources,evidence),end='')
    except (ValueError,OSError,KeyError,TypeError) as exc: p.error(str(exc))

if __name__=='__main__': main()
