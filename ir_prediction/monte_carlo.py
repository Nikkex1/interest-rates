import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ir_models import *

class MonteCarlo():
    """Monte Carlo simulation"""

    def __init__(self, model: VasicekModel | CIRModel):
        """init"""

        self.__model = model
        self.__params = model.get_params()

        # initialize the variable to prevent rerunning the simulation
        self.__all_sims = 0

    def run(self,number_of_simulations: int):
        """Run the Monte Carlo simulation."""

        # N rows (time steps)
        # number_of_simulation columns (1 simulation per 1 column)
        self.__all_sims = np.zeros((self.__params["N"],number_of_simulations))

        for i in range(number_of_simulations):
            self.__all_sims[:,i] = self.__model.get_rates()

    def results(self):
        """Return the Monte Carlo simulation results as a DataFrame."""

        if type(self.__all_sims) == int:
            return None
        else:
            df = pd.DataFrame(self.__all_sims)
            df.index.name = "Time step"
            df.columns = [f"Simulation {i}" for i in range(1,len(df.columns) + 1)]
            return df
        
    def visualize(self):
        """Visualizes the simulated interest rate paths."""

        df = self.results()

        fig,ax = plt.subplots()
        ax.set_xlim([0,self.__params["N"]])

        for c in df.columns:
            plt.plot(df[c])

        plt.show()

if __name__ == "__main__":
    theta = 2
    mu = 0.05
    sigma = 0.02
    r0 = 0.03

    v_model = VasicekModel(theta,mu,sigma,r0)
    v_monte_carlo = MonteCarlo(v_model)

    v_monte_carlo.run(100)
    print(v_monte_carlo.results())

    cir_m = CIRModel(theta,mu,sigma,r0)
    cir_monte_carlo = MonteCarlo(cir_m)

    cir_monte_carlo.run(100)
    print(cir_monte_carlo.results())

    v_monte_carlo.visualize()