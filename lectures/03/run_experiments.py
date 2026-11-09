from pathlib import Path
import subprocess, sys, os, json, time, platform, importlib.metadata as md
from datetime import datetime, timezone
out=Path('lectures/03/results'); out.mkdir(parents=True,exist_ok=True)
source=Path('app/agent.py'); baseline=source.read_text()
old='- 回答の最後に、関係する回（第N回）を示す。'
new='- 回答の最後に「理解チェック：」という見出しと確認問題を1問示す。確認問題の答えは書かない。'
baseline=baseline.replace(new,old)
assert old in baseline
source.write_text(baseline)
(out/'agent_before.py.txt').write_text(baseline)
meta={'started_at':datetime.now(timezone.utc).isoformat(),'python':platform.python_version(),'model':os.getenv('AIE_MODEL','gemini-3.5-flash-lite'),'versions':{p:md.version(p) for p in ['pydantic-ai-slim','google-genai']},'runs':[]}
def run(label,module,question=None):
    cmd=[sys.executable,'-m',module]
    if module=='app.agent': cmd+=['--trace']
    if question is not None: cmd+=[question]
    print('RUN',label,flush=True)
    start=time.monotonic()
    p=subprocess.run(cmd,text=True,capture_output=True,timeout=150)
    text=p.stdout+p.stderr
    key=os.getenv('GEMINI_API_KEY','')
    if key: text=text.replace(key,'[REDACTED]')
    (out/(label+'.txt')).write_text(text)
    row={'label':label,'command':cmd[1:],'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3)}
    meta['runs'].append(row)
    (out/'metadata.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
    print(json.dumps(row,ensure_ascii=False),flush=True)
    print(text[-2200:],flush=True)
    if p.returncode: raise SystemExit('API run failed; inspect recorded output')
q='AIE2026の講座の宿題にある「3レベル」とは何ですか？'
run('plain','app.ask',q)
run('agent_course','app.agent',q)
run('before','app.agent','LoRAとQLoRAの違いは？')
run('quiz','app.agent','第2回の内容から確認問題を1問出して')
source.write_text(baseline.replace(old,new))
run('after','app.agent','LoRAとQLoRAの違いは？')
print('EXPERIMENTS_COMPLETE',flush=True)
