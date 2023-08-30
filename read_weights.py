import pandas as pd
import numpy as np


def read_excel_weights(file):

	weights_file = pd.read_excel(file)

	print(weights_file)

	weights_file = weights_file.dropna()
	weights_file.drop(columns=weights_file.columns[0], axis=1, inplace=True)


	print(weights_file)
	with open('weights_file.npy', 'wb') as f:
		np.save(f, weights_file.to_numpy())

