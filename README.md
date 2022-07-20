### behavioral cloning vs inverse RL max-margin for tic-tac-toe 
## project description:
The main point of the project was having observed 9 games of tic-tac-toe between 2 optimal players come up with a machine learning algorithm that can play tic-tac-toe. Due to the little amount of data, supervised learning was out of the question and inverse RL was used instead. the agent performed very well when playing against the optimal player it observed but not so well when playing against players it has never observed before. In conclusion, even though the max-margin inverse RL algorithm is very promissing, perhaps a more advanced inverse RL algorithm should be tried (since the agent did well just not adapt to new player styles/strategies).
## Dataset used
the AI algorithm required a sequence of state action pairs of 9 tic-tac-toe games between 2 optimal players. Since this data is obviously not found online, the minimax algorithm was used to generate this data.

## instlation and execution steps
simple download this repo and navigate to the **Testing** folder, and from there open the ***irl.py***  file. from there simple run that file, it will train the model quickly and you can play against different version of it by uncommenting the one you want (there are blocks of code denoting different agents trainined in different ways, just uncomment the one you want to play against).

## Performance parameters 
the performance parameters used in this project where wether the agent tied with an optimal agent or not. that is, the "win-rate/accuracy/etc" was measured by how often it tied against an expert opponent. Since you can't possible win against an expert/optimal/minimax opponent, the best you can do is tie with it. 

## dividing up with work
all of the work was done by me since i worked on the project alone 

## licence
The GNU General Public License is the licence my project has
