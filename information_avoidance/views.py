from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import numpy.random

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
            if (self.round_number % Constants.rounds_per_supergame != 1):
                previous_choice = self.participant.vars[str(self.round_number - 1)]
            else:
                previous_choice = None
        except KeyError:
            previous_choice = None
        
        #lotteries = zip([round(a*100) for a in Constants.probs1], [round(b * 100) for b in Constants.probs2], Constants.outcome1, Constants.outcome2, Constants.values)
        return{"previous_choice": previous_choice}

    def before_next_page(self):
        self.participant.vars[str(self.round_number)] = self.player.chosen_option

        multiplier = None
        if (self.player.chosen_option == "A"):
            multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsA)
        elif (self.player.chosen_option == "B"):
            multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsB)
        elif (self.player.chosen_option == "C"):
            multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsC)

        print(multiplier)
        multiplier = multiplier/10.0
        # idx = Constants.values.index(self.player.chosen_option)
        # prob_success = Constants.probs1[idx]

        # outcomes = [True] * int(prob_success*10) + [False] * int((1 - prob_success) * 10) # Relies on probabilities being multiples of 10
        # self.player.outcome = random.choice(outcomes)
        # multiplier = None
        # if (self.player.outcome):
        #     multiplier = Constants.outcome1[idx]
        # else:
        #     multiplier = Constants.outcome2[idx]

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
        return((self.round_number % Constants.rounds_per_supergame == 0) or self.player.treatment == "optional")

    # def before_next_page(self):
    #     if (self.player.treatment == "mandatory"):
    #         self.player.information_shown = True
    #     if (self.player.information_shown):
    #         self.participant.vars[str(self.round_number)] = self.player.chosen_option

    #         multiplier == 
    #         if (self.player.chosen_option == "A"):
    #             multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsA)
    #         elif (self.player.chosen_option == "B"):
    #             multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsB)
    #         elif (self.player.chosen_option == "C"):
    #             multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsC)

    #         multiplier *= 0.1

    #         self.player.earned = float(self.player.investment * multiplier)
    #         self.player.earned_total = self.player.earned + (Constants.tokens_per_subgame - self.player.investment)
    #         self.player.payoff = self.player.earned_total


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
        pass
        # for fixed_player in self.subsession.get_players():
            # Boolean to keep track if player has set their information variables
            # found_info = False 

            # If player chose to view the outcome of someone else
            # Added "True" predicate temporarily for static information outcomes
            # if (fixed_player.treatment == "other" or fixed_player.treatment == "no_other" or True ):
            #     own_choice = fixed_player.chosen_option
            #     idx = Constants.values.index(own_choice)
            #     info_idx = (idx + 1) % len(Constants.values)
            #     fixed_player.info_option = Constants.values[info_idx]
            #     fixed_player.info_investment = Constants.tokens_per_subgame
            #     fixed_player.info_outcome = True
            #     fixed_player.info_earned = float(fixed_player.info_investment * Constants.outcome1[info_idx])
            #     found_info = True

                # players = self.subsession.get_players()
                # random.shuffle(players)

                # for p in players:
                #     if (p.chosen_option != own_choice):
                #         fixed_player.info_option = p.chosen_option
                #         fixed_player.info_investment = p.investment
                #         fixed_player.info_outcome = p.outcome
                #         fixed_player.info_earned = p.earned
                #         found_info = True
                #         break

            # If player chose to view their own alternate outcome
            # if (found_info == False):
            #     if (fixed_player.chosen_option == "A"):
            #         fixed_player.info_option = "B"
            #     else:
            #         fixed_player.info_option = "A"

            #     print(fixed_player.info_option)
            #     fixed_player.info_investment = fixed_player.investment

            #     if (fixed_player.info_option == "A"):
            #         prob_success = 0.5
            #     else:
            #         prob_success = 0.8

            #     outcomes = [True] * int(prob_success*10) + [False] * int((1 - prob_success) * 10)
            #     fixed_player.info_outcome = random.choice(outcomes)
            #     multiplier = 0
            #     if (fixed_player.info_option == "A" and fixed_player.info_outcome == True):
            #         multiplier = 4
            #     elif (fixed_player.info_option == "A" and fixed_player.info_outcome == False):
            #         multiplier = 0
            #     elif (fixed_player.info_option == "B" and fixed_player.info_outcome == True):
            #         multiplier = 1.5
            #     elif (fixed_player.info_option == "B" and fixed_player.info_outcome == False):
            #         multiplier = 0.5

            #     fixed_player.info_earned = float(fixed_player.info_investment * multiplier)


page_sequence = [
    Introduction,
    PRA,
    Instructions1,
    Instructions2,
    Supergame,
    Outcome,
    Information,
    #WaitForBets,
    Show_Information,
    Survey1,
    Survey2,
    Survey3,
    Survey4
]
