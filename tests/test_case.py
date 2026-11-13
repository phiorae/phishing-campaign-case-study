from copy import deepcopy
import json
from pathlib import Path
import unittest
import report
import triage
ROOT=Path(__file__).resolve().parents[1]

class CaseTests(unittest.TestCase):
    def setUp(self):
        self.sources=json.loads((ROOT/'data/sources.json').read_text())
        self.evidence=json.loads((ROOT/'data/evidence.json').read_text())
        self.events=json.loads((ROOT/'examples/synthetic-events.json').read_text())
    def test_provenance_and_reproducibility(self):
        self.assertTrue(report.validate(self.sources,self.evidence))
        self.assertEqual(report.render(self.sources,self.evidence),(ROOT/'examples/evidence-register.md').read_text())
    def test_missing_source_fails(self):
        self.evidence[0]['source_ids']=['S99']
        with self.assertRaises(ValueError): report.validate(self.sources,self.evidence)
    def test_duplicate_evidence_fails(self):
        with self.assertRaises(ValueError): report.validate(self.sources,self.evidence+[self.evidence[0]])
    def test_reversed_source_dates(self):
        self.sources[0]['accessed']='2020-01-01'
        with self.assertRaises(ValueError): report.validate(self.sources,self.evidence)
    def test_analytic_mapping_requires_reference(self):
        self.evidence[0]['technique_source']='S99'
        with self.assertRaises(ValueError): report.validate(self.sources,self.evidence)
    def test_triage_true_and_negative_controls(self):
        out=triage.correlate(self.events)
        self.assertEqual(len(out),1)
        self.assertEqual(out[0]['evidence_ids'],['L01','L02','L03'])
        self.assertEqual(out,triage.correlate(list(reversed(self.events))))
    def test_cross_account_not_correlated(self):
        self.events[2]['account_id']='other-lab-account'
        self.assertEqual(triage.correlate(self.events),[])
    def test_outside_window(self):
        self.events[2]['timestamp']='2024-01-01T10:31:00Z'
        self.assertEqual(triage.correlate(self.events),[])
    def test_wrong_event_order(self):
        self.events[2]['timestamp']='2024-01-01T10:02:00Z'
        self.assertEqual(triage.correlate(self.events),[])
    def test_timezone_required(self):
        self.events[0]['timestamp']='2024-01-01T10:00:00'
        with self.assertRaises(ValueError): triage.correlate(self.events)
    def test_duplicate_event_rejected(self):
        with self.assertRaises(ValueError): triage.correlate(self.events+[self.events[0]])

if __name__=='__main__': unittest.main()
