###README.txt

Project SYBIL is the next iteration of personal practical learning project SPADE, a home-brewed searching, enumerating and crawling implemetation in python.
It should be noted that this project is started by an absolute beginner experimenting in different learning approaches (read: general lack of responsibility).



Time immemorial:

TODO:
components/dbagent.py 		- basic functions implemented
components/googleagent.py   - limited search capability
components/langdetect.py    - language detecton testing
components/clientagent.py   - user interaction agent
components/mongobots.py     - bots executing tasks on/behalf mongoDB


Ver 03221:

In the root folder of project are located "executables", scripts meant to be executed by the user for performing defined tasks
Following "components" made with very hazy vision of underlaying mechanics or possible challenges.
Calling these files components because skipped over the lingo definition.

config_db				- mongodb connection parameters
dbagent.py				- component defining pymongo module implemetation and usage
ioagent.py				- intercommunication between components and misc operations during input or output of working data and results
googleagent.py			- total crap of a job on my part
langdetect.py			- experimental feature and function, separated for debug and general fuckery

TODO:
Graphing user input - output through the whole project and working out the exact alghoritm behind the desired output scenarios
queryman.py				- adding basic management of user input, connecting and exporting to the mongodb server instance, basic sanitation,
						  duplicate and illegal options checking and verification; error tracing in the case of problem