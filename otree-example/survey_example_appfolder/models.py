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
#import random for group assignment
import random 

author = 'Richard Neureuther, Julia Schleißheimer, Mariia Pyvovar'
doc = 'This is the app for the Candidates Pictures group of the "Designing and implementing online survey experiments" seminar.'

class Constants(BaseConstants):
    name_in_url = 'politician-pictures'
    players_per_group = None
    num_rounds = 2

    # Global dictionary for group pictures
    groupPictures = {
        0: ["1", "2"],
        1: ["3", "4"],
        2: ["5", "6"],
        3: ["7", "8"]
    }
    

class Subsession(BaseSubsession):

    def creating_session(self):
        if self.round_number == 1:
            players = self.get_players()
            num_groups = 4
            for i, p in enumerate(players):
                p.group_assignment = i % num_groups
        
        else:
            # Carry over group_assignment from the first round
            for p in self.get_players():
                p.group_assignment = p.in_round(1).group_assignment
        
         #def creating_session(self):

            # fetch players
            #players = self.get_players()
            # if we want we can shuffle the players to be more randomly distributed among groups:
            # random.shuffle(players)

            # randomly assign a group to each participant
            #num_groups = 4 
            #for i, p in enumerate(players):
                #p.group_assignment = i % num_groups
                


class Group(BaseGroup):
    #we will only come to the group class when we look at advanced methods
    pass


class Player(BasePlayer):
    #variable for group assignment
    group_assignment = models.IntegerField(initial=-1)

    #variable for picture assignment
    picture_assignment_1 = models.IntegerField(initial=-1)
    picture_assignment_2 = models.IntegerField(initial=-1)
    
    #The Variables are structured on the base of pages
    popout_question_competence_1 = models.IntegerField(
        initial=-999,
        choices =[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (-1, 'Keine Angabe')
        ],
        label="Wie schätzen Sie die Kompetenz dieser Politikerin ein?"
    )

    popout_question_competence_2 = models.IntegerField(
        initial=-999,
        choices =[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (-1, 'Keine Angabe')
        ],
        label="Wie schätzen Sie die Kompetenz dieser Politikerin ein?"
    )

    popout_question_femininity = models.IntegerField(
        initial=-999,
        choices=[
            (1, '1'),
            (2, '2'),
            (3, '3'),
            (4, '4'),
            (5, '5'),
            (-1, 'Keine Angabe')
        ],
        label="Bitte bewerten Sie, wie feminin das Gesicht dieser Politikerin auf Sie wirkt."
    )

    age_question = models.IntegerField()                          