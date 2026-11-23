+++
title = "Smart models probably don't need their own harness"
date = "2026-11-20"
slug = "harness-gain-vs-model-intelligence"
draft = false
description = ""
+++

It’s unclear whether harness really matters for coding agents. I frequently see claims that it does matter. Meanwhile I’ve done [my own analysis showing that it doesn’t matter much](/blog/on-model-harness-interactions/).

One recent claim about harnesses came from Ramp. (Yes, the B2B SaaS. Anything that gets attention will be used to promote B2B SaaS). In [their post](https://x.com/ramplabs/status/2123114999874994596), they ran agents both in their own harnesses and in a generic harness. Here is their chart of the differences:

[![Ramp’s SWE-Bench v2 chart comparing solve rate and mean cost per task with Bash-only and native harnesses.](/images/harness-gain-vs-model-intelligence/ramp-original-chart.jpg)](https://x.com/ramplabs/status/2123114999874994596)

What struck me looking at this chart was how the really good models didn’t seem to lose much in the generic harness. To investigate further, I inspected the top losers and gainers by being put in a generic harness:

### Largest generic-harness losses

![Largest generic-harness losses. Columns: Model, AA Index, Native, Generic, Change. GPT-6 Luna, 21, 52.4%, 42.6%, −9.8 pp; GPT-6.1 Terra, 42, 70.4%, 60.6%, −9.8 pp; Grok 4.7, 35, 64.4%, 55.4%, −9.0 pp.](/images/harness-gain-vs-model-intelligence/largest-generic-harness-losses.png)

### Smallest generic-harness losses

![Smallest generic-harness losses. Columns: Model, AA Index, Native, Generic, Change. Opus 5.5, 52, 67.8%, 71.2%, +3.4 pp; Fable 5.2, 62, 73.4%, 73.0%, −0.4 pp; Muse Wonder, 41, 58.6%, 57.8%, −0.8 pp.](/images/harness-gain-vs-model-intelligence/smallest-generic-harness-losses.png)

Indeed, it looks like there was an effect here. To investigate this further, I charted each model’s performance drop in the generic harness against its score on [Artificial Analysis’ intelligence index](https://artificialanalysis.ai/articles/artificial-analysis-intelligence-index-v5):

![Generic harness loss vs. model intelligence. Generic minus native solve rate in percentage points against the Artificial Analysis Intelligence Index for 13 models, excluding OpenCode, with a linear trendline.](/images/harness-gain-vs-model-intelligence/aa-intelligence-loss.png)

The p-val on this effect is 0.051 (I promise I just ran this once). The R² of the fit is 0.304.
