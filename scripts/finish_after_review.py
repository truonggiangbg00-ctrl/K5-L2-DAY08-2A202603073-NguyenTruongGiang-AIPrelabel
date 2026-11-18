"""Run only after human review of all 24 batch images. Does not submit or publish."""
import argparse
import csv
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reviewed', required=True, type=Path)
    ap.add_argument('--confirm-reviewed', action='store_true')
    ap.add_argument('--review-minutes', type=float, help='Measured total review time only; omit if unavailable')
    a = ap.parse_args()
    if not a.confirm_reviewed:
        ap.error('Confirm all 24 images have actually been reviewed with --confirm-reviewed.')
    if a.review_minutes is not None and (not math.isfinite(a.review_minutes) or a.review_minutes <= 0):
        ap.error('--review-minutes must be a positive finite measured duration.')
    if not a.reviewed.is_file():
        ap.error('Reviewed COCO JSON file does not exist. Extract the CVAT export ZIP first.')
    data = json.loads(a.reviewed.read_text(encoding='utf-8-sig'))
    with (ROOT/'data/split.csv').open(encoding='utf-8-sig') as f:
        expected = {r['image'] for r in csv.DictReader(f) if r['split']=='batch'}
    names = [str(i['file_name']).replace('\\','/').split('/')[-1] for i in data.get('images', [])]
    if len(names)!=24 or len(set(names))!=24 or set(names)!=expected:
        ap.error('Export must contain exactly the 24 unique batch images from data/split.csv.')
    target = ROOT/'submission/labels/batch_reviewed.json'
    if target.exists() and a.reviewed.resolve()!=target.resolve():
        ap.error('batch_reviewed.json exists. Preserve a backup and explicitly update it before rerunning.')
    # Validate before any mutation or reading the trap key.
    def run(script, *args):
        subprocess.run([sys.executable, str(ROOT/'scripts'/script), *map(str,args)],cwd=ROOT,check=True)
    run('validate_labels.py', a.reviewed.resolve(), '--expect', 'batch')
    if a.reviewed.resolve()!=target.resolve():
        target.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if a.review_minutes is not None:
        log=ROOT/'submission/time_log.csv'
        with log.open(encoding='utf-8-sig',newline='') as f:
            reader=csv.DictReader(f); fields=reader.fieldnames; rows=list(reader)
        if any(r['step']=='batch_review' for r in rows):
            print('Preserving existing batch_review time entry.')
        else:
            rows.append(dict(step='batch_review',images=24,minutes=a.review_minutes,
                             note='Total measured duration supplied by human reviewer after completing 24 images'))
            with log.open('w',encoding='utf-8',newline='') as f:
                writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(rows)
    run('review_stats.py','--pre','submission/prelabel/pre_traps.coco.json',
        '--final',target,'--gold','submission/labels/gold_manual.json',
        '--key','submission/prelabel/traps_key.json')
    run('build_release.py')
    if (ROOT/'submission/qc/qc_review.csv').exists():
        print('Existing QC sample/review preserved; inspect freshness if labels changed.')
    else:
        run('qc_sample.py','--seed','42')
    print('Candidate and statistics generated. Human QC, calibration, report and submission checks remain.')

if __name__=='__main__':
    main()
