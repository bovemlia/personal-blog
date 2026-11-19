+++
title = "Opus 5.5 is probably still nerfed"
date = "2026-11-13T12:00:00-06:00"
lastmod = "2026-11-19T14:54:18-06:00"
slug = "opus-5.5-after-fable"
draft = false
showFooter = true
description = "Checking Opus 5.5's reasoning output again after the Fable 5.2 launch."
+++

A few days ago, [I wrote about Opus 5.5 being nerfed](/blog/get-ready-for-fewer-opus-5.5-em-dashes/). One theory was that this was because of testing Fable 5.2, so I wanted to check again, since [Fable has now launched](https://www.anthropic.com/claude-fable-and-mythos-5-2).

Here's a chart of Opus 5.5's reported reasoning tokens per request, relative to alternative models in the same battles. The vertical line is the Fable release date, November 9:

![Opus 5.5 reasoning relative to matched opponents through November 18, with a vertical line at Fable's November 9 launch and confidence intervals](/images/opus-5.5/reasoning-fable-launch.png)

**Original conclusion (November 13):** From our data alone, we can only say that it’s likely that Opus is still nerfed. The p-val on the bootstrap test of before and after the Fable launch is p=0.105.

**Update (November 19):** The chart now includes 524 matched battles through November 18, adding 70 to the original sample. The opponent-adjusted reasoning ratio is 50.1% higher on November 9–18 than November 1–8 (95% CI: +5.6% to +113.5%; two-sided developer-clustered bootstrap p=0.033, previously p=0.105). This is a relative rebound: the point estimates show little change in Opus's own reported reasoning tokens per request and lower opponent usage.

The ratio remains 26.9% below October 15–31, but that difference is inconclusive (95% CI: −59.8% to +33.0%; p=0.220). Excluding launch day also weakens the rebound result to p=0.091. Reported token usage alone does not establish whether Opus is still nerfed.

Data: [daily chart estimates](/data/opus-5.5-after-fable/daily-chart-data.json) · [statistical results and methodology](/data/opus-5.5-after-fable/results.json).
