import numpy as np

class VasicekModel():
    """Discrete Vasicek model"""

    def __init__(self, theta: float, mu: float, sigma: float, r0: float, T: float, dt: float):
        """
        Parameters
        ----------
        """

        self.__theta = theta
        self.__mu = mu
        self.__sigma = sigma
        self.__r0 = r0
        self.__T = T
        self.__dt = dt

        self.__n = int(T/dt)
        self.__rates = np.zeros(self.__n)

    def get_rates(self):
        """Calculate the interest rates from t = 0 to T"""

        self.__rates[0] = self.__r0 # start from the initial interest rate

        # dr = theta * (mu-r[t-1]) * dt + sigma * sqrt(dt) * rand_normal
        # rate[t] = rate[t-1] + dr
        for t in range(1,self.__n):
            dr = self.__theta * (self.__mu - self.__rates[t-1]) * self.__dt + self.__sigma * np.sqrt(self.__dt) * np.random.normal()
            self.__rates[t] = self.__rates[t-1] + dr

        return self.__rates

if __name__ == "__main__":
    model1 = VasicekModel(2,0.05,0.02,0.03,1,0.001)
    print(model1.get_rates())