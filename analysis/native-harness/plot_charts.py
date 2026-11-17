from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'static/images/native-harness'
OUT.mkdir(parents=True,exist_ok=True)
d=pd.read_csv(ROOT/'static/data/native-harness/model-confidence.csv')
hi=d[d.positive_simultaneous].sort_values('delta',ascending=False).reset_index(drop=True)
other=d[~d.positive_simultaneous]
ink='#172b3a'; muted='#607485'; green='#087f8c'; gray='#9eabb6'; grid='#e7edf1'
names={'gpt-5.4':'GPT-5.4','gpt-5.1-codex':'GPT-5.1 Codex','gpt-5-mini':'GPT-5 Mini','gpt-5':'GPT-5','claude-haiku-4-5':'Claude Haiku 4.5'}
native_names={'codex':'Codex','claude-code':'Claude Code'}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':ink,'axes.labelcolor':ink,'xtick.color':muted,'ytick.color':muted,'svg.fonttype':'none'})

def save(fig,name):
    for ext in ['png','svg']:
        fig.savefig(OUT/f'{name}.{ext}',dpi=220,facecolor='white',bbox_inches='tight')
    plt.close(fig)

fig=plt.figure(figsize=(9,8.9),facecolor='white')
ax=fig.add_axes([.12,.105,.83,.815])
fig.text(.12,.965,'Which models do better in their own harness?',fontsize=18,weight='bold')
ax.plot([0,100],[0,100],color='#aab6bf',lw=1.3,ls=(0,(4,4)),zorder=1)
ax.scatter(100*other.alternative_mean,100*other.native_mean,s=49,c=gray,alpha=.78,edgecolor='white',linewidth=.6,zorder=3)
ax.scatter(100*hi.alternative_mean,100*hi.native_mean,s=86,c=green,edgecolor='white',linewidth=1,zorder=5)
ax.text(3,94,'Native harness higher',fontsize=11,color=muted)
ax.text(63,4,'Alternatives higher',fontsize=11,color=muted)
positions={'gpt-5.4':(48,76),'claude-haiku-4-5':(8,38),'gpt-5':(12,48),'gpt-5-mini':(8,58),'gpt-5.1-codex':(18,68)}
for r in hi.itertuples():
    ax.annotate(names[r.model],xy=(100*r.alternative_mean,100*r.native_mean),xytext=positions[r.model],fontsize=11,color=ink,weight='bold',ha='left',va='center',arrowprops={'arrowstyle':'-','color':green,'lw':.9,'shrinkA':4,'shrinkB':6},bbox={'facecolor':'white','edgecolor':'none','alpha':.94,'pad':2.5},zorder=6)
ax.set(xlim=(0,100),ylim=(0,100),xlabel='Mean available alternatives · matched success (%)',ylabel='Native harness · matched success (%)')
ax.set_xticks(np.arange(0,101,20));ax.set_yticks(np.arange(0,101,20))
ax.set_aspect('equal',adjustable='box');ax.grid(color=grid,lw=.8);ax.set_axisbelow(True)
for k in ['top','right']:ax.spines[k].set_visible(False)
for k in ['bottom','left']:ax.spines[k].set_color('#cbd5dd')
legend=[Line2D([0],[0],marker='o',color='none',markerfacecolor=green,markeredgecolor='white',markersize=9,label='95% simultaneous CI above zero'),Line2D([0],[0],marker='o',color='none',markerfacecolor=gray,markeredgecolor='white',markersize=8,label='Other models')]
ax.legend(handles=legend,loc='upper left',bbox_to_anchor=(.025,.89),frameon=False,fontsize=9,handlelength=1)
save(fig,'native_harness_scatter_labeled')

fig=plt.figure(figsize=(9,5.1),facecolor='white')
ax=fig.add_axes([.09,.15,.85,.73])
fig.text(.09,.95,'Native-harness advantage',fontsize=22,weight='bold')
ax.axvline(0,color='#9baab5',lw=1)
for i,r in hi.iterrows():
    y=len(hi)-1-i
    lo,est,up=100*np.array([r.simultaneous_ci_low,r.delta,r.simultaneous_ci_high])
    ax.errorbar(est,y,xerr=[[est-lo],[up-est]],fmt='o',color=green,ecolor=green,elinewidth=2.7,capsize=4,markersize=7,zorder=4)
    ax.text(0,y+.30,f'{names[r.model]}  /  {native_names[r.native_harness]}',fontsize=12,weight='bold',ha='left',va='center')
    ax.text(30,y-.26,f'+{est:.1f} pp   [{lo:.1f}, {up:.1f}]',fontsize=11,ha='right',va='center')
ax.set(xlim=(0,30),ylim=(-.6,len(hi)-.4),xlabel='Native minus mean available alternatives (percentage points)',yticks=[])
ax.set_xticks([0,5,10,15,20,25,30]);ax.grid(axis='x',color=grid,lw=.7);ax.set_axisbelow(True)
for k in ['top','right','left']:ax.spines[k].set_visible(False)
ax.spines['bottom'].set_color('#cbd5dd')
save(fig,'native_harness_advantage_intervals')
print('Saved blog charts as PNG and SVG, without subtitles or footnotes.')
