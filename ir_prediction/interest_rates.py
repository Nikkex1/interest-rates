import pandas as pd
import numpy as np

class Euribor():

    def __init__(self, maturity: str = "3 months"):
        """
        Fetch Euribor rates of a given maturity.

        Parameters
        ----------
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
    
    def get_yearly(self, start: str, end: str):
        """Returns the yearly rates from the first day of the year in the given date range."""

        # For slicing the df without months and days
        s = pd.to_datetime(start).strftime("%Y")
        e = pd.to_datetime(end).strftime("%Y")

        df = self.__concat(s,e)
        mask = df.index.month == 1

        return df[mask]
    
    def get_monthly(self, start: str, end: str):
        """Returns monthly rates from the first day of the month in the given date range."""

        # For slicing the df without days
        s = pd.to_datetime(start).strftime("%Y/%m")
        e = pd.to_datetime(end).strftime("%Y/%m")

        df = self.__concat(s,e)
        df.rename(columns={0:f"Euribor ({self.__maturity})"},inplace=True)

        return df[s:e]
    
    def __concat(self, s: str, e: str):
        """Returns the monthly rates for several years in a single DataFrame."""

        s_year = pd.to_datetime(s).year
        e_year = pd.to_datetime(e).year
        y_range = range(s_year,e_year + 1)

        df_list = [self.__fetch_by_year(year) for year in y_range]

        return pd.concat(df_list)
    
    def __fetch_by_year(self, y: int):
        """Returns the cleaned monthly rates of a given year for the given maturity."""

        # Check validity of the year:
        current_year = pd.Timestamp.today().year
        if y > current_year or y < 1999:
            raise ValueError(f"{y} is an invalid year (valid range: 1999 - {current_year}).")

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
        df[0] = r_column.round(5) # round to avoid errors due to python miscalculations

        return df

if __name__ == "__main__":
    maturities = ["1 week", #0
                  "1 month", #1
                  "3 months", #2
                  "6 months", #3
                  "12 months"] #4

    r = Euribor()
    #print(r.get_monthly("1999","2025/07"))

    print(r.get_yearly("1999/01/11","2025/07/31"))