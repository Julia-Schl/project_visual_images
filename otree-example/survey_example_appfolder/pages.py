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

        # Increment counters if in rounds 1 to 10
        if 1 <= self.round_number <= 10:
            if selected_question == 'competence':
                self.player.competence_question_count += 1
            elif selected_question == 'trustworthiness':
                self.player.trustworthiness_question_count += 1

        # Send the variables to the HTML page

        return {
            'group_pictures': available_pictures,
            'assigned_picture': assigned_picture,
            'image_path': image_path,
            'displayed_question': selected_question
        }

    def is_displayed(self):
        return 1 <= self.round_number <= 10

class Transition(Page):
    def is_displayed(self):
            return self.round_number == 11
class Page2(Page):
    form_model = 'player'
    form_fields = ["popout_question_femininity", "picture_assignment_femininity"]

    def vars_for_template(self):
        print(f"Player ID: {self.player.id_in_group}, Group Assignment Fem: {self.player.group_assignment_fem}")
        # Fetch the femininity pictures from session.vars
        femininity_pictures = self.session.vars.get('femininity_pictures', {})

        # Access the available femininity pictures for the current player's group
        player_group = self.player.group_assignment_fem
        available_femininity_pictures = femininity_pictures.get(player_group, [])

        # Get the assigned femininity picture
        assigned_femininity_picture = self.player.picture_assignment_femininity

        # Construct the image path dynamically
        image_path_fem =  f"/static/Group_{self.player.group_assignment_fem}/P_{assigned_femininity_picture}.png"

        # Send the variables to the HTML page
        return {
            'femininity_pictures': available_femininity_pictures,
            'assigned_femininity_picture': assigned_femininity_picture,
            'image_path_fem': image_path_fem
        }

    def is_displayed(self):
        return 11 <= self.round_number <= 20


class DemoPage(Page):
    form_model = Player
    form_fields = ['age_question']

    def is_displayed(self):
        return self.round_number == 20


class EndPage(Page):
    form_model = Player

    def vars_for_template(self):
        # Access the group and counters
        player_group = self.player.group_assignment

        # Retrieve the final counter values for the player group
        competence_count = self.session.vars['competence_counters'][player_group]
        trustworthiness_count = self.session.vars['trust_counters'][player_group]

        # Pass these values to the template for display
        return {
            'competence_count': competence_count,
            'trustworthiness_count': trustworthiness_count
        }
    def is_displayed(self):
        return self.round_number == 20


# Here we define the ordering of the pages.
page_sequence = [
    Welcome,
    Page1,
    Page2,
    EndPage
]