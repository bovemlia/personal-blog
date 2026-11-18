+++
title = "Yes, Gemini Carbon is that slow"
date = "2026-11-18T00:00:00-06:00"
slug = "carbon-is-that-slow"
draft = false
showFooter = true
description = "Basically, Carbon is good when you're willing to wait."
+++

In reviewing our leaderboard [1], I noticed an outlier: Gemini 4 Carbon was taking more than twice as long to complete its tasks than any other model. This looked weird, so I pulled up our battle data where Carbon was a contestant.

I found that Carbon really is that slow. In fact, it took about 3x as long to complete tasks compared to opponents (6m 08s vs 2m 04s).

I wanted to look into what might be the cause. The biggest outliers were:

- Output tokens 16.4k for Carbon vs 6.8k for opponents.
- Tool calls: 21 for Carbon vs 11 for opponents.

In terms of output tokens, Carbon is unique:

[![Median output tokens versus matched opponents](/images/carbon-is-that-slow/output-tokens.png)](/images/carbon-is-that-slow/output-tokens.png)

In terms of completion time, Carbon has only one comparable model, Qwen 3.8 Max, not exactly a great neighborhood to be in.

[![Median completion time versus matched opponents](/images/carbon-is-that-slow/completion-time.png)](/images/carbon-is-that-slow/completion-time.png)

In terms of tool calls, there's an outlier even worse than Gemini 4: GPT 6 Astra. We don't have enough data from the infamous 6.2 Astra, but this points to one thing that may be wrong with it.

[![Median tool calls versus matched opponents](/images/carbon-is-that-slow/tool-calls.png)](/images/carbon-is-that-slow/tool-calls.png)

Features I looked into that don't seem to be driving poor Carbon performance are inference speed (52 tps vs opponent's 73 tps), latency (12s vs opponent's 8s), and agent turns (13 vs opponent's 8).

Interestingly enough, Carbon has a high win rate when the voter waits for both solutions to finish, but a *terrible* win rate from early voting.

- Both finished: 83 carbon wins, 52 losses.
- Early votes: 2 carbon wins, 40 losses!

Here's early voting against all votes.

[![Early-vote win rate on the X axis versus all-vote win rate on the Y axis](/images/carbon-is-that-slow/early-vs-all-win-rate.png)](/images/carbon-is-that-slow/early-vs-all-win-rate.png)

<!-- Reused verbatim from https://news.ycombinator.com/item?id=50513416 by seizethecheese. -->
(We allow early voting contrary to Arena.ai because I think it makes sense for agents, where it doesn’t for chat. This means our data takes speed into account.)

Basically, Carbon is good when you're willing to wait.

[1] [https://agentduel.com/leaderboard](https://agentduel.com/leaderboard)
