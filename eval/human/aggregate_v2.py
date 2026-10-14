#!/usr/bin/env python3
"""사람 평가 2판의 결과(JSON들)와 정답표(key)를 합쳐 익명으로 집계한다.

  python eval/human/aggregate_v2.py <JSON이 든 폴더> --key eval/human/keys/key-r1.json [--out summary.json]

- 평가자 이름은 출력하지 않고 R01, R02…로 바꾼다. 코멘트 원문은 요약에 넣지 않는다.
- 이 평가는 '아이디어 품질'(아이디어만 같은 모양으로 정리한 목록)만 잰다. 쓰기 편함·읽기 쉬움은 재지 않는다.
- 신뢰구간은 '평가자 단위'로 다시 뽑아(부트스트랩) 계산한다. 평가자 한 사람의 판단들은 서로 독립이 아니기 때문이다.
- 답안 3개씩의 편차(운)를 보려고, 쪽별 답안 번호마다 승패도 따로 보여준다.
- 개발 문제(problems_v2.json 의 dev=true)와 비개발 문제를 나눠서도 본다.
"""
import argparse, json, random
from pathlib import Path

CRIT = {"new": "새로움", "do": "실행 가능성", "fit": "내 문제에 맞음"}


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs) if xs else float("nan")


def boot_ci(per_rater, stat, n=4000, seed=1):
    """per_rater: [평가자별 데이터]. 평가자를 복원추출해 stat(합친 데이터)의 95% 구간."""
    rng = random.Random(seed)
    vals = []
    for _ in range(n):
        s = [rng.choice(per_rater) for _ in per_rater]
        v = stat(s)
        if v == v:
            vals.append(v)
    vals.sort()
    if not vals:
        return (float("nan"), float("nan"))
    return vals[int(len(vals) * 0.025)], vals[int(len(vals) * 0.975) - 1]


def sign_flip_p(vals, n=20000, seed=2):
    vals = [v for v in vals if v == v]
    if not vals:
        return float("nan")
    rng = random.Random(seed)
    obs = abs(mean(vals))
    hit = sum(abs(mean([v if rng.random() < .5 else -v for v in vals])) >= obs - 1e-12 for _ in range(n))
    return hit / n


