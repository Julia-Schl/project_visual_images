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
    num_rounds = 20

    ## full dictionary with all groups
    groupPictures = {
        0: ["10", "21", "30", "41", "50", "61", "70", "81", "90", "101"],
        1: ["11", "20", "31", "40", "51", "60", "71", "80", "91", "100"],
        2: ["110", "121", "130", "141", "150", "161", "170", "181", "190", "201"],
        3: ["111", "120", "131", "140", "151", "160", "171", "180", "191","200"]}
    '''
    femininityPictures = {
        2: ["10", "21", "30", "41", "50", "61", "70", "81", "90", "101"],
        3: ["11", "20", "31", "40", "51", "60", "71", "80", "91", "100"],
        0: ["110", "121", "130", "141", "150", "161", "170", "181", "190", "201"],
        1: ["111", "120", "131", "140", "151", "160", "171", "180", "191","200"]} 
    '''

    # Counters for question assignments
    competence_counters = [0, 0, 0, 0]  # One counter for each group
    trust_counters = [0, 0, 0, 0]  # One counter for each group
    max_assignments = 125  # Max people per group per question type


class Subsession(BaseSubsession):

    def creating_session(self):
        # fetch all players
        players = self.get_players()

        # Initialize counters per picture per group
        if 'competence_counters' not in self.session.vars:
            self.session.vars['competence_counters'] = {group: {} for group in range(4)}  # Dictionary per group
        if 'trust_counters' not in self.session.vars:
            self.session.vars['trust_counters'] = {group: {} for group in range(4)}  # Dictionary per group

        # Initialize per-picture counters
        for group, pictures in Constants.groupPictures.items():
            for picture in pictures:
                self.session.vars['competence_counters'][group][picture] = 0
                self.session.vars['trust_counters'][group][picture] = 0

        if 1 <= self.round_number <= 10:
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
            elif self.round_number > 1 and self.round_number < 11:
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
        
        # For rounds 11-20, use PicturesFemininity
        elif 11 <= self.round_number <= 20:
            if self.round_number == 11:
                femininity_pictures = {}

                for i, p in enumerate(players):
                    p.group_assignment = p.in_round(1).group_assignment
                    p.group_assignment_fem = p.group_assignment

                    if p.group_assignment == 0:
                        group_assignment_fem = 2
                    elif p.group_assignment == 1:
                        group_assignment_fem = 3
                    elif p.group_assignment == 2:
                        group_assignment_fem = 0
                    elif p.group_assignment == 3:
                        group_assignment_fem = 1

                    # Assign group_assignment_fem to the player if needed
                    p.group_assignment_fem = group_assignment_fem
                    print(f"Group Assignment Fem: {p.group_assignment_fem}")

                    # Initialize PicturesFemininity for each player
                    femininity_pictures[p.group_assignment_fem] = Constants.groupPictures.get(p.group_assignment_fem, [])
                    available_femininity_pictures = femininity_pictures[p.group_assignment_fem][:]
                    p.set_player_pictures({"available_femininity_pictures": available_femininity_pictures})

                    # Randomly assign femininity pictures
                    random_femininity_picture = random.choice(available_femininity_pictures)
                    p.picture_assignment_femininity = random_femininity_picture
                    print(f"Pictures in round {self.round_number}: {random_femininity_picture}")

                    available_femininity_pictures.remove(random_femininity_picture)
                    p.set_player_pictures({"available_femininity_pictures": available_femininity_pictures})
                    print(f"State of dict in round {self.round_number}: {available_femininity_pictures}")
            
            # For rounds 12–20
            else:
                # Carry over group assignment and picture assignment for subsequent rounds
                for p in self.get_players():
                    p.group_assignment_fem = p.in_round(11).group_assignment_fem  # Group assignment stays constant

                    # Fetch pictures from the previous round dynamically
                    previous_round = self.round_number - 1
                    previous_pictures = p.in_round(previous_round).get_player_pictures()
                    p.set_player_pictures(previous_pictures)

                # Select a new random femininity picture
                for p in self.get_players():
                    available_femininity_pictures = p.get_player_pictures().get("available_femininity_pictures", [])
                    if available_femininity_pictures:  # Ensure there are pictures left
                        random_femininity_picture = random.choice(available_femininity_pictures)
                        p.picture_assignment_femininity = random_femininity_picture  # Save to correct field
                        print(f"Pictures in round {self.round_number}: {random_femininity_picture}")

                        # Remove the selected picture and update the player's available pictures
                        available_femininity_pictures.remove(random_femininity_picture)
                        p.set_player_pictures({"available_femininity_pictures": available_femininity_pictures})
                        print(f"State of dict in round {self.round_number}: {available_femininity_pictures}")
                    else:
                        print(f"No available pictures for Player {p.id_in_group} in round {self.round_number}")


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    # Field to store JSON data as a string
    player_pictures = models.LongStringField(initial="{}")

    #variable for group assignment
    group_assignment = models.IntegerField(initial=-1)
    group_assignment_fem = models.IntegerField(initial=-1)

    #variable for picture assignment
    picture_assignment = models.IntegerField(initial=-1)

    picture_assignment_femininity = models.IntegerField(initial=-1)

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
        initial='N/A',)

    popout_question_femininity = models.IntegerField(
        initial=-999,
        choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (-1, 'Keine Angabe')],
        label="Bitte bewerten Sie, wie feminin das Gesicht dieser Politikerin auf Sie wirkt."
    )
    age_question = models.IntegerField()

    # Counters for questions
    competence_question_count = models.IntegerField(initial=0)
    trustworthiness_question_count = models.IntegerField(initial=0)

    # Add this field to store the start time of the page
    time_on_page_start = models.StringField(initial="")

    # The existing time_spent_on_question field:
    time_spent_on_question = models.FloatField(initial=0.0)