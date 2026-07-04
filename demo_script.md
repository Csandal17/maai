# Maai — 2-minute demo script (ZOE hackathon)

Beats mirror the slide speaker notes. Timings assume a calm pace.
Assets: 3 slides + live Space + downloaded PDF as wifi backup.

## SLIDE 1 — Hook (20s)

There's a scene in The Pitt this season that went viral. A woman arrives
at the ER with chest pain. Her EKG reads normal — nobody knows what's
wrong. Then her heart stops. It turns out the paramedics had placed the
EKG leads too low — they hadn't wanted to move her bra. The machine said
she was fine because no one looked properly. As Dr. Robby says in the
scene: "Women are misdiagnosed for heart attacks all the time." That
failure was equipment — but the pattern runs through every step of
women's cardiac care. Here's the data.

## SLIDE 2 — Problem (25s)

This isn't television. Coronary heart disease kills twice as many women
in the UK as breast cancer. Over ten years, 8,243 women died who wouldn't
have, if their care had matched men's. And when a woman has a heart
attack, she's 50% more likely than a man to be misdiagnosed — because her
symptoms get dismissed as vague. That last number is the one we built for.

[SWITCH TO LIVE APP]

## LIVE — Solution (45s)

This is Maai. A woman describes what she's been experiencing — her own
words, any language. [paste English description] Maai maps her words to
clinical terms a GP recognises — and look: "my husband says I'm just run
down" is in the record. The dismissal itself becomes evidence. Nothing
she says is dropped, nothing is diagnosed.

## LIVE — The moment (20s)

[paste Chinese description] Same woman, in Mandarin. Same complete
record — her exact characters preserved, English clinical terms
alongside. And this phrase — [point at 上火] — has no Western clinical
equivalent. Maai doesn't drop it or fake a translation. It keeps her
words and flags the gap. She doesn't need English to be heard.

[open the PDF] This is what she takes to her appointment.

## SLIDE 3 — Guardrail + close (15s)

One thing Maai deliberately doesn't do: conclude. No diagnosis, no
severity scores — if symptoms are happening right now, it says call 999.
The tool makes her harder to dismiss; the clinician does the medicine.
Next, we'd structure records around SOCRATES — the framework GPs are
trained on — and add advocacy coaching so she knows what she's allowed
to ask for.

## Q&A back pocket

- "What if she's having a heart attack right now?" → The 999 line is on
  screen and printed on every PDF. Maai is patterns over time, never
  triage.
- "Is the 50% stat solid?" → Prof. Chris Gale's study, via BHF Bias and
  Biology (2019). Primary links in SOURCES.md.
- Second source on discomfort costing lives: UPenn — bystanders less
  likely to perform CPR on women; men 23% more likely to survive public
  cardiac events.
- "Why no framework/CrewAI?" → Three pure LLM transformations, no
  tool-use or looping. Knowing when not to add a framework is the
  engineering choice.
- "Chinese accuracy?" → Verbatim is preserved untouched by design;
  clinical mapping is an advocacy aid, the clinician interprets.
  