def complete(r):
    if r.get("winner") not in ("A", "B", "tie"):
        return False
    return all(str(r.get(f"{k}_{c}", "")).strip() != "" for k in "AB" for c in CRIT)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--key", required=True)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    key = json.loads(Path(a.key).read_text(encoding="utf-8"))
    # 정답표는 쪽 이름을 baseline/skill 로 적는다. 집계 안에서는 base/skill 로 쓴다.
    ans = {i: dict(v, arm=("base" if v["arm"] == "baseline" else v["arm"])) for i, v in key["answers"].items()}
    dev = {pid: v["dev"] for pid, v in key["problems"].items()}

    raters = [json.loads(f.read_text(encoding="utf-8")) for f in sorted(Path(a.folder).glob("*.json"))]
    print(f"평가자 {len(raters)}명 (회차 {key.get('round')})  ※ 아이디어 품질만 측정한 결과입니다(쓰기 편함은 측정하지 않음)")

    P, dropped = [], 0  # 평가자별 판단 목록
    for rows in raters:
        L = []
        for r in rows:
            if not complete(r):
                dropped += 1
                continue
            A, B = ans.get(r["A_id"]), ans.get(r["B_id"])
            if not A or not B or A["arm"] == B["arm"]:
                dropped += 1
                continue
            arm = {"A": A, "B": B}
            w = r["winner"]
            win = "tie" if w == "tie" else arm[w]["arm"]
            sk = "A" if A["arm"] == "skill" else "B"
            ba = "B" if sk == "A" else "A"
            L.append({"pid": r["id"], "win": win, "slot": w,
                      "skill": {c: int(r[f"{sk}_{c}"]) for c in CRIT},
                      "base": {c: int(r[f"{ba}_{c}"]) for c in CRIT},
                      "skill_ans": arm[sk]["file"], "base_ans": arm[ba]["file"]})
        P.append(L)
    allj = [x for L in P for x in L]
    wins = {"skill": 0, "base": 0, "tie": 0}
    for x in allj:
        wins[x["win"]] += 1
    decided = wins["skill"] + wins["base"]
    rate = wins["skill"] / decided if decided else float("nan")

    def win_rate(sample):
        s = sum(1 for L in sample for x in L if x["win"] == "skill")
        b = sum(1 for L in sample for x in L if x["win"] == "base")
        return s / (s + b) if s + b else float("nan")
    lo, hi = boot_ci([L for L in P if L], win_rate)
    print(f"\n판단 {len(allj)}건 (불완전·오류 {dropped}건 제외)")
    print(f"승패: 스킬 {wins['skill']} · 스킬 없음 {wins['base']} · 비슷함 {wins['tie']}"
          f"  → 스킬 승률(비김 제외) {rate:.0%}  95% 구간 [{lo:.0%}, {hi:.0%}] (평가자 단위)")
    slot = {"A": 0, "B": 0, "tie": 0}
    for x in allj:
        slot[x["slot"]] += 1
    print(f"위치 편향 점검: A {slot['A']} · B {slot['B']} · 비슷함 {slot['tie']}")

    by_p = {}
    print("\n[문제별]")
    for pid in sorted({x["pid"] for x in allj}):
        xs = [x for x in allj if x["pid"] == pid]
        w = {"skill": 0, "base": 0, "tie": 0}
        for x in xs:
            w[x["win"]] += 1
        by_p[pid] = {"n": len(xs), "wins": w, "dev": dev.get(pid)}
        print(f"  {pid} [{'개발' if dev.get(pid) else '비개발'}] n={len(xs):>2}  스킬 {w['skill']:>2} / 없음 {w['base']:>2} / 비슷 {w['tie']:>2}")

    grp = {}
    for name, flag in (("비개발", False), ("개발", True)):
        xs = [x for x in allj if bool(dev.get(x["pid"])) == flag]
        s = sum(1 for x in xs if x["win"] == "skill"); b = sum(1 for x in xs if x["win"] == "base")
        grp[name] = {"skill": s, "base": b, "tie": len(xs) - s - b}
        print(f"  [{name} 문제 합계] 스킬 {s} / 없음 {b} / 비슷 {len(xs) - s - b}")

    per_ans = {}
    for x in allj:
        for arm in ("skill", "base"):
            d = per_ans.setdefault((x["pid"], arm, x[f"{arm}_ans"]), {"win": 0, "loss": 0, "tie": 0})
            if x["win"] == "tie":
                d["tie"] += 1
            elif x["win"] == arm:
                d["win"] += 1
            else:
                d["loss"] += 1
    print("\n[답안별 승-패]  (같은 쪽 3개 답안이 서로 얼마나 다른지)")
    for pid in sorted({k[0] for k in per_ans}):
        cells = []
        for arm, nm in (("skill", "스킬"), ("base", "없음")):
            ks = sorted(k for k in per_ans if k[0] == pid and k[1] == arm)
            cells.append(nm + " " + " ".join(f"{per_ans[k]['win']}-{per_ans[k]['loss']}" for k in ks))
        print(f"  {pid}: " + " | ".join(cells))

    crit_out = {}
    print("\n[항목별 평균 (1~5)]  차이 = 스킬 − 스킬 없음, 평가자 단위 95% 구간·부호 뒤집기 p")
    for c, label in CRIT.items():
        sk = [x["skill"][c] for x in allj]; ba = [x["base"][c] for x in allj]
        diffs = [mean([x["skill"][c] - x["base"][c] for x in L]) for L in P if L]
        d_lo, d_hi = boot_ci([[d] for d in diffs], lambda s: mean([r[0] for r in s]))
        p = sign_flip_p(diffs)
        crit_out[c] = {"skill": mean(sk), "base": mean(ba), "diff": mean(diffs), "ci95": [d_lo, d_hi], "p": p}
        print(f"  {label:<10} 스킬 {mean(sk):.2f} · 없음 {mean(ba):.2f} · 차이 {mean(diffs):+.2f}  [{d_lo:+.2f}, {d_hi:+.2f}]  p={p:.3f}")

    if a.out:
        Path(a.out).write_text(json.dumps({"raters": len(raters), "judgments": len(allj), "wins": wins,
                                           "skill_win_rate_excl_ties": rate, "ci95": [lo, hi], "by_problem": by_p,
                                           "by_group": grp, "criteria": crit_out}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\n요약 저장: {a.out}")


if __name__ == "__main__":
    main()
