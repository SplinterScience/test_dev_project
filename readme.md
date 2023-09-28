# Web App Setup and Usage Guide

## Setup

1. **Install Dependencies**: 
    Begin by installing the necessary Python packages using pip.
    ```bash
    pip install -r requirements.txt
    ```
    ** Make sure to have django installed through 
    
    ```bash
    pip install django
    ``

2. **Navigate to the Project Directory**: 
    Change your current directory to the main project folder.
    ```bash
    cd ./test_dev_project
    ```

3. **Run the Django Development Server**: 
    Start the Django server to host your web application locally.
    ```bash
    python manage.py runserver
    ```

## Accessing the Web App

1. **Open Your Web Browser**: 
    Navigate to:
    ```
    127.0.0.1:8000/
    ```

2. **Load Your Data**: 
    - Upload the `empire.json` when prompted.

3. **Note on Data Files**:
    Ensure that the `millennium-falcon.json` and `universe.db` files are placed in the following directory before starting the server:
    ```
    test_dev_project/test_dev_app/data/
    ```

## Running the Python Script via CLI

1. **Navigate to the main project folder:**
    ```bash
    cd ./test_dev_project
    ```

2. **Locate the `universe.db` files:**
    ```
    test_dev_project/test_dev_app/data/
    ```

3. **Execute the script with the necessary arguments:**
    ```bash
    python give-the-odds.py ./test_dev_app/data/millennium-falcon.json ./test_dev_app/data/empire.json
    ```


## You can also play along and modify the universe database through ./test_dev_app/data/GenerateExtraExamples.py and generate new databases.

## The main algorithm is within the GraphPlanet class -> findAllPossiblePathsAndSurvivals()

## Exceptions and Edge Cases Handled

## Millennium JSON File
- **File Format**: Ensure the uploaded file is a valid JSON. If not, raise an error.
- **Autonomy**: 
    - Verify the `autonomy` attribute contains an integer value.
    - Verify the `autonomy` attribute is not negative
- **Departure**: 
    - Verify the `departure` attribute contains a string value.
    - Verify that the value of the `departure` attribute exists in the universe database
- **Arrival**: 
    - Verify the `arrival` attribute contains a string value.
    - Verify that the value of the `arrival` attribute exists in the universe database
- **Route Database**: Contribute the `route_db` attribute contains a string value.

## Empire JSON File
- **Countdown**: 
    - Ensure the `countdown` attribute contains an integer value.
    - Ensure the `countdown` attribute doesn't  contain a negative value.
- **Bounty Hunters List**: Check if the `bounty_hunters` attribute is a list.
- **Bounty Hunters Type**: Verify all elements within `bounty_hunters` are dictionaries.
- **Bounty Hunters Attributes**:
  - Ensure each dictionary inside `bounty_hunters` contains exactly two items.
  - The keys must be 'planet' and 'day'.
  - Their respective types must be a string and an integer.

## Universe Database
- **File Extension**: Confirm the loaded data has a `.db` extension, indicating SQLite data.
- **Table Existence**: Ensure the data contains tables.
- **Routes Table**: Verify the presence of a table named 'routes'.
- **Travel Time Consistency**: 
    - Check for inconsistencies in travel times. For instance, if the travel time from Jupiter to Mars is 5, it should also be 5 from Mars to Jupiter.
    - A negative travel time is also detected
- **Empty Database**: Ensure the uploaded database is not empty.
- **Required Columns**: Verify the table contains required columns: `origin`, `destination`, and `travel_time`.
- **Data Types**:
  - The `origin` and `destination` values should be strings.
  - The `travel_time` value should be an integer.
- **Redudancy**:
   - If the databse contains two redudunt rows with same origin and destination. Despite the travel_time value, whether it is the same or not, an exception is raised.

  ## If there is no route between origin and destination raise an exception or show it on screen !
  ## The algorithm should work correctly even if the graph is not a fully connected graph. 
