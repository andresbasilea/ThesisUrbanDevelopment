
import numpy as np

class CA_Utils:

	def __init__(self):
		
		self.central_row = 0
		self.central_col = 0
		self.central_land_use = 0
		

		# self.banda1 = [[col+1, row],[col-1, row],[col, row-1], [col, row+1] ]  
		# self.banda2 = [ [col+1, row+1], [col+1, row-1], [col-1, row-1], [col-1, row+1] ]
		# self.banda3 = [ [col+2, row], [col,row-2], [col-2, row], [col, row+2]]
		# self.banda4 = [ [col+2, row+1], [col+2, row-1], [col+1,row+2], [col+1, row-2], [col-2, row+1], [col-2, row-1], [col-1, row+2], [col-1, row-2] ]  
		# self.banda5 = [ [col+2, row+2], [col+2, row-2], [col-2, row-2], [col-2, row+2]]
		#self.land_categories = ['Industrial', 'Commercial', 'Residential', 'Green', 'Vacant']

		self.colors_mapping = {'white':0,'rebeccapurple':1, 'crimson':2, 'darkorange':3,'darkcyan':4,'black':5}

		self.banda1 = [[1, 0],[-1,0 ],[0, -1], [0, 1] ]  
		self.banda2 = [ [1, 1], [1, -1], [-1, -1], [-1, 1] ]
		self.banda3 = [ [2,0 ], [0,-2], [-2,0 ], [0, 2]]
		self.banda4 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]  
		self.banda5 = [ [2, 2], [2, -2], [-2, -2], [-2, 2]]


		self.list_distance_bands = [ 
									self.banda1,
									self.banda2,
									self.banda3,
									self.banda4,
									self.banda5,
									] 

		self.ItoC = 0
		self.ItoI = 0
		self.ItoH = 0
		self.ItoG = 0
		self.CtoC = 0
		self.CtoI = 0
		self.CtoH = 0
		self.CtoG = 0
		self.HtoC = 0
		self.HtoI = 0
		self.HtoH = 0
		self.HtoG = 0
		self.GtoC = 0
		self.GtoI = 0
		self.GtoH = 0
		self.GtoG = 0
		self.VtoC = 0
		self.VtoI = 0
		self.VtoH = 0
		self.VtoG = 0
		self.VtoV = 0

		self.sum_XtoC = 0
		self.sum_XtoI = 0
		self.sum_XtoH = 0
		self.sum_XtoG = 0

		self.P_XtoC = 0
		self.P_XtoI = 0
		self.P_XtoH = 0
		self.P_XtoG = 0
		
		self.list_potential_value = [self.P_XtoC, self.P_XtoI, self.P_XtoH, self.P_XtoG]

		# self.sum_CtoC = 0
		# self.sum_CtoI = 0
		# self.sum_CtoH = 0
		# self.sum_CtoG = 0
		# self.sum_HtoC = 0
		# self.sum_HtoI = 0
		# self.sum_HtoH = 0
		# self.sum_HtoG = 0
		# self.sum_GtoC = 0
		# self.sum_GtoI = 0
		# self.sum_GtoH = 0
		# self.sum_GtoG = 0
		# self.sum_VtoC = 0
		# self.sum_VtoI = 0
		# self.sum_VtoH = 0
		# self.sum_VtoG = 0
		# self.sum_VtoV = 0

		self.potential_ItoC = 0
		self.potential_ItoI = 0
		self.potential_ItoH = 0
		self.potential_ItoG = 0
		self.potential_CtoC = 0
		self.potential_CtoI = 0
		self.potential_CtoH = 0
		self.potential_CtoG = 0
		self.potential_HtoC = 0
		self.potential_HtoI = 0
		self.potential_HtoH = 0
		self.potential_HtoG = 0
		self.potential_GtoC = 0
		self.potential_GtoI = 0
		self.potential_GtoH = 0
		self.potential_GtoG = 0
		self.potential_VtoC = 0
		self.potential_VtoI = 0
		self.potential_VtoH = 0
		self.potential_VtoG = 0
		self.potential_VtoV = 0

		self.weights_range = 0

		self.rng_0_1 = np.random.default_rng()
		self.stochastic_disturbance = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)


	# def apply_cellular_automata_rule(self,cell, neighbors):
	# 	# Define your rules here, this is just a simple example
	# 	# If cell is empty and has at least 1 developed neighbor, it becomes developed
	# 	if cell == 4 and np.sum(neighbors) >= 1:
	# 		return np.sum(neighbors)%5
	# 	else:
	# 		return cell


	def white_transition(self, matrix, weights):

		changed_state_matrix = np.zeros_like(matrix)

		list_potential_land_use = ['Vacant','Industrial', 'Commercial', 'Residential', 'Green']
		#Ihd = 1
		#sum_result = 0
		
		number_of_bands = 5


		# sum_result_ItoSomething = 0
		# sum_result_CtoSomething = 0
		



		for row in range(matrix.shape[0]):
			for col in range(matrix.shape[1]):
				self.central_col = col
				self.central_row = row
				self.central_land_use = matrix[row, col]
				self.central_land_use = int(self.central_land_use)
				print("central_row: ",self.central_row,"central_col: ", self.central_col, "central_land_use: ", self.central_land_use)



				if self.central_land_use == 0: # i cell (central cell) is vacant 
					pass
				if self.central_land_use == 1: # i cell (central cell) is Industrial 
					self.weights_range = 0
				if self.central_land_use == 2: # i cell (central cell) is Commercial
					self.weights_range = 24
				if self.central_land_use == 3: # i cell (central cell) is Residential
					self.weights_range = 48
				if self.central_land_use == 4: # i cell (central cell) is Green
					self.weights_range = 72



				distance_band_num = 0
				for distance_band in self.list_distance_bands:
					distance_band_num += 1
					for h in distance_band:
						print("H: ", h, " distance_band: ", distance_band)
						new_row = self.central_row + h[0]
						new_col = self.central_col + h[1]

						try: 
							h_land_use = matrix[new_row, new_col]
						except:
							h_land_use = None
							print("h_land_use outside of bounds")
							break 
						print("new_row: ", new_row, "new_col: ", new_col, "h_land_use: ", h_land_use)

						
						if h_land_use == 0:
							self.sum_XtoC += weights[self.weights_range + 5][distance_band_num]
							self.sum_XtoI += weights[self.weights_range + 11][distance_band_num]
							self.sum_XtoH += weights[self.weights_range + 17][distance_band_num]
							self.sum_XtoG += weights[self.weights_range + 23][distance_band_num]

						if h_land_use == 1:
							self.sum_XtoC += weights[self.weights_range + 2][distance_band_num]
							self.sum_XtoI += weights[self.weights_range + 8][distance_band_num]
							self.sum_XtoH += weights[self.weights_range + 14][distance_band_num]
							self.sum_XtoG += weights[self.weights_range + 20][distance_band_num]
						
						if h_land_use == 2:
							self.sum_XtoC += weights[self.weights_range + 1][distance_band_num]
							self.sum_XtoI += weights[self.weights_range + 6][distance_band_num]
							self.sum_XtoH += weights[self.weights_range + 12][distance_band_num]
							self.sum_XtoG += weights[self.weights_range + 18][distance_band_num]

						if h_land_use == 3:
							self.sum_XtoC += weights[self.weights_range + 3][distance_band_num]
							self.sum_XtoI += weights[self.weights_range + 9][distance_band_num]
							self.sum_XtoH += weights[self.weights_range + 15][distance_band_num]
							self.sum_XtoG += weights[self.weights_range + 21][distance_band_num]

						if h_land_use == 4:
							self.sum_XtoC += weights[self.weights_range + 4][distance_band_num]
							self.sum_XtoI += weights[self.weights_range + 10][distance_band_num]
							self.sum_XtoH += weights[self.weights_range + 16][distance_band_num]
							self.sum_XtoG += weights[self.weights_range + 22][distance_band_num]	

				
				#self.max_potential = 
				#for potential_value in self.list_potential_value:

				self.P_XtoC = self.stochastic_disturbance * (1 + self.sum_XtoC)
				self.P_XtoI = self.stochastic_disturbance * (1 + self.sum_XtoI)
				self.P_XtoH = self.stochastic_disturbance * (1 + self.sum_XtoH)
				self.P_XtoG = self.stochastic_disturbance * (1 + self.sum_XtoG)
				self.list_potential_value = [self.P_XtoC, self.P_XtoI, self.P_XtoH, self.P_XtoG]

				max_index = self.list_potential_value.index(max(self.list_potential_value))
				# print("max_index: ", max_index)
				changed_state_matrix[row][col] = max_index + 1




				"""
				TODO:
					ADD weight range for vacant
	
				"""


				# 		for potential in range(len(list_potential_land_use)-1):

				# 			if matrix[new_row, new_col] == 1: 
				# 				centralLandUsetoSomething = weights[potential+1][distance_band_num]
				# 			if matrix[new_row, new_col] == 2: 
				# 				centralLandUsetoSomething = weights[potential+2][distance_band_num]
				# 			if matrix[new_row, new_col] == 3: 
				# 				centralLandUsetoSomething = weights[potential+3][distance_band_num]
				# 			if matrix[new_row, new_col] == 4: 
				# 				centralLandUsetoSomething = weights[potential+4][distance_band_num]
				# 			if matrix[new_row, new_col] == 5: 
				# 				centralLandUsetoSomething = weights[potential+5][distance_band_num]

				# 			potential += 6










				# 		try:
				# 			if matrix[new_row, new_col] == matrix[self.central_row, self.central_col]:
				# 				Ihd = 1
				# 			else: 
				# 				Ihd = 0
				# 		except: Ihd = 0

						
				# 		#sMax = [0, 0]
						
				# 		if Ihd == 1:
				# 			if self.central_land_use == 1: # industrial to something
				# 				ItoSomething = weights[0+1][distance_band_num] * Ihd
				# 				print("\n\n############\n\nItoSomething: ",ItoSomething,"\n\n###########\n\n")

				# 				sum_result_ItoSomething = sum_result_ItoSomething + ItoSomething
				# 				list_potential_value[0] = sum_result_ItoSomething

				# 			if self.central_land_use == 2: # commercial to something
				# 				CtoSomething = weights[20+1][distance_band_num] * Ihd
				# 				print("\n\n############\n\nCtoSomething: ",CtoSomething,"\n\n###########\n\n")
								
				# 				sum_result_CtoSomething = sum_result_CtoSomething + CtoSomething
				# 				list_potential_value[1] = sum_result_CtoSomething

				# 			if self.central_land_use == 3: # housing to something
				# 				pass

				# 			if self.central_land_use == 4: # green to something
				# 				pass

				# 			if self.central_land_use == 5: # vacant to something
				# 				pass

				
				# print("sum_result_ItoSomething: ", sum_result_ItoSomething)
				# print("sum_result_CtoSomething: ", sum_result_CtoSomething)
				# max_index = list_potential_value.index(max(list_potential_value))
				# print("max_index: ", max_index)
				# changed_state_matrix[row][col] = max_index + 1
				

		return changed_state_matrix


						# for land_use_h in range(0, len(list_potential_land_use)):
						# 	if self.central_land_use == 1: # industrial to something
						# 		ItoSomething = weights[land_use_h][distance_band_num] * Ihd


						# 		sum_result = sum_result + (matrix_pesos[d][tipo_suelo_queremos][potencial_de_cada_tipo_suelo] * Ihd)



						# 	if self.central_land_use == 2: # commercial to something
						# 		pass
						# 	if self.central_land_use == 3: # housing to something
						# 		pass
						# 	if self.central_land_use == 4: # green to something
						# 		pass
						# 	if self.central_land_use == 5: # vacant to something
						# 		pass



						



						#sum_result = sum_result + (matrix_pesos[d][tipo_suelo_queremos][potencial_de_cada_tipo_suelo] * Ihd)

						



						# i = 0
						# for potential_land_use in list_potential_land_use:
						# 	i += 1
						# 	if matrix[new_row, new_col] == tipo_suelo_potencial:
						# 		Ihd = 1
						# 	else:
						# 		Ihd = 0

				# 			for potencial_lista_ila... in range(0,100):

				# 				suma = suma + (matrix_pesos[d][tipo_suelo_queremos][potencial_de_cada_tipo_suelo] * Ihd)

				# 				list_potential_value.insert(i, perturbation * (1 + suma))

				# max_potential = list_potential_value.max_index

				# matrix[col][row] = max_potential


	# def white_transition(self, matrix, iterations, number_of_bands):



	# 	list_potential_land_use = ['Industrial', 'Commercial', 'Residential', 'Green', 'Vacant']
	# 	Ihd = 1
	# 	suma = 0
	# 	list_potential_value = []

	# 	for i in range(0, iterations):

	# 		for row in range(matrix.shape[0]):
	# 			for col in range(matrix.shape[1]):
	# 				self.central_col = col
	# 				self.central_row = row

	# 				for distance_band in range(0,number_of_bands):
	# 					for h in self.list_distance_bands:
	# 						i = 0
	# 						for potential_land_use in list_potential_land_use:
	# 							i += 1
	# 							if matrix[h] == tipo_suelo_potencial:
	# 								Ihd = 1
	# 							else:
	# 								Ihd = 0

	# 							for potencial_lista_ila... in range(0,100):

	# 								suma = suma + (matrix_pesos[d][tipo_suelo_queremos][potencial_de_cada_tipo_suelo] * Ihd)

	# 								list_potential_value.insert(i, perturbation * (1 + suma))

	# 				max_potential = list_potential_value.max_index

	# 				matrix[col][row] = max_potential






















	# # d = 

	# for distance_band:
	#   for h_cell_index:
	#       for potential:


	








	def update_array(self,array):
		new_array = np.copy(array)
		rows, cols = array.shape

		for i in range(rows):
			for j in range(cols):
				# Extract the neighborhood of the current cell
				neighborhood = array[max(0, i-1):min(rows, i+2), max(0, j-1):min(cols, j+2)]
				
				# Apply the rule to update the new_array
				new_array[i, j] = self.apply_cellular_automata_rule(array[i, j], neighborhood)

		return new_array
