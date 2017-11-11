# LCS Implementation from github.com/ryanurbs/elcs
## Overview
Interested in LCS algorithms, I have re-written/copied the LCS implementation presented in the book Introduction to Learning Classifier Systems by Ryan Urbanowicz and Will Browne.

This was mainly to gain an understanding of how a "fully featured" LCS implementation should be structured in python.

The results of my studies are presented below

## Results
From my analysis of the code and it's corresponding documentation, I've summarized the functions of the components in the system as follows:

- *LCS Constants*
	A Class designated to hold all the parameters for an LCS - this allows for loading the configuration from a config file, and also provides a single source of truth for the parameters of the system
- *LCS ConfigParser*
	A very general class designed to parse simple configuration files in the form of VARIABLE=VALUE, cleverly this returns a dictionary representing the variables and their corresponding assignments from the config file.

- *LCS DataManager*
	A class designed to retrieve and parse data into a format for use in the LCS algorithm. This allows the developer to seperate out the concerns of data management from the rest of the system. It also provides a single location where all the data parsing is done, and where all the datasets are stored, making it easy to find errors in the dataset.

- *LCS Environment*
	A class designed to contain a datamanager, and then provide a simple interface for retrieving test samples - once it has read the dataset, it can simple return on element from the datamanager, keeping track of it's position through the file.

- *LCS Classifier*
	A class designed to be the classifer for the system, simply performs the function of verifying whether it matches or not.

- *LCS ClassifierSet*
	A class designed to hold a set of classifiers - it also contains pertinent operations for retrieving data-statistics required for the LCS algorithm such as match sets and so forth.

- *LCS Algorithm*
	The Class which composes together all the other passive data components into a LCS system.


## TakeAway

From this, my main takeaway is the use of a config file class, and a config parser. Alongside this, the dataformat class was also interesting as it enforced separation of concerns and prevented data access code from being mixed up with the underlying algorithm. In my own implementation I didn't provide a separate datamanager class and my dataaccess became intertwined with the algorithm making it hard to iterate - I will definitely be using a simmilar design pattern for my future designs from now on.
