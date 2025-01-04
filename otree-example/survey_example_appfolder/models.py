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

author = 'your names and team objective go here'
doc = 'Your app description goes here'

class Constants(BaseConstants):
    name_in_url = 'survey-example'
    players_per_group = None
    num_rounds = 1

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    #we will only come to the group class when we look at advanced methods
    pass


class Player(BasePlayer):
    #this is the most important feature of this file. We can collect all the variables used on the html pages here
    
#The Variables are structured on the base of pages
    popout_question_competence = models.IntegerField(
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