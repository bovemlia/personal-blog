+++
title = "I, too, can make a chart of perplexity drops"
date = "2026-11-22T13:58:44-06:00"
slug = "lowering-perplexity-without-scaling"
draft = false
showFooter = true
description = ""
+++

Today, OpenAI released [a blog post](https://openai.com/index/perplexity-and-intelligence/) claiming that perplexity drops can be a universal measurement of intelligence. The core of the post is a chart showing perplexity values of their models dropping over time.

[![OpenAI's chart of base model log-perplexity falling from GPT-3.5 to an internal model](/images/perplexity-data-mix/openai-base-model-log-perplexity.png)](https://openai.com/index/perplexity-and-intelligence/)

The immediate question that comes to mind seeing the chart is: perplexity against what? The answer to this is buried in a footer. It's perplexity against a fixed corpus of code.

But the problem with this is that maybe the proportion of their pre-training mix that is code is increasing.

## Lowering perplexity without scaling

So I set out to show that I could lower perplexity by just changing the pretraining mix. As I spun an agent up to get started with this, it helpfully pointed out that it had already been done in [this 2025 paper](https://arxiv.org/abs/2403.16952). (Funny enough, this was Astra 6.2, it certainly wasn't perplexed by the task.)

The authors trained models on five mixes of GitHub code and web text, with the same architecture and the same model size (160M parameters), then tested each on held-out code:

[![As code rises from 25% to 75% of training data, log-perplexity on held-out GitHub code falls from 1.213 to 1.041](/images/perplexity-data-mix/loss-by-code-share.png)](/images/perplexity-data-mix/loss-by-code-share.png)

Spoiler: the "internal model" here is the same 160M model with 75% of training corpus being code.

## Raising perplexity without scaling

As expected, the same effect holds in reverse. The same paper shows increases in performance on text only as the code share decreases.

## Conclusions

The obvious rebuttal to all of this is that the 160M model with 75% code in training mix is almost certainly more intelligent in terms of code than the 25% model. So what's my point? Only that perplexity loss only measures something meaningful in the context of what text is chosen to generate the loss. And that OpenAI's post needs a few qualifications [1].

[1] Funny enough, OpenAI admits as such in a footnote, saying in reference to GPT-2 and GPT-3: "how well they predict code is a poor proxy for their general capabilities." Why they didn't redo this analysis with a more general corpus is anyone's guess.
