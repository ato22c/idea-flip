---
name: idea-flip
description: >
  Ideation skill for when you need ideas: contrarian or reverse-thinking, innovative, fresh or creative ideas, "just
  give me some ideas", a non-obvious approach, or a new way out of a stuck problem. Under the hood it uses TRIZ to strip
  out the AI's "safe answer" first, then forces candidates from unexpected directions (contradictions, Ideal Final
  Result, 40 inventive principles, extremizing). The user does not need to know TRIZ. Triggers: "give me ideas",
  "contrarian idea", "innovative idea", "fresh idea", "is there a new way", "I'm stuck", "not the obvious answer",
  "out-of-the-box", "TRIZ", and Korean: "아이디어 내줘", "아이디어 만들어줘", "역발상", "혁신적인 아이디어",
  "참신한 아이디어", "고정관념 깨는", "새로운 방법 없을까", "막혔어", "뻔한 답 말고", "발상 전환", "트리즈로", and "모순 해결"
  when it means finding a new approach (not data conflicts or merge conflicts). NOT for requirements
  interviews, implementation planning, plan review, code bug diagnosis, or scheduling.
---

# TRIZ Ideation

**Purpose:** Produce candidates beyond the safe answer. For principles and sources see [40 principles](reference/principles.md)
and [tools](reference/tools.md).

## Why it works this way

- The AI converges on the most plausible = most common answer. Thinking harder only circles near the same answer.
- So **replace the starting point with a procedure.** If principles are assigned by list instead of picked by the AI,
  the starting point moves to directions it normally avoids.
- Three rules: (1) write down the common answers first and discard them; (2) no realism judging during divergence;
  (3) use the principle assigned, not the one that appeals.

## Modes

| Mode | When | Sweep range | Minimum ideas |
|---|---|---|---|
| Quick (default) | everyday or light problems, little time | 2 each from 5 directions (10 total) | 15 |
| Deep | "do it properly", important decisions, long-stuck problems | all 40 | 30 |

If the user does not say, use quick. If the result is thin, ask on the last line of Next steps whether to go deeper.

## Response size

Depth (the modes above) is separate from size. Read what the user asks for:

