import numpy as np
from scipy.stats import norm
import pandas as pd

class RiskManager:
    @staticmethod
    def calculate_var(returns, confidence=0.95):
        """Calculate Value-at-Risk (Historical Simulation)"""
        return np.percentile(returns, 100 * (1 - confidence))

    @staticmethod
    def dynamic_stoploss(current_price, entry_price, volatility, multiplier=2):
        """ATR-based trailing stop"""
        return entry_price - (multiplier * volatility)

    @staticmethod
    def position_size(capital, entry_price, stoploss, risk_pct=0.01):
        """Calculate position size based on risk % of capital"""
        risk_per_share = entry_price - stoploss
        return (capital * risk_pct) / risk_per_share

    @staticmethod
    def kelly_criterion(win_rate, win_loss_ratio):
        """Optimal betting size calculation"""
        return win_rate - ((1 - win_rate) / win_loss_ratio)

if __name__ == "__main__":
    # Example usage
    returns = pd.Series([0.01, -0.02, 0.015, -0.01, 0.03])
    print(f"VaR(95%): {RiskManager.calculate_var(returns):.2%}")
    
    stoploss = RiskManager.dynamic_stoploss(
        current_price=1.08,
        entry_price=1.05,
        volatility=0.02
    )
    print(f"Dynamic Stoploss: {stoploss:.4f}")