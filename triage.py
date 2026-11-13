"""Synthetic behavioral correlation, not a production detection rule."""
from datetime import datetime, timedelta
import json
from pathlib import Path
import argparse

def correlate(events,window_minutes=30):
    if not 1<=window_minutes<=1440: raise ValueError('invalid correlation window')
    normalized=[]; seen=set()
    for e in events:
        if e['id'] in seen: raise ValueError('duplicate event ID')
        seen.add(e['id'])
        t=datetime.fromisoformat(e['timestamp'].replace('Z','+00:00'))
        if t.tzinfo is None: raise ValueError('timezone required')
        if e['event_type'] not in ('unusual_signin','mailbox_access','inbox_rule_created'):
            raise ValueError('unsupported event type')
        if not e['account_id']: raise ValueError('missing account')
        normalized.append((t,e))
    normalized.sort(key=lambda x:(x[0],x[1]['id']))
    results=[]
    for start,login in normalized:
        if login['event_type']!='unusual_signin': continue
        later=[(t,e) for t,e in normalized if e['account_id']==login['account_id']
            and start<=t<=start+timedelta(minutes=window_minutes) and e['id']!=login['id']]
        access=[(t,e) for t,e in later if e['event_type']=='mailbox_access']
        rules=[(t,e) for t,e in later if e['event_type']=='inbox_rule_created']
        pairs=[(a,b) for a in access for b in rules if a[0]<=b[0]]
        if pairs:
            a,b=min(pairs,key=lambda pair:(pair[1][0],pair[0][0],pair[0][1]['id'],pair[1][1]['id']))
            results.append({'account_id':login['account_id'],'evidence_ids':[login['id'],a[1]['id'],b[1]['id']],
                'window_minutes':window_minutes,'assessment':'review_required_not_confirmed_compromise'})
    return results

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('input',type=Path)
    a=p.parse_args()
    try:
        if a.input.stat().st_size>1_000_000: raise ValueError('input exceeds 1 MB')
        events=json.loads(a.input.read_text(encoding='utf-8'))
        if len(events)>500: raise ValueError('maximum 500 events')
        print(json.dumps(correlate(events),indent=2))
    except (ValueError,OSError,KeyError,TypeError) as exc: p.error(str(exc))

if __name__=='__main__': main()
