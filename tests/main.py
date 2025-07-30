from ir_forecast.interest_rates import Euribor

r = Euribor(maturity="3 months")

monthly = r.get_monthly(start="2024/01", end="2025/07")
print(monthly)

from ir_forecast.ir_models import VasicekModel, CIRModel

theta_val = 0.5
mu_val = 0.02
volatility = 0.2
initial = 0.04

# Use default T = 1 and N = 252 for both models
vasicek = VasicekModel(theta=theta_val,
                       mu=mu_val,
                       sigma=volatility,
                       r0=initial)

cir = CIRModel(theta=theta_val,
               mu=mu_val,
               sigma=volatility,
               r0=initial)

from ir_forecast.monte_carlo import MonteCarlo

vasicek_mc = MonteCarlo(model=vasicek,
                        number_of_simulations=100)
vasicek_mc.visualize()
print(vasicek_mc.stats())