+++
title = "Actually congressman probably beat the S&P 500"
slug = "house-trades-mean-returns"
date = "2026-11-15T12:00:00-06:00"
draft = false
showFooter = true
description = "What changes when we average congressional stock returns, including the biggest winners?"
+++

*Warning: this page is pure slop. It is refuting a post that was also slop, and if you can’t refute slop with slop then bullshit will win.*

[This study](https://arkanumdata.com/research/house-trades) reached Hacker News claiming that copying House members' stock trades wouldn't beat the market. My objection [in the thread, as seizethecheese](https://news.ycombinator.com/item?id=50511528): corrupt trades could be among the extreme results. Showing that lots of trades look normal doesn't rule that out.

The study focused on the **median—the middle trade**. But a few big winners can account for most of your profits. So I redid the calculations using the **mean: add up every return, then divide by the number of trades**. This includes the big winners. It doesn't tell us whether any trade was corrupt.

Two comparisons: the **usual S&P 500**, where bigger companies count more (the SPY fund), and the **S&P 500 with roughly equal money in each company** ([the RSP fund](https://www.invesco.com/us/en/financial-products/etfs/invesco-sp-500-equal-weight-etf.html)). Below, “points” means percentage points: a 12% return beats a 10% return by 2 points.

![Six months after trades become public, stocks bought beat the S&P 500 with equal amounts per company by 2.0 points on average, but trail the usual S&P 500 by 0.6 points.](/images/house-trades-mean/mean-vs-median.png)

**Stocks bought beat the equal-amount fund by 2.0 points. They trail the usual S&P 500 by 0.6.** Both results have enough uncertainty to allow for no difference. Stocks sold subsequently do better than stocks bought.

**A few big winners matter.**

![The best 5% of purchases add 5.1 points to the average; the other 95% subtract 3.1. For stocks sold, the figures are +5.8 and −2.4.](/images/house-trades-mean/tail-contributions.png)

Only **46.3%** of purchases beat the equal-amount fund. Most trades can lose to the market while the average still wins.

**One, three and six months.**

![Average returns compared with both S&P 500 funds, measured from the trade date and from when the trade becomes public.](/images/house-trades-mean/return-windows.png)

While buyers wait for trades to become public, the stocks fall **0.6 points behind the usual S&P 500** on average. Starting from the member's trade date puts six-month returns **2.3 points ahead of the equal-amount fund**, but **0.9 behind the usual S&P 500**.

**Break it down.**

![Average six-month results for purchases, split by party, trade size, account owner, reporting delay and trading activity.](/images/house-trades-mean/purchase-groups.png)

![The same breakdown for stocks sold, showing how they performed after the sale.](/images/house-trades-mean/sale-groups.png)

Several groups of purchases look better than the equal-amount fund. But these groups overlap, and testing many groups makes chance wins more likely. For sales, a positive number means the stock beat the fund *after the member sold it*.

**Let bigger trades count more.**

![Giving larger reported trades more weight raises the purchase average to 4.2 points ahead of the equal-amount fund and 1.4 ahead of the usual S&P 500.](/images/house-trades-mean/amount-weighting.png)

So far, each trade counts equally. If larger trades count more, purchases finish **4.2 points ahead of the equal-amount fund; 1.4 ahead of the usual S&P 500**. Members report dollar ranges, so I estimated each trade's size using the middle of its range.

**How this was calculated**

8,941 trades · 99 members · prices through Nov. 13, 2026. [Same source data](https://arkanumdata.com/open-data); same 1-, 3- and 6-month periods. Group counts match; middle-trade results differ by less than 0.15 points. Chart lines show 90% uncertainty ranges. These are individual stock returns, not a working investment strategy; trading costs, missing prices and differences in risk still matter.

[All 312 results (CSV)](/data/house-trades-mean/all-results.csv) · [Check against the original (CSV)](/data/house-trades-mean/replication-check.csv) · [Bought versus sold (CSV)](/data/house-trades-mean/buy-minus-sale.csv) · [Methods and code (ZIP)](/data/house-trades-mean/analysis.zip)
