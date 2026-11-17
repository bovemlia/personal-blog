+++
title = "On model x harness interactions"
slug = "on-model-harness-interactions"
date = "2026-11-17T00:00:00-06:00"
draft = false
showFooter = true
description = ""
+++

Today, a [blog post](https://runta.com/blog/introducing-frontierharness-eval-v1-1/) purporting to show that models prefer their own harnesses hit the front page of hacker news. It was based on 27,280 agent runs. It reminded me that I had done a similar analysis out of curiosity, based on 926,588 agent runs!

(How do I have so many agent runs? Because there is a ton of benchmark trajectory data available on Hugging Face. Funny enough, this includes the data from the blog post that triggered me writing this.)

## About the data

- 75 benchmark strata (counting source-specific versions and subsets separately)
- 72 different model identities
- 54 different harness configurations

## Do models prefer their own harness

The obvious effect we’d expect would be models preferring their own harness. To investigate this, I looked at benchmark runs when a model used its own harness against ones that it used a different harness, then charted the pass rate:

![Native-harness versus alternative-harness matched success rates for 31 models, with five positive outliers labeled.](/images/native-harness/native_harness_scatter_labeled.png)

As we can see, most models do not perform differently in their own harness. The only outliers here that are statistically significant are highlighted in the above chart and included below:

![Positive native-harness advantages for GPT-5.4, GPT-5.1 Codex, GPT-5 Mini, GPT-5, and Claude Haiku 4.5, with approximate 95% simultaneous confidence intervals adjusted across 31 models.](/images/native-harness/native_harness_advantage_intervals.png)

## Is there a strong model x harness effect?

To investigate this, I built a model to predict benchmark performance with the following coefficients:

- Intercept
- Harness
- Model
- Benchmark
- Task (within benchmark)
- Study
- Model x benchmark
- Benchmark x harness
- Model x harness

If there is a strong effect for model x harness, that is independent of the rest of the effects, we would see a strong signal in the model x harness effect. In fact, we do, but the effect is smaller than the benchmark x harness interaction and the model x benchmark interaction. Here is a chart:

![Six groups summarized by the standard deviation of their contribution to predicted log odds over a balanced observed reference population, with approximate 95% posterior intervals. Model × harness has posterior median spread 0.57 log-odds units and interval 0.46–0.72. These nonnegative magnitudes avoid signed cancellation; positive bounds are not a test against zero, and the groups' variances are not additive. Intercept, task, and study remain in the fitted model but are omitted from the chart.](/images/native-harness/model_group_effect_spread.png)
