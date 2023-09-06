Uses backtesting.py to test a strategy based on price action dipping into price areas that were not well traded into (ICT's fair value gap)

Initial tests suggest that the strategy does very well when the broader market is in a big drawdown:

```
Start                     2022-01-10 09:00:00
End                       2022-01-18 18:22:00
Duration                      8 days 09:22:00
Exposure Time [%]                        5.96
Equity Final [$]                   10553.1171
Equity Peak [$]                    10604.2101
Return [%]                           5.531171
Buy & Hold Return [%]               -6.875992
Return (Ann.) [%]                  446.178119
Volatility (Ann.) [%]               79.690084
Sharpe Ratio                         5.598916
Sortino Ratio                     6947.319819
Calmar Ratio                       297.347613
Max. Drawdown [%]                   -1.500527
Avg. Drawdown [%]                    -0.22509
Max. Drawdown Duration        3 days 11:45:00
Avg. Drawdown Duration        0 days 07:59:00
# Trades                                  118
Win Rate [%]                        43.220339
Best Trade [%]                       1.233005
Worst Trade [%]                     -0.337559
Avg. Trade [%]                       0.045847
Max. Trade Duration           0 days 00:08:00
Avg. Trade Duration           0 days 00:02:00
Profit Factor                        1.981222
Expectancy [%]                       0.046072
SQN                                  2.348559
_strategy                         FVGStrategy
_equity_curve                             ...
_trades                        Size  Entry...
dtype: object
```