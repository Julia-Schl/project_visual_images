from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random

class Welcome(Page):
    def is_displayed(self):
        return self.round_number == 1


class Page1(Page):
    form_model = 'player'
    form_fields = ['popout_question_competence', 'picture_assignment']

    def vars_for_template(self):
        # Fetch the group_pictures from session.vars
        group_pictures = self.session.vars.get('group_pictures', {})

        # Access the available pictures for the current player's group
        player_group = self.player.group_assignment
        available_pictures = group_pictures.get(player_group, [])

        # Get the assigned picture
        assigned_picture = self.player.picture_assignment 

        # Construct the image path dynamically
        image_path = f"/static/Group_{self.player.group_assignment}/P_{assigned_picture}.png"

        # Randomize which question to show
        question_set = ['competence', 'trustworthiness']
        selected_question = random.choice(question_set)

        self.player.displayed_question = selected_question

        # Send the variables to the HTML page
        return {
            'group_pictures': available_pictures,
            'assigned_picture': assigned_picture,
            'image_path': image_path,
            'displayed_question': selected_question  
        }

    def is_displayed(self):
        return 1 <= self.round_number <= 10


class Page2(Page):
    form_model = Player
    form_fields = ["popout_question_femininity"]

    def is_displayed(self):
        return 11 <= self.round_number <= 20


class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question']

    def is_displayed(self):
        return self.round_number == 20


class EndPage(Page):
    form_model = Player

    def is_displayed(self):
        return self.round_number == 20


# Here we define the ordering of the pages.
page_sequence = [
    Welcome,
    Page1,
    Page2,
    DemoPage,
    EndPage
]