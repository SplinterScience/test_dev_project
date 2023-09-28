from test_dev_app.Logic.CaptureProbability import calculateCaptureprobability
from test_dev_app.Logic.helper_functions import *
from test_dev_app.Logic.error_class import error_class


class GraphPlanet:
    '''
    The initialization function for a GraphPlanet object.

    Parameters:
    num_planets: int. Number of planets (nodes) in the graph

    A GraphPlanet object contains:
    1- matrix: a list of lists. A diagonal matrix where the indices represent the planet id and the value represents the travel time
    2- planet_ID: dict. A dictionary where keys are the planet names are values correspond to the planet id
    3- self.counter: int. A counter to assign ids to planets in the function add_edge
    4- AllPossiblePathsAndTravelTime: a list of lists. 
        Each element in AllPossiblePathsAndTravelTime contains a list of the paths and the weights (travel time)
    5- FalconyAutonomy: int. Represent the autonomy of the millenium falcony
    6- captureProbas: a list that stores all the capture probabilities corresponding to all possible paths.
    '''
    def __init__(self, num_planets):
        self.num_planets=num_planets
        self.matrix=[[0 if row==col else -1 for row in range(num_planets)] for col in range(num_planets)]
        self.planet_ID={}
        self.counter=0
        self.AllPossiblePathsAndTravelTime=[]
        self.FalconyAutonomy=0
        self.captureProbas=[]
    
    def add_edge(self, planet_a, planet_b, travel_time):
        """
        Parameters
        ----------
        planet_a : int
            ID of the first planet.
        planet_b : int
            ID of the second planet.
        travel_time : int
            Time taken to travel between the two planets.
        """
        # Get the id of planet_a or assign an id if it doesn't exist
        if planet_a in self.planet_ID:
            planet_a_index=self.planet_ID[planet_a]
        else:
            self.planet_ID[planet_a]=self.counter
            planet_a_index=self.counter
            self.counter+=1
        
        # Get the id of planet_b or assign an id if it doesn't exist
        if planet_b in self.planet_ID:
            planet_b_index=self.planet_ID[planet_b]
        else:
            self.planet_ID[planet_b]=self.counter
            planet_b_index=self.counter
            self.counter+=1

        # Raise an exception if the matrix isn't diagonal.
        if self.matrix[planet_a_index][planet_b_index]!=travel_time and self.matrix[planet_a_index][planet_b_index]!=-1:
            handleException("The travel time was already assigned differently, ERROR!!")

        # Assign travel time between planet_a and planet_b (both ways).
        self.matrix[planet_a_index][planet_b_index]=travel_time
        self.matrix[planet_b_index][planet_a_index]=travel_time
        
    
    def dfs_save_all_possible_paths(self, start, end, visited, path, weight, CLI):
        """
        Perform a Depth First Search (DFS) to find all possible paths with the associated total travel time.
        All Possible paths are saved in self.AllPossiblePathsAndTravelTime
        
        
        Parameters:
        - start (int): ID of the origin planet.
        - end (int): ID of the destination planet.
        - visited (dict): Keeps track of visited planets during the DFS. 
            Format: {planet_id: boolean_visited}
        - path (list): Accumulates the path taken, consisting of planet names.

        Overview:
        The algorithm explores all possible routes from the origin to the destination, 
        and it calculates the total travel time for each route. All Possible paths are saved in self.AllPossiblePathsAndTravelTime
        """
        # Mark the current node (start) as visited.
        visited[str(start)] = True
        # Add the planet name to the paths 
        path.append(get_key_for_value(self.planet_ID,start))

        # Check if the current node is the destination (end). 
        if start == end:
            # If True, welcome to our destination planet. Add the path to our list of AllPossiblePathsAndTravelTime
            self.AllPossiblePathsAndTravelTime.append([path.copy(),weight])
        else:
            # Iterate over all unvisited neighbors with valid paths.
            # A weight of -1 indicates no direct edge between the planets.
            for planet_col_index in range(self.num_planets):
                w=self.matrix[int(start)][planet_col_index]
                if w==-1:
                    continue
                # Recursively call the function for unvisited planets to continue the search from the neighbor.
                if not visited[str(planet_col_index)]:
                    # Update the total weight by adding the edge's weight (weight + w).
                    self.dfs_save_all_possible_paths(planet_col_index, end, visited, path, weight + w, CLI)

        path.pop()
        visited[str(start)] = False
        if len(self.AllPossiblePathsAndTravelTime)==0:
            handleException("There is no possible route between the start and the destination !",CLI)


    def init_all_possible_paths(self, start, end, CLI, DEBUG=False):
        """
        Print all possible paths and their associated travel time.

        Parameters
        ----------
        start : str
            name of the origin planet.
        end : str
            name of the destination planet.
        """
        visited = {str(el): False for el in self.planet_ID.values()}

        # start_i is the index of the start planet
        start_i=self.planet_ID[start]
        # end_i is the index of the start planet
        end_i=self.planet_ID[end]
        self.dfs_save_all_possible_paths(start_i, end_i, visited, [], 0, CLI)
        
        if DEBUG==True:
            print("All possible paths between {} and {} and their total travel time are \n{}".format(start,end,self.AllPossiblePathsAndTravelTime))

    
    def findAllPossibleSurvivalsForAParticularPath(self,start,end,autonomy,BountyHuntersPlan,Countdown,route,TotalTravelTime,k=0,current_planet_i=0,current_day=0,DEBUG=False):
        """
        Compute the best route for the Millenium Falcon to avoid bounty hunters and reach its destination before a deadline.
        
        Parameters:
        - start (str): Name of the origin planet.
        - end (str): Name of the destination planet.
        - autonomy (int): Millenium Falcon's travel autonomy.
        - BountyHuntersPlan (list of lists): Contains planet names and days when bounty hunters will be present. 
            Format: [['PlanetName', day], ...]
            Example: [['Planet1Name', 6], ['Hoth', 7], ['Hoth', 8]]
        - Countdown (int): Number of days remaining before BOOM.
        - route (list): Current path taken from origin to destination.
        - TotalTravelTime (int): Cumulative travel time for the route.
        - k (int): Number of encounters with bounty hunters.
        - current_planet_i (int): ID of the current planet.
        - current_day (int): Current day of travel.

        Overview:
        The algorithm is recursive and evaluates two primary actions: wait on the current planet or move to a neighboring planet.
        
        Stopping Conditions:
        1. If TotalTravelTime exceeds Countdown - return as the destination cannot be reached in time.
        2. If 'start' is the same as 'end' - destination reached.
        3. If autonomy drops below zero - travel is not possible.
        4. If Countdown is below zero - destination cannot be reached in time.

        Actions:
        1. Wait: Stay on the current planet for a day and recursively evaluate.
        2. Move: Travel to a neighboring planet, increment the current day, and decrement Countdown. Then, recursively evaluate.

        On each action, check if bounty hunters are present on the current planet and increment 'k' if necessary.
        """
        
        if DEBUG==True:
            print("finding all possible paths between {} and {}".format(start,end))

        # Check if the total travel time for our route exceeds the countdown.
        # If it does, it's theoretically impossible to arrive on time.
        # Otherwise, explore other possibilities.
        theoreticallyPossibleToArriveBeforeBoom=False
        if TotalTravelTime<=Countdown:
                theoreticallyPossibleToArriveBeforeBoom=True
        if DEBUG==True:
            print("theoreticallyPossibleToArriveBeforeBoom is ",theoreticallyPossibleToArriveBeforeBoom)
        if theoreticallyPossibleToArriveBeforeBoom==False:
            self.captureProbas.append(1)
            return
        
        #If arrived to destination
        if start==end:
            if DEBUG==True:
                print("Arrived to destination")

            capture_proba=calculateCaptureprobability(k)
            self.captureProbas.append(capture_proba)
            return

        # If out of autonomy and not at the destination, consider recharging.
        if autonomy<0:
            if DEBUG==True:
                print("Autonomy less than 0")
            self.captureProbas.append(1)
            return
        if Countdown<0:
            if DEBUG==True:
                print("Countdown less than 0")
            self.captureProbas.append(1)
            return
        

        """
        Check conditions for further travel or waiting.

        - Ensure we haven't reached the destination.
        - Verify if timely arrival is still possible.
        - Check if there's remaining autonomy.

        If all conditions are met:
            - Travel to a neighboring planet OR
            - Wait on the current planet.
        """

        # Check for bounty hunters before proceeding.
        # BountyHuntersPlan is structured as a list of lists.
        # If bounty hunters are present on the current day and planet, increment 'k'.
        for plan in BountyHuntersPlan:
            if plan[0]==start and plan[1]==current_day:
                k+=1
                break
        
        # Go to a neighbour
        travel_time_to_neighbour=self.matrix[self.planet_ID[route[current_planet_i]]][self.planet_ID[route[current_planet_i+1]]]

        canMoveToANeighbour = (travel_time_to_neighbour<=autonomy)
        if DEBUG==True:
                print("canMoveToANeighbour is ",canMoveToANeighbour)
        if canMoveToANeighbour:
            if DEBUG==True:
                print("Will visit the neighbor ", route[current_planet_i+1])
            self.findAllPossibleSurvivalsForAParticularPath(
                start=route[current_planet_i+1],
                end=end,
                autonomy=autonomy-travel_time_to_neighbour,
                BountyHuntersPlan=BountyHuntersPlan,
                Countdown=Countdown-travel_time_to_neighbour,
                route=route,
                TotalTravelTime=TotalTravelTime-travel_time_to_neighbour,
                k=k,
                current_planet_i=current_planet_i+1,
                current_day=current_day+travel_time_to_neighbour
                )
        
        # Wait on the current planet for a day
        if DEBUG==True:
                print("Will wait on ",start)
        self.findAllPossibleSurvivalsForAParticularPath(
            start=start,
            end=end,
            autonomy=self.FalconyAutonomy,
            BountyHuntersPlan=BountyHuntersPlan,
            Countdown=Countdown-1,
            route=route,
            TotalTravelTime=TotalTravelTime,
            k=k,
            current_planet_i=current_planet_i,
            current_day=current_day+1
            )
        return

    def findAllPossiblePathsAndSurvivals(self,start,end,autonomy,BountyHuntersPlan,Countdown,CLI):
        self.init_all_possible_paths(start, end,CLI)
        for route in self.AllPossiblePathsAndTravelTime:
            self.findAllPossibleSurvivalsForAParticularPath(
                start,
                end,
                autonomy,
                BountyHuntersPlan,
                Countdown,
                route[0],
                route[1] #this is  travel time
                )
        return
    def constructMatrix(self,universe_data):
        for vertex_edge in universe_data:
            self.add_edge(vertex_edge[0], vertex_edge[1],vertex_edge[2])