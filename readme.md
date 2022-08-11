# Read Me

## Purpose
The purpose of this program is to drive a dog training box.
The box training run on a rasberry pi, with :
- Two buttons, each one covering alf of the screen
- A reward distributor

Type "python3 main.py help" to run it

## Technical description
### Overall structure 
Main
 + Game
   + Db
   + Display
   + Strategy
     + Db
     + Display
     + DogConfig
     + Images

The config is load from a json file
The json file must contain:
- strategy: class of the strategy
- dog_name

#### DogConfig :
Contains a link to the json input parameters
The get method returns the value of the entry in the json, if exist

### Images

