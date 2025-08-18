# Chess Opening Trainings

This project comes from an old chess opening training iPad app I used for 10 years and that is not maintained anymore. 

I managed to extract data the app contained in sqlite form. 
Then I needed programs to extract the data ant put it into a more exploitable form. 
I currently chose a graph DB management system: exploring chess openings is like navitgating from one position to another after all. 

Chess board visualizations are also tested here in python notebooks.

## A first text app 

A first text app is available in `src/opening_book_explorer`
It loads available books and trains the player against the book he chosed, with the piece color he chosed.

## To install it: 
1. clone this repo
2. install uv if this python tool is not already on your os
3. `cd` to the root dir
4. `uv sync` # this will install the required python packages

## To run it: 
1. `cd src/opening_book_explorer`
2. `uv run first_prototype.py`

## Dev notes
Tests should be provided for each function
As much as possible ask to run tests first when asking to run a script (see example.py)

The project currently contains exploratory python scripts and notebooks.

### Scripts
Each script can be run from the project's root folder by typing:
<code>uv run src/chessopeningstraining/script/script_name.py arg1 arg2 ...</code>

### Notebooks
I currently run notebooks by first launching Jupyter lab (that displays nicely SVg images) and opening them from this app.
In this way, the SVG files are displayed fine. 
There might be a way to launch jupyter from the uv project/package manager, but how to do that?
