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
        return(self.subsession.round_number == 1 or self.subsession.round_number == (Constants.rounds_per_supergame + 1))

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
        
        part = self.round_number % Constants.rounds_per_supergame
        if (part == 0):
            part = Constants.rounds_per_supergame

        first_round = ((self.round_number % Constants.rounds_per_supergame) == 1)

        #lotteries = zip([round(a*100) for a in Constants.probs1], [round(b * 100) for b in Constants.probs2], Constants.outcome1, Constants.outcome2, Constants.values)
        return{"previous_choice": previous_choice, "part": part, "first_round": first_round}

    def before_next_page(self):
        self.participant.vars[str(self.round_number)] = self.player.chosen_option

        self.player.multiplier = None
        if (self.player.chosen_option == "A"):
            self.player.multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsA)
        elif (self.player.chosen_option == "B"):
            self.player.multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsB)
        elif (self.player.chosen_option == "C"):
            self.player.multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsC)

        print(self.player.multiplier)
        self.player.multiplier = self.player.multiplier/10.0
        # idx = Constants.values.index(self.player.chosen_option)
        # prob_success = Constants.probs1[idx]

        # outcomes = [True] * int(prob_success*10) + [False] * int((1 - prob_success) * 10) # Relies on probabilities being multiples of 10
        # self.player.outcome = random.choice(outcomes)
        # self.player.multiplier = None
        # if (self.player.outcome):
        #     self.player.multiplier = Constants.outcome1[idx]
        # else:
        #     self.player.multiplier = Constants.outcome2[idx]

        self.player.earned = round(float(self.player.investment * self.player.multiplier))
        self.player.investment_return = self.player.earned - self.player.investment
        self.player.earned_total = self.player.earned + (Constants.tokens_per_subgame - self.player.investment)
        self.player.previous_payoff = self.participant.payoff
        self.player.payoff = self.player.earned_total
        self.player.not_invested = Constants.tokens_per_subgame - self.player.investment



class Outcome(Page):
    def vars_for_template(self):
        return{"tokens_not_invested": Constants.tokens_per_subgame - self.player.investment}


class Information(Page):
    def is_displayed(self):
        # Only give option to see information if it is the last round of the supergame
        return((self.round_number % Constants.rounds_per_supergame == 0) and self.player.treatment != "none")

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
    def before_next_page(self):
        if (self.player.treatment == "mandatory"):
            self.player.info_option = random.choice(["A", "B", "C"])
            self.player.information_shown = True
            self.player.info_multiplier = None
            self.player.info_investment = random.randint(1, Constants.tokens_per_subgame)
            if (self.player.info_option == "A"):
                self.player.info_multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsA)
            elif (self.player.info_option == "B"):
                self.player.info_multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsB)
            elif (self.player.info_option == "C"):
                self.player.info_multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsC)

            self.player.info_multiplier = self.player.info_multiplier/10.0            

            self.player.info_earned = float(self.player.info_investment * self.player.info_multiplier)
            self.player.info_investment_return = self.player.info_earned - self.player.info_investment
            self.player.info_earned_total = self.player.info_earned + (Constants.tokens_per_subgame - self.player.info_investment)

class InformationChoice(Page):
    form_model = models.Player
    form_fields = ["info_option"]
    def is_displayed(self):
        # Only give option to see information if it is the last round of the supergame
        return((self.round_number % Constants.rounds_per_supergame == 0) and self.player.treatment == "optional")

    def before_next_page(self):
        self.player.information_shown = (self.player.info_option != None) and (self.player.info_option != "skip_info")
        if (self.player.info_option != None and self.player.info_option != "skip_info"):
            self.player.info_multiplier = None
            self.player.info_investment = random.randint(1, Constants.tokens_per_subgame)
            if (self.player.info_option == "A"):
                self.player.info_multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsA)
            elif (self.player.info_option == "B"):
                self.player.info_multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsB)
            elif (self.player.info_option == "C"):
                self.player.info_multiplier = numpy.random.choice(Constants.multipliers, 1, p = Constants.probsC)

            self.player.info_multiplier = self.player.info_multiplier/10.0            

            self.player.info_earned = float(self.player.info_investment * self.player.info_multiplier)
            self.player.info_investment_return = self.player.info_earned - self.player.info_investment
            self.player.info_earned_total = self.player.info_earned + (Constants.tokens_per_subgame - self.player.info_investment)


class Show_Information(Page):
    def is_displayed(self):
        # Only show information if player consented, and it's the last round of the supergame
        return(self.player.information_shown and self.round_number % Constants.rounds_per_supergame == 0)

class WaitForBets(WaitPage):
    wait_for_all_groups = False

    #def after_all_players_arrive(self):
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

class InfoAvoidance1(Page):
    form_model = models.Player
    form_fields = ["infoavoidance1"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance2(Page):
    form_model = models.Player
    form_fields = ["infoavoidance2"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance3(Page):
    form_model = models.Player
    form_fields = ["infoavoidance3"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance4(Page):
    form_model = models.Player
    form_fields = ["infoavoidance4"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance5(Page):
    form_model = models.Player
    form_fields = ["infoavoidance5"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance6(Page):
    form_model = models.Player
    form_fields = ["infoavoidance6"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance7(Page):
    form_model = models.Player
    form_fields = ["infoavoidance7"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance8(Page):
    form_model = models.Player
    form_fields = ["infoavoidance8"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance9(Page):
    form_model = models.Player
    form_fields = ["infoavoidance9"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance10(Page):
    form_model = models.Player
    form_fields = ["infoavoidance10"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance11(Page):
    form_model = models.Player
    form_fields = ["infoavoidance11"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance12(Page):
    form_model = models.Player
    form_fields = ["infoavoidance12"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class InfoAvoidance13(Page):
    form_model = models.Player
    form_fields = ["infoavoidance13"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class RiskPreferences(Page):
    form_model = models.Player
    form_fields = ["riskpreferences1"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class Courses(Page):
    form_model = models.Player
    form_fields = ["econ_exp", "marketing_exp", "law_exp"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class Demographics(Page):
    form_model = models.Player
    form_fields = ["is_male", "english", "age"]
    def is_displayed(self):
        return(self.player.round_number == Constants.num_rounds)

class End(Page):
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
    InformationChoice,
    #WaitForBets,
    Show_Information,
    InfoAvoidance1,
    InfoAvoidance2,
    InfoAvoidance3,
    InfoAvoidance4,
    InfoAvoidance5,
    InfoAvoidance6,
    InfoAvoidance7,
    InfoAvoidance8,
    InfoAvoidance9,
    InfoAvoidance10,
    InfoAvoidance11,
    InfoAvoidance12,
    InfoAvoidance13,
    RiskPreferences,
    Courses,
    Demographics,
    End
]
