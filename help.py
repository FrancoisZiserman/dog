# TODO To be updated and completed
def print_help():
    print('''
To run this program, you must create a valid json file, and type : python3 main.py jsonfile.json
The json file can contains the following elements: 
    "dog_name" # Name of the dog
    "strategy": # Class of the strategy. One of the following value: 
        "AllWhite"   
        "OneImageFixRight" 
        "OneImageFixLeft" 
        "OneImageFixRandom"
        "OneImageAlternate"
        "OneImageRandom"
        "FixRight"
        "FixLeft"
        "FixRandom"
        "Alternate"
        "Random"
        "LearnFromFirst"
    "path" # Path to the directory of pictures.
    "image_selection" # Regex for image selection. 
    "interval": time between two round, in sec
    "turn_duration": max time of a turn
    "repeat_start": number of training turns
    "fail_action" # One of the following value : 
        "ERROR_SCREEN_AND_STEP_FORWARD"
        "BEEP_AND_STAY"
        "ERROR_SCREEN_AND_STAY"
        "STAY_IN_SILENCE"
    "full_screen" # true or false
    "with_motor" # true or false
    "input" # One of the following value :  
        "MOUSE"
        "CLIC"
    "reward_parameters" # technical parameters for the reward servo motor {
        "left": 2.5,
        "right": 12,
        "neutral": 12,
        "sleep_after_left": 0.2,
        "sleep_after_right": 0.2,
        "sleep_after_neutral": 0.2
    }
  }
     
"strategy" and "dog_name" are the mandatory parameters
''')