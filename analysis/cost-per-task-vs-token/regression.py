"""Unweighted, original-unit OLS across the 14 plotted model averages."""
import json
import math
import statistics
from pathlib import Path

root = Path(__file__).resolve().parent
rows = json.loads((root / 'aggregates.json').read_text())['models']
assert len(rows) == 14 and all(r['battles'] > 100 for r in rows)
x = [r['usdPerMillionTokens'] for r in rows]
y = [r['usdPerTask'] for r in rows]
x_bar, y_bar = statistics.mean(x), statistics.mean(y)
sxx = math.fsum((v - x_bar) ** 2 for v in x)
sxy = math.fsum((a - x_bar) * (b - y_bar) for a, b in zip(x, y))
slope = sxy / sxx
intercept = y_bar - slope * x_bar
residuals = [b - intercept - slope * a for a, b in zip(x, y)]
sst = math.fsum((v - y_bar) ** 2 for v in y)
r_squared = 1 - math.fsum(v ** 2 for v in residuals) / sst
assert abs(math.fsum(residuals)) < 1e-10
assert abs(math.fsum(a * e for a, e in zip(x, residuals))) < 1e-10
assert math.isclose(r_squared, sxy ** 2 / (sxx * sst), abs_tol=1e-12)
result = {
    'method': 'Unweighted ordinary least squares, intercept plus one predictor; original USD units, no log transforms.',
    'observations': len(rows),
    'observation_unit': 'model average',
    'response': 'Mean inference cost per model task (USD)',
    'predictor': 'Realized inference cost per million input-plus-output tokens (USD), including cached input',
    'intercept': intercept,
    'slope': slope,
    'r_squared': r_squared,
    'caveat': 'Descriptive in-sample fit across model averages. Both axes share total spend as numerator; this does not establish causality or validate list token prices as an independent predictor.',
}
(root / 'regression.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
