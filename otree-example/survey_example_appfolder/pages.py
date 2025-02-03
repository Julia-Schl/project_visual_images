from otree.api import Currency as c, currency_range, safe_json
from ._builtin import Page, WaitPage
from .models import Constants, Player
import random
from datetime import datetime

class Welcome(Page):
    form_model = Player
    form_fields = ['screen_height', 'screen_width', 'operating_system']
    def is_displayed(self):
        return self.round_number == 1


class Page1(Page):
    form_model = 'player'
    form_fields = ['comp_trust', 'picture_assignment']

    def vars_for_template(self):

        # Detect if the page is being visited for the first time
        if self.player.time_on_page_start == 'NA':
            self.player.time_on_page_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            reload_page = 0 
            
        else:
            # If time_on_page_start already exists, it's a reload
            reload_page = 1  

        #fetch the group_pictures from session.vars
        group_pictures = self.session.vars.get('group_pictures', {})

        #fetch currently available pictures 
        player_group = self.player.group_assignment
        available_pictures = group_pictures.get(player_group, [])

        # Get the assigned picture
        assigned_picture = self.player.picture_assignment
        print(f"Current Picture: {assigned_picture}")

        # Construct the image path dynamically
        image_path = f"/static/Group_{self.player.group_assignment}/P_{assigned_picture}.png"

        #convert assigned pictures to string for further use
        assigned_picture = str(assigned_picture)

        # Determine the maximum limit for each question
        limit = 125

        # Get counters for this specific picture
        if self.player.displayed_question == 'NA':
            competence_count = self.session.vars['competence_counters'][player_group].get(assigned_picture)
            trustworthiness_count = self.session.vars['trust_counters'][player_group].get(assigned_picture)

            # Randomize which question to show based on the limits
            if competence_count < limit and trustworthiness_count < limit:
                # Both questions are still within the limit, so randomize
                question_set = ['competence', 'trustworthiness']
                selected_question = random.choice(question_set)

            #catch potetial error if both counter reach the limit
            elif competence_count >= limit and trustworthiness_count >= limit:
                question_set = ['competence', 'trustworthiness']
                selected_question = random.choice(question_set)
                print ("Both limits reached! Defaulting to random assignment of questions...")

            #if competence counter is full only display trust
            elif competence_count >= limit:
                selected_question = 'trustworthiness'

            #if turst counter is full only display competence 
            elif trustworthiness_count >= limit:
                selected_question = 'competence'

            # Set the displayed question for the player
            self.player.displayed_question = selected_question
        else: 
            # if reload get selected question which was already saved 
            selected_question = self.player.displayed_question


        if reload_page == 0: 
            # Increment the player's individual display counter
            if selected_question == 'competence':
                self.player.competence_question_count += 1
                self.session.vars['competence_counters'][player_group][assigned_picture] += 1

            elif selected_question == 'trustworthiness':
                self.player.trustworthiness_question_count += 1
                # Increment the group's trustworthiness counter in session.vars
                self.session.vars['trust_counters'][player_group][assigned_picture] += 1
            
            print(f'Comp Counter: {self.session.vars["competence_counters"][player_group][assigned_picture]}')
            print(f'Trust Counter: {self.session.vars["trust_counters"][player_group][assigned_picture]}')

        elif reload_page == 1: 
            print('page was reloaded and counter not updated')
            print(f'Comp Counter: {self.session.vars["competence_counters"][player_group][assigned_picture]}')
            print(f'Trust Counter: {self.session.vars["trust_counters"][player_group][assigned_picture]}')



        #send variables to html 
        return {
            'group_pictures': available_pictures,
            'assigned_picture': assigned_picture,
            'image_path': image_path,
            'displayed_question': selected_question,
            'competence_display_count': self.session.vars['competence_counters'][player_group][assigned_picture],
            'trustworthiness_display_count': self.session.vars['trust_counters'][player_group][assigned_picture],
        }

    def before_next_page(self):
        if self.player.time_on_page_start:
            start_time = datetime.strptime(self.player.time_on_page_start, '%Y-%m-%d %H:%M:%S')
            time_spent = datetime.now() - start_time
            self.player.time_spent_on_question = time_spent.total_seconds()

    def is_displayed(self):
        return 1 <= self.round_number <= 10


class Transition(Page):
    def is_displayed(self):
            return self.round_number == 11

class Page2(Page):
    form_model = 'player'
    form_fields = ["popout_question_femininity", "picture_assignment_femininity"]

    def vars_for_template(self):

        # Set the start time if it's not already set (this happens on the first visit)
        if self.player.time_on_page_start == "NA":
            self.player.time_on_page_start = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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
            'image_path_fem': image_path_fem,
            'time_spent_on_question': self.player.time_spent_on_question,  # Send the time to the HTML page
        }

    def before_next_page(self):
        if self.player.time_on_page_start:
            start_time = datetime.strptime(self.player.time_on_page_start, '%Y-%m-%d %H:%M:%S')
            time_spent = datetime.now() - start_time
            self.player.time_spent_on_question = time_spent.total_seconds()

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
    Transition,
    Page2,
    EndPage
]