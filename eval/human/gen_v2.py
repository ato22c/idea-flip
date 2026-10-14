#!/usr/bin/env python3
"""사람 평가 2판(v2)용 답안을 만든다: 문제마다 '스킬 없음'과 '스킬'을 각각 N번씩 격리 실행.

  python eval/human/gen_v2.py [--samples 3] [--workers 6] [--model MODEL] [--ids N1 N2 ...]

공정성 원칙
- 두 쪽 모두 문제 원문 그대로만 준다. '창의적으로', '뻔한 답 말고', '새로운 접근' 같은 말을 따로 붙이지 않는다.
  (문제 원문 자체도 eval/problems_v2.json 에서 그런 표현을 뺀 단순 요청으로 쓴다.)
- 두 쪽의 차이는 시스템 지시뿐이다. 스킬 없음 = 최소 지시, 스킬 = 최소 지시 + 스킬 문서.
- 같은 모델·같은 조건·세션 지침/메모리 없이 실행한다(gen_isolated.py 의 run 을 그대로 쓴다).
- 이미 만들어진 파일은 건너뛴다(중간에 끊겨도 다시 돌리면 이어서 한다).

결과: eval/human/pairs_v2/<id>/{problem.txt, baseline_1..N.md, skill_1..N.md}
"""
import argparse, json, sys, tempfile, concurrent.futures as cf
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from gen_isolated import BASE_SYS, SKILL, skill_system, run  # noqa: E402

EVAL = HERE.parent
OUT = HERE / "pairs_v2"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--model", default="claude-fable-5-1")
    ap.add_argument("--ids", nargs="*", default=None)
    ap.add_argument("--problems", default=str(EVAL / "problems_v2.json"))
    a = ap.parse_args()

    problems = json.loads(Path(a.problems).read_text(encoding="utf-8"))
    if a.ids:
        problems = [p for p in problems if p["id"] in a.ids]
    tmp = Path(tempfile.mkdtemp(prefix="triz_v2_"))
    skill_sys = skill_system(SKILL)

    jobs = []
    for p in problems:
        d = OUT / p["id"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "problem.txt").write_text(p["text"], encoding="utf-8")
        for arm, sysp in (("baseline", BASE_SYS), ("skill", skill_sys)):
            for i in range(1, a.samples + 1):
                f = d / f"{arm}_{i}.md"
                if f.exists() and f.stat().st_size > 200:
                    continue
                jobs.append((p, arm, i, f, sysp))
    print(f"만들 답안 {len(jobs)}개 (문제 {len(problems)} × 쪽 2 × {a.samples}회, 이미 있는 것 제외)", flush=True)

    def work(job):
        p, arm, i, f, sysp = job
        res = run(sysp, p["text"], a.model, tmp, f"{p['id']}_{arm}_{i}")
        f.write_text(res, encoding="utf-8")
        return f"{p['id']} {arm}_{i}: {len(res)}자"

    done = 0
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, j): j for j in jobs}
        for fut in cf.as_completed(futs):
            j = futs[fut]
            try:
                done += 1
                print(f"[{done}/{len(jobs)}] {fut.result()}", flush=True)
            except Exception as e:  # 실패해도 나머지는 계속, 다시 돌리면 이어서
                print(f"[실패] {j[0]['id']} {j[1]}_{j[2]}: {e}", flush=True)
    print("끝", flush=True)


if __name__ == "__main__":
    main()
