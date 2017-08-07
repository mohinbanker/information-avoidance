from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Introduction(Page):
    def is_displayed(self):
        return(self.subsession.initial_round)

class PRA(Page):
    def is_displayed(self):
        return(self.subsession.initial_round)

class Instructions1(Page):
    def is_displayed(self):
        return(self.subsession.initial_round)

class Instructions2(Page):
    def is_displayed(self):
        return(self.subsession.initial_round)

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
        self.player.tokens += self.player.earned + (Constants.tokens_per_subgame - self.player.investment)




class Outcome(Page):
    def vars_for_template(self):
        return{"tokens_not_invested": Constants.tokens_per_subgame - self.player.investment}

class Information(Page):
    form_model = models.Player
    form_fields = ["information_shown"]

    def before_next_page(self):
        if (self.player.treatment == "no_self" or self.player.treatment == "no_other"):
            self.player.information_shown = True

class Show_Information(Page):
    def is_displayed(self):
        return(self.player.information_shown)

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

page_sequence = [
    Introduction,
    PRA,
    Instructions1,
    Instructions2,
    Supergame,
    Outcome,
    Information,
    #Show_Information,
    Survey1,
    Survey2,
    Survey3,
    Survey4
]
