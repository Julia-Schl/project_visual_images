from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player

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

    def is_displayed(self):
        return True

class Politician2_femininity(Page):
    form_model = Player
    form_fields = ["popout_question_femininity"]
    
    def is_displayed(self):
        print(f"Politician2_femininity is_displayed: round_number={self.round_number}")
        return self.round_number == 2

class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question']

    def is_displayed(self):
        print(f"DemoPage is_displayed: round_number={self.round_number}")
        return self.round_number == 2

class EndPage(Page):
    #style: this is a good example of the style 'CamelCase' that one normally uses for classes
    form_model = Player

    def is_displayed(self):
        print(f"EndPage is_displayed: round_number={self.round_number}")
        return self.round_number == 2

#Here we define in which ordering we want the pages to be shown. We always start with a Welcome page and end with an End page.
page_sequence = [Welcome, 
                Page1,
                Politician2_femininity,
                DemoPage, 
                EndPage
                ]
