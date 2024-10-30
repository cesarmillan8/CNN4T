import numpy as np
from PIL import Image
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.utils import shuffle

class ImageDataProcessor:
    def __init__(self, csv_path, root_path, is_testing = False, handle_imbalance=False):
        """
        Inicializa la clase con los parámetros necesarios.

        Args:
            csv_path (str): Ruta al archivo CSV.
            root_path (str): Directorio raíz donde se guardarán las imágenes.
            handle_imbalance (bool): Si es True, maneja el desequilibrio de clases.
        """
        self.csv_path = csv_path
        self.root_path = root_path
        self.handle_imbalance = handle_imbalance
        self.is_testing = is_testing
        self.df = None
        self.images = None
        self.labels = None

        # Directorios para guardar imágenes según el tipo
        self.buy_path = os.path.join(self.root_path, 'Buy')
        self.sell_path = os.path.join(self.root_path, 'Sell')
        self.hold_path = os.path.join(self.root_path, 'Hold')

    def make_image(self, array):
        """Convierte un array de numpy en una imagen de escala de grises."""
        data = Image.fromarray(array, mode='L')
        return data

    def read_and_preprocess_data(self):
        """Lee el archivo CSV y prepara los datos."""
        self.df = pd.read_csv(self.csv_path)
        self.df.set_index("Date",inplace = True)
        self.df.sort_index()
        #self.df.drop(self.df.columns[0], axis=1, inplace=True)

        # Si se selecciona manejar el desequilibrio
        if self.handle_imbalance:
            self.handle_class_imbalance()

        # Convertir los datos en arrays de imágenes y etiquetas
        self.images = self.df.iloc[:, 3:].to_numpy()  # Asume que las columnas de imagen están después de las dos primeras
        self.labels = self.df.iloc[:, 0]

    def handle_class_imbalance(self):
        """Maneja el desequilibrio de clases replicando datos."""
        l0 = self.df.loc[self.df["Label"] == 0]
        l1 = self.df.loc[self.df["Label"] == 1]
        l2 = self.df.loc[self.df["Label"] == 2]
        l0_size = l0.shape[0]
        l1_size = l1.shape[0]
        l2_size = l2.shape[0]
        
        l0_l1_ratio = (l0_size // l1_size)
        l0_l2_ratio = (l0_size // l2_size)

        l1_new = pd.DataFrame()
        l2_new = pd.DataFrame()

        for idx, row in self.df.iterrows():
            if row["Label"] == 1:
                for _ in range(l0_l1_ratio):
                    l1_new = l1_new.append(row)
            if row["Label"] == 2:
                for _ in range(l0_l2_ratio):
                    l2_new = l2_new.append(row)

        self.df = self.df.append(l1_new)
        self.df = self.df.append(l2_new)

        # Shuffle y reset de índices
        self.df = shuffle(self.df)
        self.df.reset_index(drop=True, inplace=True)

    def create_directories(self):
        """Crea los directorios donde se guardarán las imágenes."""
        os.makedirs(self.buy_path, exist_ok=True)
        os.makedirs(self.sell_path, exist_ok=True)
        os.makedirs(self.hold_path, exist_ok=True)

    def save_images(self):
        """Guarda las imágenes en las carpetas correspondientes según la etiqueta."""
        for i in range(np.shape(self.images)[0]):
            img = np.abs(self.images[i:i + 1][0:]).transpose()
            img = np.round(img * 255).reshape((15, 15)).astype('int')
            img = self.make_image(img)
            img_number = f'{i + 1:04}' 
            if self.is_testing:
                img.save(os.path.join(self.root_path, f'img{img_number}.png'))
            else:
                if self.labels[i] == 0:
                    img.save(os.path.join(self.hold_path, f'img{img_number}.png'))
                elif self.labels[i] == 1:
                    img.save(os.path.join(self.buy_path, f'img{img_number}.png'))
                elif self.labels[i] == 2:
                    img.save(os.path.join(self.sell_path, f'img{img_number}.png'))

    def process(self):
        """Realiza todo el flujo de procesamiento de datos y creación de imágenes."""
        self.read_and_preprocess_data()
        
        if self.is_testing == False:
            self.create_directories()
        
        self.save_images()

        if self.is_testing:
            df_result = self.df[['Label', 'Open', 'Close']].copy()
            df_result.to_csv(f'{self.root_path}/cnn_result.csv') # Save Data as CSV
