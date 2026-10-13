# 🙃 idea-flip — skip the obvious answer, get a genuinely different idea

**한국어: [README.ko.md](README.ko.md)**

> Ask an AI for ideas and you get the same safe answers every time.
> This skill **writes the obvious answers down first and bans them**, forces candidates from unexpected directions,
> and attaches **a cheap first experiment you can start tomorrow**. (TRIZ under the hood — you don't need to know it.)

An agent skill (`SKILL.md`) — built and tested with Claude Code, and the instructions are plain text, so they also work pasted into other AI chats and agents. It answers in the language you write in (Korean or English).

## What you get

Input: *"Our weekly meeting is 90 minutes and boring, but we can't cancel it."* — real output, trimmed ([full text](eval/runs/v26/meeting_en.md)):

> **Keep the 90-minute slot, but stop making all 10 people listen to everyone's status. Collect status in writing before the meeting, and use the live time only for the few places where two people's work touches.**
>
> 🧩 The core conflict: if everyone hears everything, nobody duplicates work but everyone is bored. If we cut the listening, people get bored less but lose track of each other.
>
> | Idea | One-line summary | Start |
> |---|---|---|
> | ① Written status, live overlaps only | Fill a sheet first, discuss only matches | 🟢 start tomorrow |
> | ② The weekly matchmaker | One person reads all 10 and picks the pairs | 🟡 within this month |
> | ③ Present your partner's work | Pairs interview, then report each other | 🟡 within this month |
> | 🎲 Wildcard: the meeting is the gate | New work only starts after it is claimed there | 🔴 risky, test small |
>
> **① 🧪 First experiment:** whole team, 2 weeks. Continue if at least 8 of 10 fill the sheet on time and the team finds at least 1 overlap per week.
> **⚠️ Where it fails:** people skip the sheet or write vague lines like "various tasks."

Every idea comes with *where it fails* and *a cheap experiment with a numeric bar*. The wildcard is always flagged risky.

Side-by-side "without the skill vs with the skill" answers are in [`eval/human/pairs/`](eval/human/pairs) (the test problems there are in Korean).

## Install (1 minute)

**Option 1 — plugin (recommended)**

```
/plugin marketplace add ato22c/idea-flip
/plugin install idea-flip@idea-flip
```

**Option 2 — copy the files**

```bash
git clone https://github.com/ato22c/idea-flip
cp -r idea-flip/skills/idea-flip ~/.claude/skills/
```

**Option 3 — other AI tools (ChatGPT, Gemini, Cursor, Codex, …)**

Copy [`SKILL.md`](skills/idea-flip/SKILL.md) and the two files in [`reference/`](skills/idea-flip/reference) into your tool's custom instructions / project knowledge / rules file, or paste them at the start of a chat, then describe your problem.
I have only tested it with Claude; results on other models may differ.

## Usage

Call it with a slash, or just ask in plain words (that works the same everywhere).
If you installed it as a plugin, the slash command may be namespaced as `/idea-flip:idea-flip`.

```
/idea-flip Our weekly meeting is 90 minutes and boring, but we can't cancel it.
Give me a contrarian idea for getting 20-somethings into our local market
I'm stuck — not the obvious answer, please
```

- **Short or long, your call.** Say "brief" for the conclusion, a table and one card. After an answer, say "detail ②" to expand one idea into steps, what you need, how to tell it works, a fallback and the first 24 hours.
- **Tip: ask for more in the same conversation.** After the first answer, say "more ideas". The follow-up round skips the cards it already gave, and it can turn up ideas you did not expect. In 6 test runs the follow-up never repeated an earlier card. (Starting the same question over in a fresh chat tends to bring back similar ideas, so continue the conversation instead.)
- Default is **quick** mode. Say "go deep" to sweep all 40 inventive principles.
- For team/meeting problems it also gives you **questions to ask the team**.

## Getting better ideas

Two to four sentences are enough. Include what the skill uses:

1. **Goal** — what you want, not the solution you already picked
2. **Constraints** — budget, people, time, what must not change
3. **The dilemma** — "doing A makes B worse"
4. **What you already tried** — it goes straight onto the ban list

| Weak | Better |
|---|---|
| "Ideas for our meeting" | "Our 10-person weekly meeting is 90 minutes and boring. Without it we duplicate work. We can't cancel it. Already tried: shorter agenda." |

(These tips come from how the skill uses your input; their effect has not been tested separately.)

## What's different

1. **Ban the obvious first** — common answers are listed as a banned list; variations don't count as new ideas
2. **Forced starting points** — the 40 inventive principles are *assigned*, not chosen by the model
3. **Wildcard** — one deliberately odd idea, always labeled risky, with a cheap test attached
4. **Ends in an experiment** — every idea gets a "won't work if…" and a numeric first test

## Honest limits

- In blind AI grading the skill scored far higher (86 vs 46). In a blind A/B test with **15 colleagues** on an **earlier version (v11; the current one is v26)**, 3 problems, the skill won 23–16 (6 ties) with clearly higher **novelty** (4.07 vs 3.02) but lower **readability** (3.38 vs 4.04); one problem went the other way. Later versions added plain-language rules in response, but **the current version has not been re-tested with people.**
  So the claim is not "more creative" — it is **"a procedure that removes the common answers first and gives you odd ones with risks and experiments."**
- Answers are longer than without the skill.
- Asking the same question repeatedly tends to produce similar ideas.

Test problems, rubric, the 26 revisions (including rules that didn't work and were reverted), and all limits: **[docs/EVALUATION.md](docs/EVALUATION.md)** (in Korean).

## References

- Altshuller's 40 Inventive Principles; non-physical interpretations were rewritten in this repo's own words, drawing on Mann & Domb and Kevin Rea.
- [truinorva/triz-skills](https://github.com/truinorva/triz-skills), [smixs/creative-director-skill](https://github.com/smixs/creative-director-skill), [athola/claude-night-market](https://github.com/athola/claude-night-market) — ideas only, no code or text copied.
- [Verbalized Sampling (arXiv 2510.01171)](https://arxiv.org/abs/2510.01171) — the mode-collapse problem this skill targets.

## License

MIT
