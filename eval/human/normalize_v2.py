#!/usr/bin/env python3
"""답안에서 '아이디어만' 뽑아 같은 모양의 목록으로 바꾼다(평가 1단계: 아이디어 품질용).

  python eval/human/normalize_v2.py [--workers 6] [--model MODEL]

왜 필요한가
- 스킬 답은 표·이모지·카드·신호등이 있고 길이도 2배 안팎이라, 평가자가 어느 쪽이 스킬인지 알아보기 쉽고
  '이해하기 쉬움'이 구조적으로 불리하다. 그래서 아이디어 품질만 볼 때는 겉모양을 걷어낸 목록을 보여 준다.
- 쓰기 편함(2단계)은 원본 전체를 그대로 보여 준다.

규칙(두 쪽에 똑같이 적용, 변환기는 어느 쪽 답인지 모른다)
- 답이 제안하는 주요 아이디어만 뽑는다. 답이 가장 강조한 순서대로 '정확히 4개'(개수로 쪽을 알아내지 못하게 맞춘다).
- 제외 목록·접어 둔 아이디어·근거·부록·질문 목록은 뺀다.
- 각 아이디어는 '짧은 제목 — 한두 문장(누가 무엇을 어떻게)', 설명은 100~130자 안팎(분량 단서를 줄인다).
  이모지·표·점수·신호·실험·약한 고리 같은 부가 정보는 뺀다.
- 원문에 없는 내용을 더하거나 고치지 않는다. 평가하지 않는다.

결과: pairs_v2/<id>/<이름>.ideas.md
"""
import argparse, sys, tempfile, concurrent.futures as cf
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from gen_isolated import run  # noqa: E402

OUT = HERE / "pairs_v2"

SYS = """너는 글에서 '제안된 아이디어'만 뽑아 같은 모양으로 정리하는 편집자야. 다음 규칙을 정확히 지켜.

1. 입력은 어떤 문제에 대한 답변이야. 그 답변이 사용자에게 제안하는 주요 아이디어만 뽑아.
2. 답변이 가장 강조한 순서대로 정확히 4개를 뽑아. 5번째 이후 아이디어는 버려. 4개보다 적게 제안했으면 있는 만큼만 써.
3. 제외 목록(버린 흔한 답), 접어 둔·보류한 아이디어, 근거·원인 분석·부록, 토론 질문 목록은 아이디어로 치지 마.
4. 형식은 아래 하나뿐이야. 번호 매긴 목록으로, 각 줄을 이렇게 써:
   1. **짧은 제목** — 무엇을 어떻게 하는지 한두 문장. (누가 무엇을 하는지 보이게)
   설명은 공백 포함 100~130자 안팎으로 맞춰. 더 길면 줄이고, 이미 짧으면 그대로 둬.
5. 이모지, 표, 점수, 신호(색깔), 실험 기준, 실패 조건, 제목 표기 같은 겉모양과 부가 정보는 모두 빼.
6. 원문에 없는 내용을 더하거나 고치거나 평가하지 마. 원문 표현을 가능한 한 살려 줄여 써.
7. 인사말, 설명, 머리말 없이 목록만 출력해."""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--model", default="claude-fable-5-1")
    ap.add_argument("--force", action="store_true", help="이미 있는 .ideas.md 도 다시 만든다")
    a = ap.parse_args()
    tmp = Path(tempfile.mkdtemp(prefix="triz_norm_"))
    jobs = []
    for d in sorted(x for x in OUT.iterdir() if x.is_dir()):
        for f in sorted(d.glob("*_[0-9]*.md")):
            if f.name.endswith(".ideas.md"):
                continue
            o = f.with_suffix(".ideas.md")
            if o.exists() and o.stat().st_size > 50 and not a.force:
                continue
            jobs.append((f, o))
    print(f"정리할 답안 {len(jobs)}개", flush=True)

    def work(j):
        f, o = j
        txt = f.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
        res = run(SYS, txt, a.model, tmp, f"{f.parent.name}_{f.stem}")
        o.write_text(res, encoding="utf-8")
        return f"{f.parent.name}/{f.name}: {len(res)}자"

    done = 0
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, j): j for j in jobs}
        for fut in cf.as_completed(futs):
            done += 1
            try:
                print(f"[{done}/{len(jobs)}] {fut.result()}", flush=True)
            except Exception as e:
                print(f"[실패] {futs[fut][0].name}: {e}", flush=True)
    print("끝", flush=True)


if __name__ == "__main__":
    main()
