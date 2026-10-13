# 🙃 idea-flip — 뻔한 답 말고, 진짜 다른 아이디어

**English: [README.md](README.md)**

> AI에게 "아이디어 내줘" 하면 늘 비슷한 무난한 답이 나오죠?
> 이 스킬은 **뻔한 답을 먼저 적어서 금지**시키고, 일부러 엉뚱한 방향에서 후보를 뽑아
> **내일 시작할 수 있는 작은 실험**까지 붙여 줍니다. (속은 TRIZ인데, 몰라도 됩니다.)

에이전트 스킬(`SKILL.md`)입니다. Claude Code로 만들고 시험했고, 지침이 일반 텍스트라 다른 AI 채팅·에이전트에 붙여 써도 됩니다. 한국어로 물으면 한국어로, 영어로 물으면 영어로 답합니다.

## 한눈에 보기

같은 질문: *"앱 푸시 알림을 늘리면 재방문은 늘지만 알림을 끄는 사용자도 늘어요. 새로운 접근법은?"*

| 스킬 없이 | `/idea-flip` 사용 |
|---|---|
| "사용자별 상한, 시간대 조정, 종류별 끄기" 같은 **누구나 떠올리는 답** | 먼저 그런 답을 **금지 목록**으로 적어 버림 |
| 목록이 길게 나열됨 | **결론이 맨 첫 줄**: "내일은 이것부터 해보세요" |
| 해보라는 말만 있음 | 안마다 **안 통하는 조건 + 숫자 기준이 있는 싼 실험** |
| 늘 비슷한 방향 | 알림의 **발신자를 '회사'에서 '사용자 본인'으로** 바꾸는 식의 다른 방향 + 위험하다고 밝힌 **와일드카드** 1개 |

> 예: "사용자가 직접 '이거 내일 알려줘'를 주문한 알림만 보낸다. 자기가 예약한 알림은 끄지 않는다."
> 실험: *버튼만 한 화면에 달고 1주 → 방문자의 5% 이상이 누르고 열람률이 일반 알림의 2배면 정식 개발.*

실제 답안 전체: [`eval/human/pairs/D2/`](eval/human/pairs/D2) (baseline.md = 스킬 없음, skill.md = 스킬 사용)

## 설치 (1분)

**방법 1 — 플러그인 (추천)**

```
/plugin marketplace add ato22c/idea-flip
/plugin install idea-flip@idea-flip
```

**방법 2 — 파일 복사**

```bash
git clone https://github.com/ato22c/idea-flip
cp -r idea-flip/skills/idea-flip ~/.claude/skills/
```

**방법 3 — 다른 AI 도구 (ChatGPT, Gemini, Cursor, Codex 등)**

[`SKILL.md`](skills/idea-flip/SKILL.md)와 [`reference/`](skills/idea-flip/reference)의 파일 2개를 도구의 사용자 지침·프로젝트 지식·규칙 파일에 넣거나, 대화 맨 처음에 붙여 넣은 뒤 문제를 말하면 됩니다.
Claude에서만 시험했고, 다른 모델에서는 결과가 다를 수 있습니다.

## 사용법

슬래시로 부르거나, 그냥 말로 해도 됩니다. 플러그인으로 설치했다면 슬래시 명령이 `/idea-flip:idea-flip`처럼 길게 보일 수 있습니다. TRIZ를 몰라도 됩니다.

```
/idea-flip 책상이 3일이면 다시 어질러져요. 정리 습관 말고 다른 방법 없을까요?
역발상 아이디어 좀 내줘 — 우리 주간회의가 90분인데 지루하고, 없앨 수는 없어요
뻔한 답 말고 다른 방법 없을까? 막혔어
```

- 기본은 **빠르게** 모드. "제대로 깊게 해줘"라고 하면 발명원리 40개를 전부 훑는 **깊게** 모드로 돌아갑니다.
- 팀·회의 문제면 **팀에게 던질 질문**도 같이 줍니다.

## 어떻게 다른가

1. **뻔한 답 먼저 버리기** — 흔한 답을 적어 금지 목록으로 만들고, 그 변형은 새 아이디어로 치지 않음
2. **출발점 강제 변경** — AI가 고르지 않고, 40가지 발명원리를 *배정대로* 문제에 대 봄
3. **와일드카드** — 가장 엉뚱한 안 1개. 항상 "위험하다"고 밝히고 싼 실험을 붙임
4. **끝에는 실험** — 안마다 안 통하는 조건과 숫자 기준이 있는 첫 실험

## 솔직하게 말하면

- AI 블라인드 채점에서는 스킬 답이 크게 앞섰지만(86 vs 46점), **사람 평가는 1명**이고 결과가 엇갈렸습니다.
  지금은 "더 창의적"이라고 약속하지 않고, **"흔한 답을 먼저 걷어내고 엉뚱한 안을 위험·실험과 함께 받는 절차"** 라고 말합니다.
- 답이 스킬 없이 받는 것보다 깁니다(분량 상한을 뒀지만 그래도 깁니다).
- 같은 질문을 여러 번 돌리면 비슷한 안이 반복되는 경향이 있습니다.

시험문제, 채점표, 26번 고친 기록(효과 없어서 되돌린 것 포함), 한계 전체는 → **[docs/EVALUATION.md](docs/EVALUATION.md)**

## 구성

```
skills/idea-flip/SKILL.md           절차·출력 형식
skills/idea-flip/reference/         40원리, IFR·자원·모순·분리 도구
.claude-plugin/                플러그인·마켓플레이스 설정
eval/                          시험문제·채점 하네스·회차별 원본 답안
docs/EVALUATION.md             평가 기록과 한계
```

## 참고한 자료

- 알트슐러의 40 Inventive Principles. 비물리 분야 해석은 Mann & Domb, *40 Inventive (Business) Principles*와 Kevin Rea, *TRIZ and Software*를 참고해 **자체 표현**으로 다시 썼습니다.
- [truinorva/triz-skills](https://github.com/truinorva/triz-skills), [smixs/creative-director-skill](https://github.com/smixs/creative-director-skill), [athola/claude-night-market](https://github.com/athola/claude-night-market) — 아이디어만 참고(코드·문장 복사 없음). 자세한 내용은 [docs/EVALUATION.md](docs/EVALUATION.md#참고한-자료와-벤치마킹).
- [Verbalized Sampling (arXiv 2510.01171)](https://arxiv.org/abs/2510.01171) — AI가 흔한 답으로 수렴하는 문제의식

## 라이선스

MIT
