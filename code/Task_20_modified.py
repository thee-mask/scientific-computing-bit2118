import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------
# Modified case: M-Pesa agent cash-float risk
# Question: how likely is it that one day's customer withdrawals
# are larger than the cash the agent holds (a "stock-out")?
# All money values are in Kenya shillings (KSh).
# ------------------------------------------------------------

rng = np.random.default_rng(42)

cash_float = 250_000.0        # cash the agent holds at start of day
mean_withdrawals = 180_000.0  # average daily withdrawals (assumed)
std_withdrawals = 45_000.0    # day-to-day variation (assumed)
N = 100_000                   # number of simulated days

# Random daily withdrawal scenarios (cannot be negative)
withdrawals = rng.normal(mean_withdrawals, std_withdrawals, N)
withdrawals = np.clip(withdrawals, 0, None)

stock_out = withdrawals > cash_float
stock_out_probability = stock_out.mean()

print(f"Estimated stock-out probability: {stock_out_probability:.4%}")
print(f"Stock-out days: {stock_out.sum()} out of {N}")
print(f"Expected stock-out days per 30-day month: {30 * stock_out_probability:.2f}")

# Try different float levels to find a safe amount to hold
print("\nFloat level (KSh) vs stock-out probability:")
float_levels = np.array([200_000, 225_000, 250_000, 275_000, 300_000, 325_000])
probabilities = []
for level in float_levels:
    p = (withdrawals > level).mean()
    probabilities.append(p)
    print(f"  {level:>9,.0f}  ->  {p:.4%}")

# Graph 1: running estimate (convergence)
running_probability = np.cumsum(stock_out) / np.arange(1, N + 1)
indices = np.unique(np.logspace(1, np.log10(N), 200).astype(int)) - 1

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

axes[0].semilogx(indices + 1, running_probability[indices])
axes[0].set_xlabel("Number of simulated days")
axes[0].set_ylabel("Estimated stock-out probability")
axes[0].set_title("Convergence of the estimate")
axes[0].grid(True)

# Graph 2: risk at different float levels
axes[1].plot(float_levels / 1000, np.array(probabilities) * 100, marker="o")
axes[1].set_xlabel("Cash float (thousand KSh)")
axes[1].set_ylabel("Stock-out probability (%)")
axes[1].set_title("Risk falls as the float increases")
axes[1].grid(True)

plt.tight_layout()

# Save BEFORE show(), otherwise the saved image is blank
plt.savefig("outputs/task20_modified_graph.png", dpi=150)
plt.show()
