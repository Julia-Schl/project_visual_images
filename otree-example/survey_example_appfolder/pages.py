from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player

#This is the pages.py file. Here we structure how our pages and pagesequence function.
#Each page has its own class where you always specify form_model = Player as we have players for each page
#and we have the form_fields in a list which indicate the variables we have on that page. There will be
#more functionality added here but this is a good start. 

class Welcome(Page):
    pass

class Politician1_competence(Page):
    form_model = Player
    form_fields = ["popout_question_competence"]

class Politician2_femininity(Page):
    form_model = Player
    form_fields = ["popout_question_femininity"]
    


class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question']

class EndPage(Page):
    #style: this is a good example of the style 'CamelCase' that one normally uses for classes
    form_model = Player

#Here we define in which ordering we want the pages to be shown. We always start with a Welcome page and end with an End page.
page_sequence = [Welcome,
                Politician1_competence,
                Politician2_femininity,
                DemoPage,           
                EndPage]