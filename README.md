### behavioral cloning vs inverse RL max-margin for tic-tac-toe 
## project description:
The main point of the project was: having observed 9 games of tic-tac-toe between 2 optimal players, come up with a machine learning algorithm that can play tic-tac-toe. Due to the little amount of data, supervised learning was out of the question and inverse reinforcement learning was used instead. the agent performed very well when playing against the optimal player it observed but not so well when playing against players it has never observed before. In conclusion, even though the max-margin inverse reinforcemenet learning algorithm is very promissing, perhaps a more advanced inverse reinforcement learning algorithm should be tried (since the agent did well just not adapt to new player styles/strategies).
## Dataset used
the AI algorithm required a sequence of state action pairs of 9 tic-tac-toe games between 2 optimal players. Since this data is obviously not found online, the minimax algorithm was used to generate this data.

## installation and execution steps
simply download this repo and navigate to the **Testing** folder, and from there open the ***irl.py***  file. from there run that file, it will train the model quickly and you can play against different versions of it by uncommenting the one you want (there are blocks of code denoting different agents trainined in different ways, just uncomment the one you want to play against).

## packages 
the project uses numpy, matplotlib (only ones that need to be installed by pip if they aren't already there). so please make sure they are installed.

## Performance parameters 
the performance parameters used in this project was wether the agent tied with an optimal agent or not. that is, the "win-rate/accuracy/etc" was measured by how often it tied against an expert opponent. Since you can't possible win against an expert/optimal/minimax opponent, the best you can do is tie with it. 

## dividing up with work
all of the work was done by me since i worked on the project alone 

## licence
The GNU General Public License is the licence my project has
