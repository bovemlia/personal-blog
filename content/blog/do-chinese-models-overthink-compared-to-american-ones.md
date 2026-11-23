+++
title = "Chinese models do not overthink, Gemini 4 Neon does"
date = "2026-11-23T00:00:00-06:00"
slug = "do-chinese-models-overthink-compared-to-american-ones"
draft = false
showFooter = true
+++

There was a [disagreement today on hacker news](https://news.ycombinator.com/item?id=50610680) about whether Chinese models overthink. I had recently written about how [Gemini Carbon definitely overthinks](https://micjm.com/blog/carbon-is-that-slow/), so while I knew this wasn't entirely true, I wondered how true it was.

To analyze this, I used [data](https://agentduel.com/leaderboard) from [our open source battle system](https://github.com/bottomless/agent-duel) built on opencode. This data gives a nice control because two models are given the exact same prompt in the same local environment.

First, I charted how many tokens models output per battle compared to opponents, giving Chinese models red icons and American ones blue.

[![Median output tokens versus matched opponents; Chinese models red and American models blue](/images/do-chinese-models-overthink-compared-to-american-ones/output-tokens.png)](/images/do-chinese-models-overthink-compared-to-american-ones/output-tokens.png)

It looks like the over-thinkers are Gemini Neon and Carbon, while Qwen 4 Max, Kimi 3.1 Pro and GPT 6.2 Sol are under-thinkers.

(Interestingly, in the comment thread people argued that Fable 5.2 overthinks but this seems to be the case only slightly.)

For completion time, Qwen 3.8 Max joins as an over thinker, but this is mediated by it being sloooooow (32.3 tokens/sec versus 63.0 for its matched opponents).

[![Median completion time versus matched opponents; Chinese models red and American models blue](/images/do-chinese-models-overthink-compared-to-american-ones/completion-time.png)](/images/do-chinese-models-overthink-compared-to-american-ones/completion-time.png)

In terms of tool calls, Gemini models aren’t outliers anymore, but Qwen 4 and GPT Sol, are under-tool-callers, while Astra is an over-tool-caller.

If you squint you can sort of see that Chinese models might make fewer tool calls.

[![Median tool calls versus matched opponents; Chinese models red and American models blue](/images/do-chinese-models-overthink-compared-to-american-ones/tool-calls.png)](/images/do-chinese-models-overthink-compared-to-american-ones/tool-calls.png)

Aggregating all of this, it looks like there’s no real effect here, other than perhaps slightly lower tool calling by Chinese models.

[![Chinese-versus-American ratios for completion time, output tokens, and tool calls with 80% and 95% confidence intervals](/images/do-chinese-models-overthink-compared-to-american-ones/head-to-head.png)](/images/do-chinese-models-overthink-compared-to-american-ones/head-to-head.png)

So, no Chinese models don’t systematically overthink.