- **Brief** ("short", "briefly", "just the gist", "한 줄로", "간단히", "짧게"): run the whole procedure silently, then output only (a) the bold conclusion sentence, (b) the "🧩 The core conflict" line, (c) the "📋 At a glance" table with its four rows (the last row is always "🎲 Wildcard: idea name", with only the word "Wildcard" translated into the user's language, e.g. "🎲 와일드카드: …" for Korean; never drop or leave it in English), and (d) card ① with only "A scene" and "First experiment". Write exactly one card: do not write cards ②, ③ or the wildcard card (the table rows are their only trace) and do not write "The catch", the crossed-out common answers or the pitch. Finish with one line saying a card number can be sent back to expand it. No reasoning, appendix or team questions. At most about 250 words.
- **Detail** (the user names one idea from your earlier answer: "detail ②", "expand the wildcard", "자세히 ③", "구체적으로 2번"): do not redo the procedure and do not list other ideas. Write only that idea: its card title, then "Steps" (3 to 6 short steps, each with who does it and when), "What you need" (people, time and money in numbers), "How to tell it works" (one number and a date), "If it goes wrong" (one fallback) and "First 24 hours" (the single smallest first move). At most about 450 words. Translate these labels into the user's language like every other label. If there is no earlier answer to expand, treat the request as a normal one.
- **Page** (the user asks for the result as a page, document, report or artifact: "as a page", "as an artifact", "make it a document", "페이지로", "아티팩트로", "문서로 뽑아줘", "보기 좋게 만들어줘"): run the whole procedure and write the same content as the normal format, in the same order, but as one self-contained HTML page built from [page template](reference/page-template.html). Fill in the template; do not redesign it. Every `{{…}}` placeholder must be replaced with text in the user's language (translate each heading and field label like everywhere else) and none may remain. Banner: under the reason, the `.dead` line shows the three crossed-out common answers as chips. Cards use the rows scene, catch and test (the scene row has class `scene`). Between the cards and the next steps put the pitch block (one sentence in `#say`, a copy button, two objection and answer pairs). The `<h1>` holds only the action as a short phrase (about 40 characters or fewer, no reason clause, for example "먼저 1인분 소포장부터 시작하세요" in Korean), and the `.reason` paragraph under it gives the reason in one short sentence (about 40 characters or fewer). The bold conclusion sentence in the chat reply stays as in the normal format. Cards: the number goes in the round badge (1, 2, 3) and the `<h3>` holds only the idea name; the start signal (emoji plus word, the same text as the table's last cell) goes in the pill. Card ① gets the class `lead`. Keep the wildcard rule: the last card has class `risk`, the badge holds `🎲`, and its `<h3>` is the translated word for "Wildcard", a colon and the idea name. The reasoning and appendix go inside the collapsed `<details>` blocks. Page text follows the plain-language rules. The only external request allowed is the Google Fonts stylesheet already in the template; the page must read fine without it. No other external files, fonts or scripts. Deliver it in the first way that works: (1) if you can publish or render a page (for example an artifact tool), do that and reply with only the bold conclusion sentence and the link; (2) otherwise save it as `idea-flip-<short-topic>.html` in the current folder and reply with the conclusion sentence and the file path; (3) otherwise reply with the conclusion sentence and the full HTML in one code block. Do not repeat the cards in the chat reply.
- **Markdown file** (the user asks for a markdown or md file: "as a markdown file", "as md", "md 파일로", "마크다운으로 저장", "문서 파일로"): write the normal format below, unchanged and in the same order, and deliver it as a file. The file starts with one line `# ` plus a short topic name (no explanation after it), then the answer exactly as in the normal format (the bold conclusion sentence first). Deliver it in the first way that works: (1) save it as `idea-flip-<short-topic>.md` in the current folder and reply with the bold conclusion sentence and the file path; (2) otherwise reply with the bold conclusion sentence and the full markdown in one code block. If the user also asked for a page, do both. All other rules still apply (the user's language, plain language, no TRIZ terms in sections 1 to 3).
- Anything else: the normal format below.

All other rules still apply (the user's language, plain language, no TRIZ terms).

## Procedure

**0. Input** — Answer entirely in the language the user wrote in, including card titles, field labels (A scene / The catch / First experiment / Likely objection / How to answer), section headings (Next steps / Reasoning / Appendix) and principle tags, translating principle names into that language. Never mix English labels into a non-English answer.
Ask questions only when the goal is too vague to state in one sentence (at most 3: goal, constraints, what has been tried).
Otherwise do not ask: write down your assumptions and proceed. Put whatever the user has already tried on the ban list first.
**Ideate independently.** Do not anchor on ideas or solutions that appeared earlier in this conversation or in the session's project notes; generate as if starting fresh. Follow any formatting or tone the user explicitly asked for. Keep using only the facts and constraints the user stated, and put any solution already proposed earlier in the conversation on the ban list.

**1. Redefine as a function** — State "what are we trying to achieve" in one sentence, with no solution nouns.
Ask "why?" twice to widen the goal; if the wider goal can be solved, switch to that sentence.
Write down the user's stated **constraints** (budget, people, time, things that must not change) separately. Recommendations must respect them.
Write the **cause** of why this problem occurs in one line ("Because of A, B happens"). If you do not know the cause,
say it is a guess, and add one line on how the answer would change if that guess is wrong.

**2. Obvious-answer dump** — Before using any device, write the 5–8 answers that come to mind. This is the **ban list**.
From here on, anything with the same mechanism as a ban-list item does not count as a novel idea.

**3. IFR and resources** — Write in one sentence "ideally the goal is achieved by itself, with no cost or device,"
and find 5 or more resources that already exist for free (people, time, data, waste, idle space).
Among them, always include at least one from a **nuisance, waste, or constraint** (something that is a burden now) that can be used in reverse. → [tools](reference/tools.md#ifr-and-resources)

**4. Contradiction formulation** — (a) Technical contradiction: "Improving A makes B worse." (b) Physical contradiction: "X must be P
and at the same time must not be P." For a physical contradiction, resolve it with the four separations (time, space, condition, level).
If no real contradiction is visible, write "no contradiction (plain optimization problem)" and go to 5. Do not force one.
If you wrote a contradiction, give each recommendation one line in the Reasoning section on "which side of this contradiction it resolves and how."
At least 1 of recommendations ①②③ must directly resolve one side of the contradiction. For a recommendation not connected to the contradiction,
do not force a link; instead write one line on where it came from (which resource from step 3, which extremizing tool).

**5. Forced divergence** — Apply the principles to the problem one by one over the mode's sweep range and write ideas.
- Generate from the principle's prompt question, not from earlier ideas in the conversation. Tag each idea `[principle name]`. Tag only an idea that **actually started** from that principle's prompt question.
  Thinking of the idea first and then attaching a fitting principle is forbidden.
  If it is a stretch, leave `SKIP(reason)` and move on. 2–3 SKIPs in a sweep is normal.
- Write absurd ideas too. Deleting an idea for being "unrealistic" is forbidden at this stage.
- After the sweep, use **at least 2** extremizing tools: size/time/cost 0/∞, 9 windows, doing it backwards,
  far-field analogy, flipping obvious assumptions, starting with no resources. → [tools](reference/tools.md#extremizing-tools)
- Variants of the same mechanism count as 1. Do not count SKIPs or variants to reach the number. Keep only the titles of the divergent list in the appendix.

**6. Bridging** — From the 3 most absurd ideas, pull out **the core mechanism in one line**, and build a
realistic version that keeps only that.

**7. Convergence** — Score each candidate 1–5 on novelty (distance from the safe answer), doability (can it start tomorrow within the constraints),
and effect (does it really solve the problem), then fill the recommendations like this:
- **① An idea to start tomorrow** — the idea with the highest doability and effect. Even better if it can start as a small step, such as one setting
  or one line of wording. It may be a sharpened version of a common answer, but it must actually solve the problem the user stated.
- **②③ New ideas** — ideas whose **operating mechanism** differs from the safe-answer list and that can actually work.
- **Wildcard** — the strangest idea. State that it is risky and attach a cheap experiment.
- **Operating mechanism = "what removes the problem."** If only position, shape, strength, count, or name differs, it is the same mechanism.
  For ②③ and the wildcard, silently write for each candidate "closest common answer: ○○ / what differs in mechanism: □□";
  if you cannot write □□, treat it as a variant and move it down to ① or to a supporting idea.
- Attach to each idea **one condition where it fails** and **one first experiment**. The experiment states who tries it, for how long, and what
  number means continue. For ideas that need development, start with a hand-made version (paper mockup, manual sending).
- Novelty 4 or higher goes to at most half of the candidates, and a 5 to at most one.

## Output format (in this order, conclusion first)

The only visible headings are the card titles and the headings for the at-a-glance table, next steps, team questions (only when used), reasoning and appendix, all named in the user's language (for an English user: "📋 At a glance", "Next steps", "Reasoning", "Appendix"). Never write internal labels anywhere, such as "One-line conclusion", "Recommendation slots",
the mode name, the number of principles, or "closest common answer / what differs in mechanism".

1. **Conclusion** — "Start with ○○ first. The reason is △△." Write one bold sentence on the very first line with no label or heading.
   Do not list assumptions at length; put them in one line in section 4.
2. **At-a-glance table + four recommendation cards (①, ②, ③, wildcard)** — first one line "🧩 The core conflict: …" that states the conflict in plain words ("doing A makes B worse"; no TRIZ terms, never the word "contradiction"), then one line "✗ Common answers: ~~a~~, ~~b~~, ~~c~~" (translate "Common answers") with the three most typical items from the ban list, each in markdown strikethrough, then one table titled "📋 At a glance" (translate the title; columns: idea, one-line summary (about 6 words), start; one row per card).
   The start column is 🟢 start tomorrow / 🟡 within this month / 🔴 risky, test small (the wildcard is always 🔴). Then each card in the format below (within 4 lines).
   Card titles are a number, a name and the signal like "① Idea name 🟢"; the wildcard is "🎲 Wildcard: idea name" — translate the word "Wildcard" but never rename or drop it (no "surprise card" or "wild idea"), and use the same word in its table row. Separate cards with `---`. Do not use TRIZ terms or principle names. The reader must be able to decide and act from this section alone. Follow the **plain-language rules** under "Writing in plain language" below.
   Write every heading, table header and field label in the user's language; if that language is not English, no English label may remain anywhere in the answer, so check the headings once before sending. Translate "The core conflict", "At a glance", "A scene", "The catch", "First experiment", "Common answers", "How to pitch it", "Likely objection", "How to answer", "Next steps", "Reasoning" and "Appendix".
   ```
   ### ① Idea name (one line)
   - 🎬 A scene: two short sentences that show the idea in use at a concrete moment ("Tomorrow at 12, …"): who does what and what the person it is for sees happen. Use only facts and constraints the user stated; invent no numbers, names or case studies.
   - ⚠️ The catch: one short sentence naming the weakest assumption this idea rests on. Do not name or compare with the common answer here.
   - 🧪 First experiment: who, for how long → what number means continue
   ```
   The wildcard card uses the same fields but its title line is exactly "### 🎲 Wildcard: idea name" and its table row starts with "| 🎲 Wildcard: idea name" (translate only the word "Wildcard", in both places).
2b. **How to pitch it** (translate this heading; "💬" in front) — for idea ① only, because the reader usually has to convince someone else. One bold sentence the reader can say to the person who must approve it: what to do, why it helps, and the smallest first step. Then two lines of "Likely objection: …" each followed by "How to answer: …" (one sentence each). Answers use only facts the user stated or the card already shows; invent nothing. Skip this block in brief and detail answers.
3. **Next steps** (translate this heading into the user's language) — within 3 lines, the last one being a short hint that sending a card number (for example "detail ②") expands that idea and "brief" gives a shorter version. If the cause of the problem is still unknown, the first line is "check as cheaply as possible whether the cause matches my guess."
   Only when the problem is about a team, a meeting or a group decision, add a short block "Questions to ask the team" (translate the heading): 2 or 3 one-sentence questions the reader can ask out loud, each tailored to this problem, covering (a) how we could make this fail on purpose, then do the opposite, (b) what we would try if one constraint (budget, time, a rule) vanished, (c) which idle resource or leftover we are ignoring.
4. **Reasoning (short)** (translate this heading too) — within 8 lines in total: the problem redefinition, your assumptions and the user's constraint list, and for each recommendation one line on how it resolved the core conflict or where it came from (resource or tool), plus the closest common answer it differs from.
5. **Appendix (within 12 lines)** (translate this heading too) — the safe-answer list and the titles of divergent ideas (`[principle name] idea`). Use technical terms only here,
   and explain each in parentheses the first time it appears. Do not use arrows or emoji; write sentences (emoji only in the table and card labels).
   End the appendix with the two most novel ideas you set aside, one line each with the reason (for example "too costly" or "needs the leader's consent"), so the reader can revive them.

**Length:** no more than about 1,000 words in quick mode, about 1,800 words in deep mode (brief and detail answers follow their own limits under "Response size"). If over, cut the appendix first. Sections 1–3 are at least 70% of the text.
Quality is the clarity of sections 1–2, not length.

**Final check before sending:** read every heading, table header and field label in your answer (in a page, also the `<title>`, the `<summary>` texts and the table header cells). If any is in a language other than the user's, rewrite it now.

## Writing in plain language

The result must make sense to a colleague who does not know the field. Sections 1–3 (conclusion, recommendations, next steps) most of all.

- Keep sentences short (about 20 words or fewer), one idea per sentence.
- Choose everyday words over jargon, abbreviations and industry terms. A term the user used first can stay, but explain any other
  technical term in one line the first time it appears.
- Avoid abstract, stiff phrasing ("leverage to facilitate"); say who does what with a subject and a verb.
- Cut arrows (→), slashes, nested parentheses and numbered lists. Split into two or three short sentences if needed.
- Write numeric criteria so they can be pictured at once (how many out of how many people, for how many days, how many times out of how many).
- Write the conclusion sentence so that "what to do" is visible first.

## Do not

- Do not fill contradiction matrix (39×39) cells from memory. Filling them without a source is fabrication. This skill uses the principle sweep.
- Do not pretend a principle fits. If it does not fit, SKIP.
- Do not produce output that leaves the user unable to decide (long with no conclusion). The conclusion comes first.
- Assume the user does not know TRIZ. Terms like IFR, contradiction, separation, 9 windows and principle numbers appear only in section 4 and below (Reasoning, Appendix),
  with a one-line explanation in parentheses the first time. Never in sections 1–3 (conclusion, recommendations, next steps).
