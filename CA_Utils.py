
import numpy as np
from collections import defaultdict

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
		self.banda6 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda7 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda8 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda9 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda10 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda11 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda12 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda13 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda14 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda15 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda16 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda17 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]
		self.banda18 = [ [2, 1], [2, -1], [1,2], [1, -2], [-2, 1], [-2, -1], [-1, 2], [-1, -2] ]


		self.list_distance_bands = [ 
									self.banda1,
									self.banda2,
									self.banda3,
									self.banda4,
									self.banda5,
									self.banda6,
									self.banda7,
									self.banda8,
									self.banda9,
									self.banda10,
									self.banda11,
									self.banda12,
									self.banda13,
									self.banda14,
									self.banda15,
									self.banda16,
									self.banda17,
									self.banda18

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
		self.sum_XtoV = 0

		self.P_XtoC = 0
		self.P_XtoI = 0
		self.P_XtoH = 0
		self.P_XtoG = 0
		self.P_XtoV = 0
		
		self.list_potential_value = [self.P_XtoC, self.P_XtoI, self.P_XtoH, self.P_XtoG, self.P_XtoV]

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

		# self.potential_ItoC = 0
		# self.potential_ItoI = 0
		# self.potential_ItoH = 0
		# self.potential_ItoG = 0
		# self.potential_CtoC = 0
		# self.potential_CtoI = 0
		# self.potential_CtoH = 0
		# self.potential_CtoG = 0
		# self.potential_HtoC = 0
		# self.potential_HtoI = 0
		# self.potential_HtoH = 0
		# self.potential_HtoG = 0
		# self.potential_GtoC = 0
		# self.potential_GtoI = 0
		# self.potential_GtoH = 0
		# self.potential_GtoG = 0
		# self.potential_VtoC = 0
		# self.potential_VtoI = 0
		# self.potential_VtoH = 0
		# self.potential_VtoG = 0
		# self.potential_VtoV = 0

		self.weights_range = 0

		self.rng_0_1 = np.random.default_rng()
		#self.stochastic_disturbance = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)


		self.maximum_changes_per_land_use = 20


	# def apply_cellular_automata_rule(self,cell, neighbors):
	# 	# Define your rules here, this is just a simple example
	# 	# If cell is empty and has at least 1 developed neighbor, it becomes developed
	# 	if cell == 4 and np.sum(neighbors) >= 1:
	# 		return np.sum(neighbors)%5
	# 	else:
	# 		return cell


	def white_transition(self, matrix, weights):

		changed_state_matrix = np.zeros_like(matrix)

		#list_potential_land_use = ['Vacant','Industrial', 'Commercial', 'Residential', 'Green']
		#Ihd = 1
		#sum_result = 0
		
		#number_of_bands = 18


		# sum_result_ItoSomething = 0
		# sum_result_CtoSomething = 0
		

		#self.list_maximum_to_change = [0,0,0,0,0]
		self.list_vacants_to_change = []  # row, col, prev, sig, pot
		self.max_potential_vacant_to_change = []


		for row in range(matrix.shape[0]):
			for col in range(matrix.shape[1]):

				self.P_XtoC = 0
				self.P_XtoI = 0
				self.P_XtoH = 0
				self.P_XtoG = 0
				self.P_XtoV = 0
				self.sum_XtoC = 0 
				self.sum_XtoI = 0
				self.sum_XtoH = 0
				self.sum_XtoG = 0
				self.sum_XtoV = 0

				self.central_col = col
				self.central_row = row
				self.central_land_use = matrix[row, col]
				self.central_land_use = int(self.central_land_use)
				#print("central_row: ",self.central_row,"central_col: ", self.central_col, "central_land_use: ", self.central_land_use)



				if self.central_land_use == 5: # i cell (central cell) is vacant 
					self.weights_range = 80
				if self.central_land_use == 1: # i cell (central cell) is Industrial 
					self.weights_range = 0
				if self.central_land_use == 2: # i cell (central cell) is Commercial
					self.weights_range = 20
				if self.central_land_use == 3: # i cell (central cell) is Residential
					self.weights_range = 40
				if self.central_land_use == 4: # i cell (central cell) is Green
					self.weights_range = 60

				# TODO: CHECK VACANT TRANSITION

				distance_band_num = 0
				for distance_band in self.list_distance_bands:
					
					

					for h in distance_band:
						#print("H: ", h, " distance_band: ", distance_band)
						new_row = self.central_row + h[0]
						new_col = self.central_col + h[1]

						try: 
							h_land_use = matrix[new_row, new_col]
							if self.central_land_use == 5:

								if h_land_use == 5:
									self.sum_XtoV += weights[self.weights_range + 4][distance_band_num]
									# print("# Peso VtoV ",weights[self.weights_range+4][distance_band_num])
									# print("# Peso VtoC ",weights[self.weights_range+9][distance_band_num])
									# print("# Peso VtoI ",weights[self.weights_range+14][distance_band_num])
									# print("# Peso VtoH ",weights[self.weights_range+19][distance_band_num])
									# print("# Peso VtoG ",weights[self.weights_range+24][distance_band_num])
									self.sum_XtoC += weights[self.weights_range + 9][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 14][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 19][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 24][distance_band_num]

								if h_land_use == 1:
									# print("# Peso VtoV dado C ",weights[self.weights_range+1][distance_band_num])
									# print("# Peso VtoC dado C ",weights[self.weights_range+6][distance_band_num])
									# print("# Peso VtoI dado C",weights[self.weights_range+11][distance_band_num])
									# print("# Peso VtoH dado C ",weights[self.weights_range+16][distance_band_num])
									# print("# Peso VtoG dado C",weights[self.weights_range+21][distance_band_num])
									self.sum_XtoV += weights[self.weights_range + 1][distance_band_num]
									self.sum_XtoC += weights[self.weights_range + 6][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 11][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 16][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 21][distance_band_num]

								if h_land_use == 2:
									self.sum_XtoV += weights[self.weights_range + 0][distance_band_num]
									self.sum_XtoC += weights[self.weights_range + 5][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 10][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 15][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 20][distance_band_num]

								if h_land_use == 3:
									self.sum_XtoV += weights[self.weights_range + 2][distance_band_num]
									self.sum_XtoC += weights[self.weights_range + 7][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 12][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 17][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 22][distance_band_num]

								if h_land_use == 4:
									self.sum_XtoV += weights[self.weights_range + 3][distance_band_num]
									self.sum_XtoC += weights[self.weights_range + 8][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 13][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 18][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 23][distance_band_num]
							

							else:
						
								if h_land_use == 5:
									#self.sum_XtoV += weights[self.weights_range + 5][distance_band_num]
									self.sum_XtoC += weights[self.weights_range + 4][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 9][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 14][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 19][distance_band_num]

								if h_land_use == 1:
									self.sum_XtoC += weights[self.weights_range + 1][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 6][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 11][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 16][distance_band_num]
								
								if h_land_use == 2:
									self.sum_XtoC += weights[self.weights_range + 0][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 5][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 10][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 15][distance_band_num]

								if h_land_use == 3:
									self.sum_XtoC += weights[self.weights_range + 2][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 7][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 12][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 17][distance_band_num]

								if h_land_use == 4:
									self.sum_XtoC += weights[self.weights_range + 3][distance_band_num]
									self.sum_XtoI += weights[self.weights_range + 8][distance_band_num]
									self.sum_XtoH += weights[self.weights_range + 13][distance_band_num]
									self.sum_XtoG += weights[self.weights_range + 18][distance_band_num]
						except:
							h_land_use = None
							#print("h_land_use outside of bounds")
							#break ############## REVISAR 
							########################################
						#print("new_row: ", new_row, "new_col: ", new_col, "h_land_use: ", h_land_use)



							

					distance_band_num += 1
				#self.max_potential = 
				#for potential_value in self.list_potential_value:


				# self.stochastic_disturbance_1 = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)
				# self.stochastic_disturbance_2 = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)
				# self.stochastic_disturbance_3 = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)
				# self.stochastic_disturbance_4 = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)
				# self.stochastic_disturbance_5 = 1 + np.power((-np.log(self.rng_0_1.random())), 2.5)
				self.stochastic_disturbance_1 = 1
				self.P_XtoC = self.stochastic_disturbance_1 * (1 + self.sum_XtoC)
				self.P_XtoI = self.stochastic_disturbance_1 * (1 + self.sum_XtoI)
				self.P_XtoH = self.stochastic_disturbance_1 * (1 + self.sum_XtoH)
				self.P_XtoG = self.stochastic_disturbance_1 * (1 + self.sum_XtoG)
				self.P_XtoV = self.stochastic_disturbance_1 * (1 + self.sum_XtoV)
				self.list_potential_value = [self.P_XtoI, self.P_XtoC, self.P_XtoH, self.P_XtoG, self.P_XtoV]

				#print("list_potential_value: ", self.list_potential_value)




				# if self.central_land_use == 5: # vacant



				# 	if self.list_maximum_to_change[max_index] < 20:
				# 		previous = self.list_maximum_to_change[max_index]
				# 		#print("previ", previous)
				# 		self.list_maximum_to_change[max_index] = previous + 1
				# 		#print("after", self.list_maximum_to_change[max_index])
				# 		changed_state_matrix[row][col] = max_index + 1
				# 	else:
				# 		changed_state_matrix[row][col] = self.central_land_use
				# 		pass





				# si todos son iguales
				if all(x==self.list_potential_value[0] for x in self.list_potential_value):
					changed_state_matrix[row][col] = self.central_land_use
					#print("no hago nada")
					pass



				elif any(self.list_potential_value):
					max_index = self.list_potential_value.index(max(self.list_potential_value))

					if self.central_land_use == 5: # vacant
						#change to dictionary in the future
						self.list_vacants_to_change.append([self.central_row, self.central_col, max_index+1, max(self.list_potential_value)])
						changed_state_matrix[row][col] = 5
					else:
						#print("max_index: ", max_index)
						changed_state_matrix[row][col] = max_index + 1
						#print(changed_state_matrix)

				# si 
				else:
					#changed_state_matrix[row][col] = self.central_land_use
					pass

		


		##Change only 20 max vacant to other thing

		state_potentials = defaultdict(list)
		for row, col, state, potential in self.list_vacants_to_change:
			state_potentials[state].append((row, col, potential))

		top_potentials = {}

		for state, potentials in state_potentials.items():
			sorted_potentials = sorted(potentials, key=lambda x: x[2], reverse=True)
			top_potentials[state] = sorted_potentials[:20]


		for state, potentials, in top_potentials.items():
			for row, col, potential in potentials:
				print(state, row, col, potential)
				changed_state_matrix[row][col] = state

		# for i in self.list_vacants_to_change:
		# 	self.max_potential_vacant_to_change = self.max_potential_vacant_to_change.append(i[-1])




		# 	else:
		# 		#print("not equal", max_index+1, self.central_land_use)
		# 		if self.list_maximum_to_change[max_index] < 20:
		# 			previous = self.list_maximum_to_change[max_index]
		# 			#print("previ", previous)
		# 			self.list_maximum_to_change[max_index] = previous + 1
		# 			#print("after", self.list_maximum_to_change[max_index])
		# 			changed_state_matrix[row][col] = max_index + 1
		# 		else:
		# 			changed_state_matrix[row][col] = self.central_land_use
		# 			pass

		return changed_state_matrix


						




	# def update_array(self,array):
	# 	new_array = np.copy(array)
	# 	rows, cols = array.shape

	# 	for i in range(rows):
	# 		for j in range(cols):
	# 			# Extract the neighborhood of the current cell
	# 			neighborhood = array[max(0, i-1):min(rows, i+2), max(0, j-1):min(cols, j+2)]
				
	# 			# Apply the rule to update the new_array
	# 			new_array[i, j] = self.apply_cellular_automata_rule(array[i, j], neighborhood)

	# 	return new_array
