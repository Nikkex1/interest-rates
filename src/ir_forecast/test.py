from interest_rates import Euribor
from ir_models import VasicekModel, CIRModel
from monte_carlo import MonteCarlo

# Monthly Euribor rates from January 2024 to July 2025
r = Euribor(maturity="3 months")
monthly = r.get_monthly(start="2024/01", end="2025/07")
print(monthly)

# Using the same parameters for both Vasicek and CIR models
mean_reversion_speed = 1.5
long_term_mean = 0.05
volatility = 0.02
initial_rate = 0.03

# Use default T = 1 and N = 252 for both models
vasicek = VasicekModel(theta=mean_reversion_speed,
                       mu=long_term_mean,
                       sigma=volatility,
                       r0=initial_rate)

cir = CIRModel(theta=mean_reversion_speed,
               mu=long_term_mean,
               sigma=volatility,
               r0=initial_rate)

# Monte Carlo simulation with 100 simulation runs
vasicek_mc = MonteCarlo(model=vasicek,
                        number_of_simulations=100)

cir_mc = MonteCarlo(model=cir,
                    number_of_simulations=100)

vasicek_mc.visualize()
cir_mc.visualize()

# Summary statistics for both models
print(vasicek_mc.stats().to_markdown())
print(cir_mc.stats().to_markdown())