from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
import numpy.random

class Introduction(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1 and self.subsession.show_round)

class PRA(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1 and self.subsession.show_round)

class Instructions1(Page):
    def is_displayed(self):
        return(self.subsession.round_number == 1 and self.subsession.show_round)

class Instructions2(Page):
    def is_displayed(self):
        return((self.subsession.initial_round) and self.subsession.show_round)

class Supergame(Page):
    form_model = models.Player
    form_fields = ["chosen_option", "investment"]

    def is_displayed(self):
        return(self.subsession.show_round)

    def vars_for_template(self):
        try:
            if (self.round_number % self.subsession.subgames != 1):
                previous_choice = self.participant.vars[str(self.round_number - 1)]
            else:
                previous_choice = None
        except KeyError:
            previous_choice = None
        
        part = ((self.round_number - 1) % self.subsession.subgames) + 1

        first_round = ((self.round_number % self.subsession.subgames) == 1)

        #lotteries = zip([round(a*100) for a in Constants.probs1], [round(b * 100) for b in Constants.probs2], Constants.outcome1, Constants.outcome2, Constants.values)
        return{"previous_choice": previous_choice, "part": part, "first_round": first_round}

    def before_next_page(self):
        self.participant.vars[str(self.round_number)] = self.player.chosen_option
        self.participant.vars["investment" + str(self.round_number)] = self.player.investment

        self.player.multiplier = self.subsession.sim_gamble(self.player.chosen_option)

        self.player.earned = round(float(self.player.investment * self.player.multiplier))
        self.player.investment_return = self.player.earned - self.player.investment
        self.player.revenue = self.player.earned + (self.subsession.tokens_per_subgame - self.player.investment)
        self.player.previous_payoff = self.participant.payoff
        self.player.payoff = self.player.revenue
        self.player.not_invested = self.subsession.tokens_per_subgame - self.player.investment



class Outcome(Page):
    def is_displayed(self):
        return(self.subsession.show_round)

    def vars_for_template(self):
        return{"tokens_not_invested": self.subsession.tokens_per_subgame - self.player.investment}


class Information(Page):
    def is_displayed(self):
        # Only give option to see information if it is the last round of the supergame
        return(((self.round_number % self.subsession.subgames == 0) and self.player.treatment != "none") and self.subsession.show_round)

    def vars_for_template(self):
        total_investment = 0
        for i in range((self.round_number - self.subsession.subgames + 1), (self.round_number + 1)):
            print(i)
            total_investment = total_investment + self.participant.vars["investment" + str(i)]

        print(total_investment)
        return{"total_investment": total_investment}

    def before_next_page(self):
        if (self.player.treatment == "mandatory"):
            self.player.info_option = random.choice(["A", "B", "C"])
            self.player.information_shown = True
            self.player.info_investment_return = 0
            self.player.info_earned_total = 0
            self.player.info_total_invested = 0
            self.player.info_not_invested = 0
            self.player.info_revenue = 0
            for i in range(0, self.subsession.subgames):
                self.player.info_multiplier = self.subsession.sim_gamble(self.player.info_option)
                self.player.info_investment = random.randint(1, self.subsession.tokens_per_subgame)
                self.player.info_total_invested += self.player.info_investment
                self.player.info_not_invested += self.subsession.tokens_per_subgame - self.player.info_investment          

                self.player.info_earned = round(self.player.info_investment * self.player.info_multiplier)
                self.player.info_earned_total += self.player.info_earned
                self.player.info_investment_return += self.player.info_earned - self.player.info_investment
                self.player.info_revenue += self.player.info_earned + (self.subsession.tokens_per_subgame - self.player.info_investment)

class InformationChoice(Page):
    form_model = models.Player
    form_fields = ["info_option"]
    def is_displayed(self):
        # Only give option to see information if it is the last round of the supergame
        return(((self.round_number % self.subsession.subgames == 0) and self.player.treatment == "optional") and self.subsession.show_round)

    def before_next_page(self):
        self.player.information_shown = (self.player.info_option != None) and (self.player.info_option != "skip_info")
        if (self.player.info_option != None and self.player.info_option != "skip_info"):
            self.player.info_investment_return = 0
            self.player.info_earned_total = 0
            self.player.info_total_invested = 0
            self.player.info_not_invested = 0
            self.player.info_revenue = 0
            for i in range(0, self.subsession.subgames):
                self.player.info_multiplier = self.subsession.sim_gamble(self.player.info_option)
                self.player.info_investment = random.randint(1, self.subsession.tokens_per_subgame)
                self.player.info_total_invested += self.player.info_investment
                self.player.info_not_invested += self.subsession.tokens_per_subgame - self.player.info_investment          

                self.player.info_earned = round(self.player.info_investment * self.player.info_multiplier)
                self.player.info_earned_total += self.player.info_earned
                self.player.info_investment_return += self.player.info_earned - self.player.info_investment
                self.player.info_revenue += self.player.info_earned + (self.subsession.tokens_per_subgame - self.player.info_investment)


class Show_Information(Page):
    def is_displayed(self):
        # Only show information if player consented, and it's the last round of the supergame
        return((self.player.information_shown and self.round_number % self.subsession.subgames == 0) and self.subsession.show_round)

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
