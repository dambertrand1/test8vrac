import pandas as pd
import numpy as np
import plotly.graph_objs as go

np.random.seed(42)

n_periods = 1000
initial_price = 100
true_values = pd.Series([initial_price] + list(np.random.randn(n_periods - 1).cumsum() + initial_price))
predicted_values = true_values + np.random.randn(n_periods) * 0.1 # Predictions with some noise

df = pd.DataFrame({
    'true_values': true_values,
    'predicted_values': predicted_values
})

df['predicted_values']


df['position'] =  np.sign(df['predicted_values'] - df['true_values'].shift(1))

df['true_value_change'] = df['true_values'].diff()

df['prediction_error'] = np.abs(df['true_values'] - df['predicted_values'])
df['pnl'] = df['position'] * (df['true_value_change'] - df['prediction_error'])

initial_capital = 100000
df['cumulative_pnl'] = df['pnl'].cumsum() + initial_capital

fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['cumulative_pnl'], mode='lines', name='Cumulative PnL'))

fig.update_layout(
    title='Cumulative PnL Based on Regression Prediction Strategy',
    xaxis_title='Time Period',
    yaxis_title='Cumulative PnL ($)',
    legend_title='Strategy',
    template='plotly_white'
)

fig.show()
daily_risk_free_rate = 0.01 / 252  # Example: 1% annual risk-free rate

=df['daily_returns'] = df['cumulative_pnl'].pct_change()

df['excess_daily_returns'] = df['daily_returns'] - daily_risk_free_rate

annualized_excess_return = df['excess_daily_returns'].mean() * 252

annualized_std_dev = df['excess_daily_returns'].std() * np.sqrt(252)


sharpe_ratio = annualized_excess_return / annualized_std_dev

print(f"Annualized Sharpe Ratio: {sharpe_ratio}")
