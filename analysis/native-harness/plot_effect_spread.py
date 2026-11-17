"""Six-row magnitude chart from the existing fitted model's posterior draws."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
d=pd.read_csv(ROOT/'static/data/native-harness/aggregate_effect_spread.csv')
assert len(d)==7 and d.term.is_unique
assert np.isfinite(d[['estimate','ci_low','ci_high']].to_numpy()).all()
assert ((d.ci_low>=0)&(d.ci_low<=d.estimate)&(d.estimate<=d.ci_high)).all()
assert d.loc[d.term=='intercept','estimate'].item()==0
d=d[d.term!='intercept'].reset_index(drop=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none','text.color':'#172b3a','axes.labelcolor':'#172b3a','xtick.color':'#607485','ytick.color':'#172b3a'})
fig,ax=plt.subplots(figsize=(10.5,5.3))
y=np.arange(len(d))
ax.axvline(0,color='#a5b3bd',lw=1)
ax.errorbar(d.estimate,y,xerr=[d.estimate-d.ci_low,d.ci_high-d.estimate],fmt='o',color='#087f8c',elinewidth=2.4,capsize=4,markersize=7,zorder=3)
ax.set_yticks(y,d.term_label)
ax.set_ylim(len(d)-.55,-.55)
ax.set_xlim(-.07,float(d.ci_high.max())+.45)
ax.set_xticks(np.arange(0,3.1,.5))
ax.set_xlabel('Spread of group contribution (standard deviation of log odds)',labelpad=13)
ax.set_title('Group effect magnitudes with 95% intervals',loc='left',fontsize=19,weight='bold',pad=23)
for i,r in d.iterrows():
    ax.text(r.ci_high+.07,i,f'{r.estimate:.2f}',va='center',ha='left',fontsize=11)
ax.grid(axis='x',color='#e7edf1');ax.set_axisbelow(True)
ax.tick_params(axis='y',length=0,pad=12)
for side in ['top','right','left']:ax.spines[side].set_visible(False)
ax.spines['bottom'].set_color('#cbd5dd')
fig.tight_layout()
for ext in ['png','svg']:
    fig.savefig(ROOT/f'static/images/native-harness/model_group_effect_spread.{ext}',dpi=220,bbox_inches='tight',facecolor='white')
plt.close(fig)
print('Saved six-row group effect magnitude chart without the intercept.')
