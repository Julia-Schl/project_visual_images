from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player

#This is the pages.py file. Here we structure how our pages and pagesequence function.
#Each page has its own class where you always specify form_model = Player as we have players for each page
#and we have the form_fields in a list which indicate the variables we have on that page. There will be
#more functionality added here but this is a good start. 

class Welcome(Page):
    #def is_displayed(self):
        #return self.num_rounds == 1
    pass

class Politician1_competence(Page):
    form_model = 'player' 

    # Dynamically set form_fields
    def get_form_fields(self):
        # Check the round or instance to decide which field to use
        if self.round_number == 1:  # Adjust logic based on your setup
            return ['popout_question_competence_1', 'picture_assignment_1']
        elif self.round_number == 2:
            return ['popout_question_competence_2', 'picture_assignment_2']

    # Pass dynamic variables to the template
    def vars_for_template(self):
        if self.round_number == 1:
            return {
                'field_name': 'popout_question_competence_1',
                'field_value': self.player.popout_question_competence_1,
                'picture_field': 'picture_assignment_1',  
                'current_picture': self.player.picture_assignment_1,
                'player_group': self.player.group_assignment,  # Group assignment for the player
                'available_pictures': Constants.groupPictures[self.player.group_assignment],  # Pictures for the player's group
            }
        elif self.round_number == 2:
            return {
                'field_name': 'popout_question_competence_2',
                'field_value': self.player.popout_question_competence_2,
                'picture_field': 'picture_assignment_2', 
                'current_picture': self.player.picture_assignment_2, 
                'player_group': self.player.group_assignment,  # Group assignment for the player
                'available_pictures': Constants.groupPictures[self.player.group_assignment],  # Pictures for the player's group
            }
    
    def is_displayed(self):
        return True

class Politician2_femininity(Page):
    form_model = Player
    form_fields = ["popout_question_femininity"]
    
    #def is_displayed(self):
        #return self.num_rounds == 1

class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question']

    #def is_displayed(self):
        #return self.num_rounds == 1

class EndPage(Page):
    #style: this is a good example of the style 'CamelCase' that one normally uses for classes
    form_model = Player

    #def is_displayed(self):
        #return self.num_rounds == 1

#Here we define in which ordering we want the pages to be shown. We always start with a Welcome page and end with an End page.
#page_sequence = [Welcome,
                #Politician1_competence,
                #Politician2_femininity,
                #DemoPage,           
                #EndPage]

page_sequence = [Welcome, 
                Politician1_competence]
