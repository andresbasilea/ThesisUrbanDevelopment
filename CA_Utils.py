
import numpy as np

class CA_Utils:

	def apply_cellular_automata_rule(self,cell, neighbors):
	    # Define your rules here, this is just a simple example
	    # If cell is empty and has at least 1 developed neighbor, it becomes developed
	    if cell == 1 and np.sum(neighbors) >= 1:
	        return np.sum(neighbors)%5
	    else:
	        return cell

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
