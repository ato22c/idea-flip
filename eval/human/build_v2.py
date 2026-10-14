#!/usr/bin/env python3
"""사람용 A/B 블라인드 평가 페이지(2판)를 만든다.

  python eval/human/build_v2.py [--seed N] [--round 1] [--reply-to a@b.c] [--out PATH]

입력: eval/problems_v2.json, eval/human/pairs_v2/<id>/{baseline_i,skill_i}.md 와 각각의 .ideas.md
출력: 평가 페이지(html) + 정답표 eval/human/keys/key-r<회차>.json

정답표 분리(중요)
- 페이지에는 '어느 답이 스킬인지'가 들어 있지 않다. 답안마다 의미 없는 무작위 ID만 붙고,
  ID -> (문제, 쪽, 번호) 대응은 keys/ 의 key 파일에만 있다. 집계할 때(aggregate_v2.py) 합친다.
- keys/ 는 .gitignore 에 들어 있다. 평가가 끝나기 전에 key 를 공개하지 말 것.
- 쪽(스킬/스킬 없음)을 가리키는 '묶음'의 순서도 문제마다 무작위로 섞어서, 묶음 위치로 알아낼 수 없게 한다.
"""
import argparse, json, random
from pathlib import Path

HERE = Path(__file__).parent
EVAL = HERE.parent
PAIRS = HERE / "pairs_v2"
KEYS = HERE / "keys"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8").replace("\r\n", "\n").strip()


def js(obj):  # <script type=application/json> 안전화
    return json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--round", default="1")
    ap.add_argument("--reply-to", default="")
    ap.add_argument("--out", default=None)
    ap.add_argument("--problems", default=str(EVAL / "problems_v2.json"))
    a = ap.parse_args()
    rng = random.Random(a.seed)

    problems = json.loads(Path(a.problems).read_text(encoding="utf-8"))
    used = set()

    def new_id():
        while True:
            i = "".join(rng.choice("0123456789abcdef") for _ in range(8))
            if i not in used:
                used.add(i)
                return i

    data, key = [], {"round": a.round, "problems": {}, "answers": {}}
    for p in problems:
        d = PAIRS / p["id"]
        pools = {"baseline": [], "skill": []}
        for arm in pools:
            for f in sorted(d.glob(f"{arm}_[0-9]*.md")):
                if f.name.endswith(".ideas.md"):
                    continue
                ideas = f.with_suffix(".ideas.md")
                if not ideas.exists():
                    raise SystemExit(f"{ideas} 없음: 먼저 normalize_v2.py 를 돌리세요")
                aid = new_id()
                pools[arm].append({"id": aid, "full": read(f), "ideas": read(ideas)})
                key["answers"][aid] = {"problem": p["id"], "arm": arm, "file": f.name}
        if not pools["baseline"] or not pools["skill"]:
            raise SystemExit(f"{p['id']}: baseline/skill 답안이 모두 있어야 합니다")
        order = ["baseline", "skill"]
        rng.shuffle(order)  # 묶음 순서를 섞어 위치로 알아내지 못하게 한다
        data.append({"id": p["id"], "domain": p["domain"], "problem": p["text"],
                     "pools": [pools[order[0]], pools[order[1]]]})
        key["problems"][p["id"]] = {"domain": p["domain"], "dev": bool(p.get("dev"))}

    html = (HERE / "template_v2.html").read_text(encoding="utf-8")
    html = html.replace("__MARKED__", (HERE / "marked.min.js").read_text(encoding="utf-8").replace("</script", "<\\/script"))
    html = html.replace("__DATA__", js(data)).replace("__CFG__", js({"round": a.round, "replyTo": a.reply_to}))
    out = Path(a.out) if a.out else HERE / f"index-v2-r{a.round}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    KEYS.mkdir(exist_ok=True)
    kp = KEYS / f"key-r{a.round}.json"
    kp.write_text(json.dumps(key, ensure_ascii=False, indent=1), encoding="utf-8")
    n_ans = sum(len(p["pools"][0]) + len(p["pools"][1]) for p in data)
    print(f"built {out}  (문제 {len(data)}개, 답안 {n_ans}개, {out.stat().st_size // 1024} KB)")
    print(f"정답표(평가 끝날 때까지 공개 금지): {kp}")
    # 검증: 페이지 문자열에 arm 정보가 새지 않았는지
    leak = [w for w in ("baseline", "skill\"", "스킬 없음") if w in html.split('<script id="data"')[1].split("</script>")[0]]
    if leak:
        print("경고: 데이터 영역에 다음 단어가 보입니다(답안 본문에 우연히 있을 수 있음):", leak)


if __name__ == "__main__":
    main()
