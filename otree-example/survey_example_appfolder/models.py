from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import random, json 

author = 'Richard Neureuther, Julia Schleißheimer, Mariia Pyvovar'
doc = 'This is the app for the Candidates Pictures group of the "Designing and implementing online survey experiments" seminar.'

class Constants(BaseConstants):
    name_in_url = 'politician-pictures'
    players_per_group = None
    num_rounds = 10

    # Global dictionary for group pictures
    '''
    groupPictures = {
        0: ["1", "2"],
        1: ["3", "4"],
        2: ["5", "6"],
        3: ["7", "8"]
    }
    #'''

    ## full dictionary with all groups and pictures so you dont have to type it out again :)
    
    groupPictures = {
        0: ["10", "21", "30", "41", "50", "61", "70", "81", "90", "101"],
        1: ["11", "20", "31", "40", "51", "60", "71", "80", "91", "102"],
        2: ["110", "121", "130", "141", "150", "161", "170", "181", "190", "201"],
        3: ["111", "120", "131", "140", "151", "160", "171", "180", "191","200"]}
    
    

class Subsession(BaseSubsession):

    def creating_session(self):
        # fetch all players
        players = self.get_players()

        # if it is the first round 
        if self.round_number == 1:
            #define number of groups and create empty dict
            num_groups = 4
            group_pictures = {}
            #iterate over players 
            for i, p in enumerate(players):
                #assign player into group
                p.group_assignment = i % num_groups

                #initialize a dict for the player from the group Pictures dict
                group_pictures[p.group_assignment] = Constants.groupPictures.get(p.group_assignment, [])
                
                #create individual copy of the global dict for the player 
                available_pictures = group_pictures[p.group_assignment][:]
                p.set_player_pictures({"available_pictures": available_pictures})

                #randomly select a pciture ID form the dict 
                random_picture = random.choice(available_pictures)
                p.picture_assignment = random_picture 
                print(f"Picture in round {self.round_number}: {random_picture}")

                #remove selected pic from the player dict 
                available_pictures.remove(random_picture)
                p.set_player_pictures({"available_pictures": available_pictures})
                print(f"state of dict in round {self.round_number}:{available_pictures}")


        #if it is not the first round 
        else:
    # Carry over group assignment and picture assignment for subsequent rounds
            for p in self.get_players():
                p.group_assignment = p.in_round(1).group_assignment  # Group assignment stays constant
                
                # Fetch pictures from the previous round dynamically
                previous_round = self.round_number - 1
                previous_pictures = p.in_round(previous_round).get_player_pictures()
                p.set_player_pictures(previous_pictures)

            # Select a new random picture
            for p in self.get_players():
                available_pictures = p.get_player_pictures().get("available_pictures", [])
                if available_pictures:  # Ensure there are pictures left
                    random_picture = random.choice(available_pictures)
                    p.picture_assignment = random_picture
                    print(f"Picture in round {self.round_number}: {random_picture}")

                    # Remove the selected picture and update the player's available pictures
                    available_pictures.remove(random_picture)
                    p.set_player_pictures({"available_pictures": available_pictures})
                    print(f"State of dict in round {self.round_number}: {available_pictures}")
                else:
                    print(f"No available pictures for Player {p.id_in_group} in round {self.round_number}")

class Group(BaseGroup):
    pass



class Player(BasePlayer):
    
    # Field to store JSON data as a string
    player_pictures = models.LongStringField(initial="{}")

    #variable for group assignment
    group_assignment = models.IntegerField(initial=-1)

    #variable for picture assignment
    picture_assignment = models.IntegerField(initial=-1)

    #methods to handle JSON serialization and deserialization (should be in HelperMethods but I cant import them for some reason)
    def set_player_pictures(self, pictures_dict):
        """Sets the player's picture dictionary."""
        self.player_pictures = json.dumps(pictures_dict)
        
    def get_player_pictures(self):
        """Returns the player's picture dictionary."""
        return json.loads(self.player_pictures)

    #The Variables are structured on the base of pages
    popout_question_competence = models.IntegerField(
        initial=-999,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (-1, 'Keine Angabe')],
        label="Wie schätzen Sie die Kompetenz dieser Politikerin ein?"
    )
    displayed_question = models.StringField(
        initial='',)

    popout_question_femininity = models.IntegerField(
        initial=-999,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (-1, 'Keine Angabe')],
        label="Bitte bewerten Sie, wie feminin das Gesicht dieser Politikerin auf Sie wirkt."
    )

    age_question = models.IntegerField()                          