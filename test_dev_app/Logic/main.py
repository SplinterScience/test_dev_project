import json
import sys
import os
from test_dev_app.Logic.helper_functions import *
from test_dev_app.Logic.GraphPlanet import GraphPlanet


    
class millennium_loader:
    def __init__(self,millennium_path,CLI):
        self.file=None
        self.autonomy=None
        self.departure=None
        self.arrival=None
        self.routes_db=None

        self.__loadMilleniumFile(millennium_path,CLI)

    def __loadMilleniumFile(self,millennium_path,CLI):
        """
        Load the Millennium file and validate its attributes.

        Parameters
        ----------
        millennium_path : str
            Path to the JSON file.
        """
        try:
            f=open(millennium_path)
            self.file=json.load(f)
        except:
            handleException("Problem when loading the millennium json file!",CLI)
        
        # Exception handling
        #=====================
        #=====================

        if isinstance(self.file['autonomy'], int):
            self.autonomy=int(self.file['autonomy'])
        else:
            handleException("'autonomy' variable is not int ",CLI)
        # ===================================================
        if isinstance(self.file['departure'], str):
            self.departure=self.file['departure']
        else:
            handleException("'departure' variable is not str ",CLI)
        # ===================================================
        if isinstance(self.file['arrival'], str):
            self.arrival=self.file['arrival']
        else:
            handleException("'arrival' variable is not str ",CLI)
        # ===================================================
        if isinstance(self.file['routes_db'], str):
            self.routes_db=self.file['routes_db']
        else:
            handleException("The dataset name is not string",CLI)

class empire_loader:
    def __init__(self,empire_path,CLI):
        self.empire_file=None
        self.countdown=None
        self.bounty_hunters=None
        self.__loadEmpireFile(empire_path,CLI)
    
    def __loadEmpireFile(self,empire_path,CLI):
        """
        Load the Empire file and validate its attributes.

        Parameters
        ----------
        empire_path : str
            Path to the JSON file.
        CLI : bool
            Indicates if the code is called from the command line or a web application.
        """
        if CLI==True:
            empire_path=open(empire_path)
        self.empire_file=json.load(empire_path)
        
        # Exception handling
        #=====================
        #=====================
        if isinstance(self.empire_file['countdown'], int):
            self.countdown=int(self.empire_file['countdown'])
        else:
            handleException("'countdown' variable is not int ",CLI)
        # ===================================================
        if isinstance(self.empire_file['bounty_hunters'], list):
            self.bounty_hunters=self.empire_file['bounty_hunters']
        else:
            handleException("'bounty_hunters' variable is not a list ",CLI)
        
        if self.__check_bountyHunterListFormatting(self.bounty_hunters)==False:
            handleException("'bounty_hunters' list problem!! ",CLI)
        
    def __check_bountyHunterListFormatting(self,lst):
        
        # Verify that all items in the list are dictionaries.
        if all(isinstance(item, dict) for item in lst):
            
            for item in lst:
                # Check if the dictionary has exactly two key-value pairs
                if len(item) != 2:
                    return False
                
                # Check if the dictionary contains the required keys and their types
                if not ('planet' in item and isinstance(item['planet'], str) and
                        'day' in item and isinstance(item['day'], int)):
                    return False
            
            # If all checks pass
            return True
        else:
            return False

def main(file2_path,file1_path="./test_dev_app/data/millennium-falcon.json"):
    """
    Parameters:
        file2_path (str): Path to the empire JSON file.
        file1_path (str): Path to the millennium JSON file.

    Notes:
        - If the web app is used, the millennium JSON file has a default path.
        - If the CLI is used, the millennium JSON file is provided in the arguments.
    """

    # CLI (bool): Determines if the CLI was used.
    # If True, exceptions are raised in the terminal.
    # If False, exceptions are displayed on screen.
    CLI=True
    if type(file2_path)!=str:
        CLI=False

    # create a miilennium falcon object to load it and check for exceptions
    millennium_falcon = millennium_loader(file1_path,CLI)

    # create a empire object to load it and check for formatting exceptions  
    empire_object=empire_loader(file2_path,CLI)
    
    # Convert bounty hunters from list of dicts to list of lists if no exceptions raised.
    for element_i in range(len(empire_object.bounty_hunters)):
        empire_object.bounty_hunters[element_i]=list(empire_object.bounty_hunters[element_i].values())
    
    # Load the universe database, universe_data is a list of lists
    universe_data=testDataLoad(millennium_falcon.routes_db,'routes',CLI)
    
    # Retrieve the unique set of all planets in the universe (removing redundancies).
    # Count the total number of distinct planets.
    ListofAllPlanets=[]
    for vertex_edge in universe_data:
        ListofAllPlanets.append(vertex_edge[0])
        ListofAllPlanets.append(vertex_edge[1])
    SetofAllPlanets=set(ListofAllPlanets)
    NumberofPlanets=len(SetofAllPlanets)


    # If NumberOfPlanets is 0 raise an exception
    if NumberofPlanets==0:
        handleException("No planets are in the universe database",CLI)

    # Verify that the value of the `departure` attribute exists in the universe database
    if millennium_falcon.departure not in SetofAllPlanets:
        handleException("'origin planet provided in the millenium json is not in the set of all planets of the db ",CLI)
        raise
    # Verify that the value of the `arrival` attribute exists in the universe database
    if millennium_falcon.arrival not in SetofAllPlanets:
        handleException("'destination planet provided in the millenium json is not in the set of all planets of the db ",CLI)
        raise

    # Create a graph and 
    g = GraphPlanet(NumberofPlanets)
    if millennium_falcon.autonomy<0:
        handleException("You are already dead man, autonomy has a negative value ",CLI)

    g.FalconyAutonomy=millennium_falcon.autonomy

    # Construct the matrix, putting edges between nodes in a matrix
    g.constructMatrix(universe_data)
    # printMatrix(g.matrix)

    g.findAllPossiblePathsAndSurvivals(
        start=millennium_falcon.departure,
        end=millennium_falcon.arrival,
        autonomy=millennium_falcon.autonomy,
        BountyHuntersPlan=empire_object.bounty_hunters,
        Countdown=empire_object.countdown,
        CLI=CLI
        )

    # Convert capture probabilities into percentages for success chances.
    Chances=[]
    Chances.extend([100 - (proba * 100) for proba in g.captureProbas])
    Chances.sort()

    return Chances[-1]

