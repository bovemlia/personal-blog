+++
title = "The exact same perplexity chart, from data mix alone"
date = "2026-11-22T17:05:36-06:00"
slug = "same-perplexity-chart-data-mix"
draft = false
showFooter = true
description = ""
+++

Earlier today, I published [a blog post](/blog/lowering-perplexity-without-scaling/) showing that if you increase the proportion of code in pretraining, you will get lower log-perplexity in evaluation. This was in response to [OpenAI's blog](https://openai.com/index/perplexity-and-intelligence/) today.

After publishing, I found [a project](https://github.com/sail-sg/regmix) that had actually randomized contents of pretraining and published log-perplexities on the various components. Basically, they'd already done an experiment to prove the relationship I was alleging.

Here's the data from their experiment, you can see how closely log-perplexity for code tracks code content.

[![All 64 RegMix 1B models: as the GitHub plus StackExchange share of training data rises from under 1% to about 50%, log loss on held-out GitHub code falls from about 1.4 to about 0.83 (r = -0.86)](/images/perplexity-data-mix/regmix-code-share-scatter.png)](/images/perplexity-data-mix/regmix-code-share-scatter.png)

The r² of this chart is 0.75 and the p-value of this relationship is about 4×10⁻²⁰.

For fun, I asked an agent to cherrypick the data and generate a similar chart to OpenAI's, just using the various points here. We even have an impressive internal model (that's just 50% code in pretraining).

[![OpenAI's base model log-perplexity curve, redrawn from 14 released RegMix models that share the same 1B architecture and 25B training tokens and differ only in training data mix, with code share rising from 1.2% to 49.4% left to right](/images/perplexity-data-mix/regmix-same-shape.png)](https://huggingface.co/sail/data-mixture-random-1b)
