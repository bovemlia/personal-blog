+++
title = "About 92% of cost per task can be predicted by cost per token"
date = "2026-11-18T12:17:45-06:00"
slug = "cost-per-task-vs-token"
draft = false
showFooter = true
description = ""
+++

I see the claim all the time that cost per toke doesn't represent real cost. This is undoubtably true, but I wondered, isn't cost per token still a good proxy?

To look into this, I looked at our battle data [1], which reflects real world times to complete real tasks, and charted against cost per token. There's clearly a relationship:

[![Cost per token versus cost per task](/images/cost-per-task-vs-token/cost-per-token-vs-task.png)](/images/cost-per-task-vs-token/cost-per-token-vs-task.png)

How much of the cost per task is explained by cost per token? I ran a simple regression, with only an intercept and one independent variable. Here is the result:

**Predicted cost per task (USD) = 0.06945 + 3.76255 × cost per million tokens (USD)**

**R² = 0.9151**

Conclusion: about 92% of cost per task can be predicted by cost per token.

[1] [Agent Duel leaderboard](https://agentduel.com/leaderboard)
