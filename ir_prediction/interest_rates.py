import pandas as pd
import numpy as np

class Euribor():

    def __init__(self, maturity: str = "3 months"):
        self.__maturity = maturity

    def current(self):
        """Returns the current Euribor rate."""

        current = self.__fetch_current()[self.__maturity]

        return float(current.iloc[0])
    
    def get_maturity(self):
        """Return the current Euribor rate's maturity."""

        return self.__maturity

    def __fetch_current(self):
        """Fetch current Euribor rates through web scraping."""

        url = "https://www.euribor-rates.eu/en/"
        euribor = pd.read_html(url)[0]

        labels = np.char.replace(list(euribor[0]),"Euribor ","")
        rates = (np.char.replace(list(euribor[1])," %","").astype(float) / 100).reshape((1,5))

        return pd.DataFrame(rates,columns=labels)

if __name__ == "__main__":
    maturities = ["1 week","1 month","3 months","6 months","12 months"]
    r = Euribor()
    print(r.current())
    print(r.get_maturity())