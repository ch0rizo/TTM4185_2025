from .graph import Graph, nx, plt
import random 

class BroomstickGraph(Graph):
    def __init__(self, n=None, seed=None, **attr):
        super().__init__(**attr)
        # Check if seed is set
        if seed != None: 
            random.seed(seed)
            n = random.randint(7, 12)
        
        # Check if n is given
        if n == None:
            n = random.randint(7, 12)

        # Check if n is valid
        if n < 7 or n > 12:
            raise ValueError("The number of nodes (n) should be between 7 and 12")
        
        # Make graph 
        for i in range(n):
            self.add_node(i)
        for i in range(n//2):
            self.add_edge(i, i+1)
        for i in range(n//2, n-1):
            self.add_edge(i, n-1)





