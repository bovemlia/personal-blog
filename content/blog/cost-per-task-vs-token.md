+++
title = "Cost per token explains 92% of a model's average cost per task."
date = "2026-11-18T12:17:45-06:00"
slug = "cost-per-task-vs-token"
draft = false
showFooter = true
description = ""
+++

I see the claim all the time that cost per token doesn't represent real cost. This is undoubtably true, but I wondered, isn't cost per token still a good proxy?

To look into this, I looked at our battle data [1], which reflects real-world costs to complete real tasks, and charted against cost per token. There's clearly a relationship:

[![Cost per token versus cost per task](/images/cost-per-task-vs-token/cost-per-token-vs-task.png)](/images/cost-per-task-vs-token/cost-per-token-vs-task.png)

How much of the variation in average cost per task across models is explained by cost per token? I ran a simple regression across 14 models, with one observation per model, using mean cost per task and realized cost per token.

**Mean cost per task (USD) = 0.06945 + 3.76255 × cost per million tokens (USD)**

**R² = 0.9151**

Conclusion: cost per token explains about 92% of the variation in mean cost per task across these models.

[1] [Agent Duel leaderboard](https://agentduel.com/leaderboard)
