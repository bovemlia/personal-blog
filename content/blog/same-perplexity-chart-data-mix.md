+++
title = "The exact same perplexity chart, from data mix alone"
date = "2026-11-22T17:05:36-06:00"
slug = "same-perplexity-chart-data-mix"
draft = false
showFooter = true
description = ""
+++

Earlier today, I published [a blog post](/blog/lowering-perplexity-without-scaling/) whose point was that OpenAI's recent post showing pre-training progress was confounded by the percent of code in their pre-training corpus.

In the post, I demonstrated that if you vary the percent of code in your pre-training mix and you only evaluate log perplexity loss on a set of code, then you almost by definition get a reduction in log perplexity loss.

After publishing, I realized I could do one better and generate something in the shape of the exact same chart:

[![OpenAI's base model log-perplexity curve, redrawn from 14 released RegMix models that share the same 1B architecture and 25B training tokens and differ only in training data mix](/images/perplexity-data-mix/regmix-same-shape.png)](https://huggingface.co/sail/data-mixture-random-1b)

[![All 64 RegMix 1B models: as the GitHub plus StackExchange share of training data rises from under 1% to about 50%, log loss on held-out GitHub code falls from about 1.4 to about 0.83 (r = -0.86)](/images/perplexity-data-mix/regmix-code-share-scatter.png)](/images/perplexity-data-mix/regmix-code-share-scatter.png)
