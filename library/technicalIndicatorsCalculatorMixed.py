import talib as ta

class TechnicalIndicatorsCalculator:
    def __init__(self, data):
        self.data = data

    def calculate_RSI(self, i):
        self.data[f'RSI_{i}'] = ta.RSI(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_WR(self, i):
        self.data[f'WILLR_{i}'] = ta.WILLR(self.data["AdjustedHigh"], self.data["AdjustedLow"], self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_CCI(self, i):
        self.data[f'CCI_{i}'] = ta.CCI(self.data["AdjustedHigh"], self.data["AdjustedLow"], self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_CMO(self, i):
        self.data[f'CMO_{i}'] = ta.CMO(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_ROC(self, i):
        self.data[f'ROC_{i}'] = ta.ROC(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_MACD(self, i):
        self.data[f'MACD_{i}'] = ta.MACD(self.data["AdjustedClose"], fastperiod=i+1, slowperiod=(i+1)*2)[0]

    def calculate_PPO(self, i):
        self.data[f'PPO_{i}'] = ta.PPO(self.data["AdjustedClose"], fastperiod=i+1, slowperiod=(i+1)*2)

    def calculate_CMFI(self, i):
        mfv = ((self.data["AdjustedClose"] - self.data["AdjustedLow"]) - (self.data["AdjustedHigh"] - self.data["AdjustedClose"])) / (self.data["AdjustedHigh"] - self.data["AdjustedLow"]) * self.data['Volume']
        self.data[f'CMFI_{i}'] = mfv.rolling(window=i+1).sum() / self.data['Volume'].rolling(window=i+1).sum()

    def calculate_SMA(self, i):
        self.data[f'SMA_{i}'] = ta.SMA(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_EMA(self, i):
        self.data[f'EMA_{i}'] = ta.EMA(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_WMA(self, i):
        self.data[f'WMA_{i}'] = ta.WMA(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_HMA(self, i):
        a = ta.WMA(self.data["AdjustedClose"], timeperiod=(i+1)//2)
        b = self.data[f'WMA_{i}']
        self.data[f'HMA_{i}'] = ta.WMA(2*a - b, timeperiod=int((i+1)**0.5))

    def calculate_TEMA(self, i):
        self.data[f'TEMA_{i}'] = ta.TEMA(self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_DMI(self, i):
        self.data[f'ADX_{i}'] = ta.ADX(self.data["AdjustedHigh"], self.data["AdjustedLow"], self.data["AdjustedClose"], timeperiod=i+1)

    def calculate_SAR(self, i):
        self.data[f'SAR_{i}'] = ta.SAR(self.data["AdjustedHigh"], self.data["AdjustedLow"])

    def calculate_all_indicators(self, start=5, end=20):
        for i in range(start, end):
            self.calculate_RSI(i)
            self.calculate_WR(i)
            self.calculate_CCI(i)
            self.calculate_CMO(i)
            self.calculate_ROC(i)
            self.calculate_MACD(i)
            self.calculate_PPO(i)
            self.calculate_CMFI(i) 
            self.calculate_SMA(i)
            self.calculate_EMA(i)
            self.calculate_WMA(i)
            self.calculate_HMA(i)
            self.calculate_TEMA(i)
            self.calculate_DMI(i)
            self.calculate_SAR(i)