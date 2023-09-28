import sqlite3
import os
from test_dev_app.Logic.error_class import error_class


def printMatrix(m):
    """
    Print a matrix represented as a list of lists.

    Parameters
    ----------
    m : list of lists
        Matrix to be printed.
    """
    for row in m:
        print(row)
def get_key_for_value(dictionary, target_value):
    """
    Retrieve the key corresponding to the provided value from a dictionary.
    Primarily used to get a planet name using its ID.

    Parameters
    ----------
    dictionary : dict
        Dictionary to search through.
    value : var_type
        Value whose corresponding key is sought.
    """
    return next((key for key, value in dictionary.items() if value == target_value), None)

def contains_redundant_lists(li):
    seen = set()
    for sublist in li:
        tuple_version = tuple(sublist[:2])
        if tuple_version in seen:
            return True
        seen.add(tuple_version)
    return False


def testDataLoad(data_path, table_name,CLI):
    """
    Description of your function goes here.

    Parameters
    ----------
    data_path : str
        Path to the database.db file.
    table_name : str
        Name of the table.
    CLI : bool
        Indicates if the command is from the web app or the command line.
    """
    try:
        con = sqlite3.connect("./test_dev_app/data/"+data_path)
    except sqlite3.Error as e:
        handleException("Cannot connect to the database:{} {}".format(data_path,str(e)), CLI)

    cur = con.cursor()

    try:
        # Get all table names and store them in the table_list variable
        table_list = [a[0] for a in cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")]
    except sqlite3.OperationalError as e:
        handleException("SQL error: {}".format(str(e)), CLI)

    if table_name in table_list:
        cur.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cur.fetchall()]
        required_columns = ['origin', 'destination', 'travel_time']

        if not all(col in columns for col in required_columns):
            handleException("The table does not have the required columns: origin, destination, and travel_time.", CLI)

        data=cur.execute("SELECT * FROM routes")
        rows = cur.fetchall()
        
        if len(rows)==0:
            handleException("The provided db is empty ERROR",CLI)
        
        if contains_redundant_lists(rows):
            handleException("Redundant lines in the database ! Error !!",CLI)

        for row in rows:
            origin, destination, travel_time = row
            if not isinstance(origin, str):
                handleException(f"Expected 'origin' to be a string, but got {type(origin).__name__}.", CLI)
                raise
            if not isinstance(destination, str):
                handleException(f"Expected 'destination' to be a string, but got {type(destination).__name__}.", CLI)
                raise
            if not isinstance(travel_time, int):
                handleException(f"Expected 'travel time' to be a int, but got {type(travel_time).__name__}.", CLI)
                if travel_time<0:
                    handleException(f"Negative travel time, sorry but we cannot go back in time, no regrets .. ", CLI)

        
    else:
        handleException("Didn't find a table named {}".format(table_name),CLI)
    
    # Be sure to close the connection
    con.close()
    return rows

def handleException(exception,CLI):
    if CLI==True:
        raise Exception("Hey there ! ",exception)
    else:
        error_class.errorsList.append('EXCEPTION: '+str(exception))
        raise