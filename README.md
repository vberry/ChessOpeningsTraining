# Chess Opening Trainings

This project comes from an old chess opening training iPad app I used for 10 years and that is not maintained anymore. 

I managed to extract data the app contained in sqlite form. 
Then I needed programs to extract the data ant put it into a more exploitable form. 
I currently chose a graph DB management system: exploring chess openings is like navitgating from one position to another after all. 

Chess board visualizations are also tested here in python notebooks.

The main app allowing to comfortably explore and exploit the data remains to be done.

## Dev notes
Tests should be provided for each function
As much as possible ask to run tests first when asking to run a script (see example.py)
Each script (not notebook) can be run from the project's root folder by typing:
<code>uv run src/chessopeningstraining/script_name.py arg1 arg2 ...</code>

