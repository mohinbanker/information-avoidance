from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Introduction(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1)

class PRA(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1)

class Instructions1(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1)

class Instructions2(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1)

class Supergame(Page):
    form_model = models.Player
    form_fields = ["chosen_option", "investment"]

    def vars_for_template(self):
        try:
            previous_choice = self.participant.vars[str(self.round_number - 1)]
        except KeyError:
            previous_choice = None
        
        print(self.participant.vars)
        print(previous_choice)
        return{"previous_choice": previous_choice}

    def before_next_page(self):
        self.participant.vars[str(self.round_number)] = self.player.chosen_option
        if (self.player.chosen_option == "A"):
            prob_success = 0.5
        else:
            prob_success = 0.8

        outcomes = [True] * int(prob_success*10) + [False] * int((1 - prob_success) * 10)
        self.player.outcome = random.choice(outcomes)
        multiplier = None
        if (self.player.chosen_option == "A" and self.player.outcome == True):
            multiplier = 4
        elif (self.player.chosen_option == "A" and self.player.outcome == False):
            multiplier = 0
        elif (self.player.chosen_option == "B" and self.player.outcome == True):
            multiplier = 1.5
        elif (self.player.chosen_option == "B" and self.player.outcome == False):
            multiplier = 0.5

        self.player.earned = float(self.player.investment * multiplier)
        self.player.earned_total = self.player.earned + (Constants.tokens_per_subgame - self.player.investment)
        self.player.payoff = self.player.earned_total



class Outcome(Page):
    def vars_for_template(self):
        return{"tokens_not_invested": Constants.tokens_per_subgame - self.player.investment}

class Information(Page):
    form_model = models.Player
    form_fields = ["information_shown"]

    def is_displayed(self):
        # Only give option to see information if it is the last round of the supergame
        return(self.round_number % Constants.rounds_per_supergame == 0)

    def before_next_page(self):
        if (self.player.treatment == "no_self" or self.player.treatment == "no_other"):
            self.player.information_shown = True

class Show_Information(Page):
    def is_displayed(self):
        # Only show information if player consented, and it's the last round of the supergame
        return(self.player.information_shown and self.round_number % Constants.rounds_per_supergame == 0)

class Survey1(Page):
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class Survey2(Page):
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class Survey3(Page):
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class Survey4(Page):
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class WaitForBets(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):

        for fixed_player in self.subsession.get_players():
            # Boolean to keep track if player has set their information variables
            found_info = False 

            # If player chose to view the outcome of someone else
            if (fixed_player.treatment == "other" or fixed_player.treatment == "no_other"):
                own_choice = fixed_player.chosen_option
                players = self.subsession.get_players()
                random.shuffle(players)

                for p in players:
                    if (p.chosen_option != own_choice):
                        fixed_player.info_option = p.chosen_option
                        fixed_player.info_investment = p.investment
                        fixed_player.info_outcome = p.outcome
                        fixed_player.info_earned = p.earned
                        found_info = True
                        break

            # If player chose to view their own alternate outcome
            if (found_info == False):
                if (fixed_player.chosen_option == "A"):
                    fixed_player.info_option = "B"
                else:
                    fixed_player.info_option = "A"

                print(fixed_player.info_option)
                fixed_player.info_investment = fixed_player.investment

                if (fixed_player.info_option == "A"):
                    prob_success = 0.5
                else:
                    prob_success = 0.8

                outcomes = [True] * int(prob_success*10) + [False] * int((1 - prob_success) * 10)
                fixed_player.info_outcome = random.choice(outcomes)
                multiplier = 0
                if (fixed_player.info_option == "A" and fixed_player.info_outcome == True):
                    multiplier = 4
                elif (fixed_player.info_option == "A" and fixed_player.info_outcome == False):
                    multiplier = 0
                elif (fixed_player.info_option == "B" and fixed_player.info_outcome == True):
                    multiplier = 1.5
                elif (fixed_player.info_option == "B" and fixed_player.info_outcome == False):
                    multiplier = 0.5

                fixed_player.info_earned = float(fixed_player.info_investment * multiplier)


page_sequence = [
    Introduction,
    PRA,
    Instructions1,
    Instructions2,
    Supergame,
    Outcome,
    Information,
    WaitForBets,
    Show_Information,
    Survey1,
    Survey2,
    Survey3,
    Survey4
]
