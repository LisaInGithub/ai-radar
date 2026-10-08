"""把 Claude 資料庫的匯出檔整理成 GitHub Pages 讀取的 data/ 資料夾。

用法：python3 scripts/build_data.py <匯出資料夾> <網站根目錄>
匯出資料夾的結構：digests/*.json、experts/*.json、predictions/*.json、
settings/*.json、calendar/upcoming.json、experts_meta/pool.json
（即 ArtifactData 讀取時用 out_dir 產生的檔案）
"""
import json, os, sys, glob, shutil

src, site = sys.argv[1], sys.argv[2]
out = os.path.join(site, 'data')
KEEP = 90  # 網站保留最近幾天

def load(p):
    with open(p, encoding='utf8') as f:
        return json.load(f)

def save(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf8') as f:
        json.dump(d, f, ensure_ascii=False, separators=(',', ':'))

def strip_audio(d):
    # Claude 資產網址在 GitHub 上無法播放，改回裝置語音
    pod = d.get('podcast')
    if isinstance(pod, dict) and 'audio' in pod:
        pod.pop('audio')
    return d

man = {}
for coll in ('digests', 'experts'):
    files = sorted(glob.glob(os.path.join(src, coll, '*.json')))[-KEEP:]
    if os.path.isdir(os.path.join(out, coll)):
        shutil.rmtree(os.path.join(out, coll))
    ids = []
    for f in files:
        i = os.path.splitext(os.path.basename(f))[0]
        d = load(f)
        save(os.path.join(out, coll, i + '.json'), strip_audio(d) if coll == 'digests' else d)
        ids.append(i)
    man[coll] = ids

preds = [dict(load(f), id=os.path.splitext(os.path.basename(f))[0])
         for f in sorted(glob.glob(os.path.join(src, 'predictions', '*.json')))]
save(os.path.join(out, 'predictions.json'), preds)

for name, dest in (('calendar/upcoming.json', 'calendar.json'),
                   ('experts_meta/pool.json', 'pool.json'),
                   ('settings/experts.json', 'settings-experts.json')):
    p = os.path.join(src, name)
    if os.path.exists(p):
        save(os.path.join(out, dest), load(p))

v = os.path.join(src, 'settings/voice.json')
if os.path.exists(v):
    d = load(v)
    d.pop('sample', None)
    save(os.path.join(out, 'settings-voice.json'), d)

dates = man.get('digests') or ['']
man['updated'] = dates[-1]
save(os.path.join(out, 'manifest.json'), man)
print('digests', len(man['digests']), 'experts', len(man['experts']), 'predictions', len(preds), 'updated', man['updated'])
