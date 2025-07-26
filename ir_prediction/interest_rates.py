import pandas as pd
import numpy as np

class Euribor():

    def __init__(self, maturity: str = "3 months"):
        """
        Fetch Euribor rates by maturity.
        """
        self.__maturity = maturity

    def get_current(self):
        """Return the latest daily Euribor rate."""

        return self.get_daily().iloc[0,0]

    def get_daily(self):
        """Returns the current Euribor rates from the last 10 days."""

        df = self.__construct(by=0)
        df.rename(columns={1: f"Daily rates ({self.__maturity})"},
                  inplace=True)

        return df
    
    def get_monthly(self):
        """Returns the Euribor rates on the first day of the month from the last 10 months."""

        df = self.__construct(by=1)
        df.rename(columns={1: f"Monthly rates ({self.__maturity})"},
                  inplace=True)

        return df
    
    def get_annual(self):
        """Returns the Euribor rates on the first day of the year from the last 10 years."""

        df = self.__construct(by=2)
        df.rename(columns={1: f"Annual rates ({self.__maturity})"},
                  inplace=True)

        return df
    
    def __fetch(self):
        """Returns a list of Euribors by day, month and year"""

        # For constructing the url below
        d = {"1 month": 1,
             "3 months": 2,
             "6 months": 3,
             "12 months": 4,
             "1 week": 5}
        
        m_number = d[self.__maturity]
        m_label = self.__maturity.split()

        url = f"https://www.euribor-rates.eu/en/current-euribor-rates/{m_number}/euribor-rate-{m_label[0]}-{m_label[1]}/"

        euribors = pd.read_html(url)

        # day [0], month [1], year [2] of given maturity
        return euribors
    
    def __construct(self, by: int):
        """Returns a cleaned DataFrame of the rates by day, month or year."""
        
        df = self.__fetch()[by]

        # Assign date index and drop the old date column
        df.index = df[0].astype("datetime64[ns]")
        df.index.name = "Date"
        df.drop(columns=0,inplace=True)

        # Convert the string rates to float
        r_column = (np.char.replace(list(df[1])," %","").astype(float)) / 100
        df[1] = r_column

        return df
    
    def fetch_by_year(self, y: int = 2025):
        """Returns the monthly rates of a given year for the given maturity."""

        # Construct the url:
        d = {"1 month": 1,
             "3 months": 2,
             "6 months": 3,
             "12 months": 4,
             "1 week": 5}
        m_id = d[self.__maturity]
        url = f"https://www.global-rates.com/en/interest-rates/euribor/historical/{y}/?id={m_id}#bmrk-maturity"

        # Monthly rates are in the second table
        df = pd.read_html(url)[1]

        # Use the first day of the month, drop everything else
        df.drop(columns=["Unnamed: 0","Last","Highest","Lowest","Average"],
                inplace=True)
        
        #Rename the remaining column for simplicity
        df.rename(columns={"First": 0},
                  inplace=True)
        
        # Monthly date index, first business day of the month
        idx = pd.date_range(f"{y}/1/1",f"{y}/12/31",freq="BMS")
        df.index = idx
        df.index.name = "Date"

        # Check for empty values and drop them
        mask = df[0] == "-"
        df[mask] = np.nan
        df.dropna(inplace=True)

        # Convert the string rates ("X.xx %") to float (0.0Xxx)
        r_column = (np.char.replace(list(df[0])," %","").astype(float)) / 100
        df[0] = r_column

        return df

if __name__ == "__main__":
    maturities = ["1 week", #0
                  "1 month", #1
                  "3 months", #2
                  "6 months", #3
                  "12 months"] #4

    r = Euribor()
    print(r.fetch_by_year())