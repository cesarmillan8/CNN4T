

class DataLabeler:
    def __init__(self, data, window_size=11):
        """
        Inicializa la clase con los datos y el tamaño de la ventana.
        
        Args:
            data (pd.DataFrame): El DataFrame con los datos que contienen la columna 'Close'.
            window_size (int): El tamaño de la ventana para etiquetar los datos.
        """
        self.data = data
        self.window_size = window_size

    def label_data(self):
        """
        Etiqueta los datos con las siguientes reglas:
        - 'Label' = 0: HOLD (valor por defecto)
        - 'Label' = 1: BUY (mínimo en la ventana)
        - 'Label' = 2: SELL (máximo en la ventana)
        
        Returns:
            pd.DataFrame: El DataFrame con la columna 'Label' añadida.
        """
        # Inicializar la columna 'Label' como 0 (HOLD)
        self.data['Label'] = 0

        # Recorrer el DataFrame y etiquetar los valores
        for counterRow in range(len(self.data)):
            if counterRow > self.window_size - 1:
                window_begin_index = counterRow - self.window_size
                window_end_index = window_begin_index + self.window_size - 1
                window_data = self.data.iloc[window_begin_index:window_end_index + 1]
                min_index = window_data['Close'].idxmin()
                max_index = window_data['Close'].idxmax()
                
                # Etiquetar mínimo como 'BUY' (1) y máximo como 'SELL' (2)
                self.data.at[max_index, 'Label'] = 2
                self.data.at[min_index, 'Label'] = 1

                # Descomentar desde aqui
                #window_middle_index = (window_begin_index + window_end_index) // 2
                #min_index = window_data['Close'].idxmin()
                #max_index = window_data['Close'].idxmax()

                #if max_index == window_middle_index:
                #    self.data.at[counterRow, 'Label'] = 2
                #elif min_index == window_middle_index:
                #    self.data.at[counterRow, 'Label'] = 1
                
                
        return self.data

    def get_labeled_data(self):
        """
        Devuelve el DataFrame con los datos etiquetados.
        
        Returns:
            pd.DataFrame: El DataFrame etiquetado.
        """
        return self.data
