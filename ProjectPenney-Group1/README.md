## Project Penney

This repository contains files which can be used to simulate a variation of Penney's Game known as the Humble-Nishiyama Randomness Game, in which two players compete to see how many times a selected three-color sequence (Black Black Red, Red Black Red, etc.) appears in a shuffled deck of cards. When a player's chosen sequence appears, they get all of the drawn cards up to that point. The winner is determined in one of two ways: highest number of cards held or highest number of times a player's sequence appeared, known as a "trick".

Files included:

* `simulation.py`: A Python file with code to run a function which simulates two version of Penney's Game for a given number of iterations, with an option to set a random seed for reproducibility. **Version 1** determines the winner by whichever player has the most cards in their pile. **Version 2** assigns points to tricks, and whichever player wins the most tricks wins the game. This function can run N additional game iterations and augment the results to the existing ones.

* `heatmap.py`: A Python file with code to run a function which converts the results of the simulation (stored as json files) into probability matrices and generates two heatmaps of said probabilities for both versions of the game.

Data for each simulation are stored as json files in the `data` folder. The data folder shows game data, deck history, and player win counts for both the tricks and total cards game mode. The game data files include the total player 1 wins for each card hand and the total games played, this data is used to calculate the probabilities. Heatmaps are stored in the `figures` folder with names `num_cards_probs.png` and `num_tricks_probs.png`. By default, there is no random seed set. To specify one, set the `random_seed` parameter when calling the simulation function. 


## Write Ups
### Simulation Team

* Patrick Church: I worked on developing the simulation code and the logic behind it. I designed and wrote the algorithms that make the game simulation run smoothly. Additionally, I helped create the files where we store the simulation data, ensuring that the data is correctly updated after each time the function is run. This makes sure that the calculations are accurate and include every instance of the function being run.

* Luke Schleck: I worked on developing the logic behind the simulation and helped with implementing the code for it. I helped to brainstorm how we could store the files and when they should be reaccesesed in order to create the probabilities for the heatmap. I helped with debugging the simulation in order to ensure that it was outputting the correct results and crosschecked it with the actual probabilities we should expect to be seeing.

### Data Management/Processing Team

* Dev Saxena: I worked on converting our stored win data and round data into a probability matrix returned as a pandas dataframe for the data visualization team to use. I also helped create files to store game data from each new and previous round to make sure it can be calculated accordingly.

* Aarya Kagalwala: I worked on creating the function that converted the simulation team's data outputs into files (data folder containing number of decks, wins, and probabilities) that the visualization team can utilize. Additionally, I helped create the function to update the files for each new round as we ran more rounds of the game. I also created a function to output the probabilities as a pandas dataframe so that it can be effectively visualized. 

### Data Visualization Team
* Annie Wicker: I worked on the function to generate the heatmaps and determine a color palette that would best convey the results. We used a red-white-green gradient color palette to represent low-medium-high win probabilities. We also worked with the Data Management and Processing team to adjust the heatmap function based on their determinations of the best way to store the simulation data.

* Colin Purtell: I worked on the aesthetics of the heatmap, ensuring that labels and legends were readable and professional. I also was responsible for creating this README file, as well as working with the files provided by the simulation team and ensuring they would be read and converted properly to be used in our visualization function. Outside of my assigned tasks, I worked with the other two teams to brainstorm efficient data storage and output methods, debug code, add the interactive element to the simulation file, and ensure that our repository fulfilled the project instructions.
