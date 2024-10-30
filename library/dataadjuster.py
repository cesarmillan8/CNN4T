class DataAdjuster:
    def __init__(self, data):
        """
        Inicializa la clase con los datos.
        
        Args:
            data (pd.DataFrame): El DataFrame que contiene las columnas 'Open', 'Close', 'High', 'Low', y 'Adj Close'.
        """
        self.data = data

    def adjust_data(self):
        """
        Ajusta los datos de las columnas 'Open', 'Close', 'High', 'Low' utilizando el ratio de ajuste calculado 
        entre 'Close' y 'Adj Close'. Agrega nuevas columnas ajustadas en el DataFrame.
        
        Returns:
            pd.DataFrame: El DataFrame ajustado con las nuevas columnas.
        """
        # Calcular el ratio de ajuste
        self.data['AdjustRatio'] = self.data['Close'] / self.data['Adj Close']

        # Ajustar los valores de 'Open', 'Close', 'High', 'Low' usando el ratio de ajuste
        self.data['AdjustedOpen'] = self.data['Open'] / self.data['AdjustRatio']
        self.data['AdjustedClose'] = self.data['Close'] / self.data['AdjustRatio']
        self.data['AdjustedHigh'] = self.data['High'] / self.data['AdjustRatio']
        self.data['AdjustedLow'] = self.data['Low'] / self.data['AdjustRatio']

        return self.data

    def get_adjusted_data(self):
        """
        Devuelve el DataFrame ajustado.
        
        Returns:
            pd.DataFrame: El DataFrame con las columnas ajustadas.
        """
        return self.data