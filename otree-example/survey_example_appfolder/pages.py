from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random

#This is the pages.py file. Here we structure how our pages and pagesequence function.
#Each page has its own class where you always specify form_model = Player as we have players for each page
#and we have the form_fields in a list which indicate the variables we have on that page. There will be
#more functionality added here but this is a good start. 

class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1
    pass

class Page1(Page):
    form_model = 'player'
    form_fields = ['popout_question_competence', 'picture_assignment']

    def vars_for_template(self):
        #fetch the group_pictures from session.vars
        group_pictures = self.session.vars.get('group_pictures', {})

        #access the available pictures for the current player's group
        player_group = self.player.group_assignment
        available_pictures = group_pictures.get(player_group, [])

        #get the assigned picture 
        assigned_picture = self.player.picture_assignment 
        
        #construct the image path dynamically
        image_path = f"/static/Group_{self.player.group_assignment}_full/P_{assigned_picture}.png"
        
        # Randomize which question to show
        question_set = ['competence', 'trustworthiness']
        selected_question = random.choice(question_set)

        self.player.displayed_question = selected_question

        #send the variables to the HTML page 
        return {
            'group_pictures': available_pictures,
            'assigned_picture': assigned_picture,
            'image_path': image_path,
            'displayed_question': selected_question  
            }
        

    def is_displayed(self):
        return True


class Politician2_femininity(Page):
    form_model = Player
    form_fields = ["popout_question_femininity"]
    
    def is_displayed(self):
        #if player is in round X display this page
        return self.round_number == 10

class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question']

    def is_displayed(self):
        #print(f"DemoPage is_displayed: round_number={self.round_number}")
        return self.round_number == 10

class EndPage(Page):
    #style: this is a good example of the style 'CamelCase' that one normally uses for classes
    form_model = Player

    def is_displayed(self):
       # print(f"EndPage is_displayed: round_number={self.round_number}")
        return self.round_number == 10

#Here we define in which ordering we want the pages to be shown. We always start with a Welcome page and end with an End page.
page_sequence = [Welcome, 
                Page1,
                Politician2_femininity,
                DemoPage, 
                EndPage
                ]
