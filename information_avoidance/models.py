from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    rounds_per_supergame = 3
    num_supergames = 4
    treatments = ["none", "optional", "mandatory"]

    tokens_per_subgame = int(30/rounds_per_supergame)
    num_rounds = num_supergames * rounds_per_supergame
    name_in_url = 'information_avoidance'
    players_per_group = None

    probsA = [1.0/21 + 0.004*(10-i) for i in range(0, 21)]
    probsB = [1.0/21 for i in range(0, 21)]
    probsC = [1.0/21 + 0.004*(i-10)for i in range(0, 21)]

    multipliers = list(range(0,21))

    values = ["A", "B", "C"]

class Subsession(BaseSubsession):
    initial_round = models.BooleanField(doc = "True iff current round is the first round of a supergame")
    
    def before_session_starts(self):
        self.initial_round = ((self.round_number - 1) % Constants.rounds_per_supergame) == 0

        # Equally distribute treatments among players
        for i in range(len(self.get_players())):
            p = self.get_players()[i]
            p.treatment = Constants.treatments[i % len(Constants.treatments)]






class Group(BaseGroup):
    pass


class Player(BasePlayer):
    treatment = models.CharField(doc = "The treatment assigned to the player")
    information_shown = models.BooleanField(
        initial = True,
        blank = True,
        choices = [[True, "Yes"], [False, "No"]],
        widget = widgets.RadioSelect(),
        doc = "True iff the player opted in to see information")
    outcome = models.BooleanField(doc = "True iff player's investment paid off")
    tokens = models.IntegerField(initial = 0, doc = "Player's current number of tokens")
    investment = models.IntegerField(doc = "How many tokens the player chose to invest")
    earned = models.IntegerField(doc = "The payoff of the investment (gross)")
    earned_total = models.IntegerField(doc = "The total tokens earned in the round")
    chosen_option = models.CharField(
    	initial = None,
    	choices = Constants.values,
    	blank = False,
    	widget = widgets.RadioSelect(),
        doc = "The lottery game chosen by the player in this round")
    
    previous_option = models.CharField(
    	initial = None,
    	choices = Constants.values,
    	blank = False,
    	widget = widgets.RadioSelect(),
        doc = "The lottery game chosen by the player in the previous round")
    
    info_option = models.CharField(initial = None)
    info_investment = models.IntegerField(initial = None)
    info_outcome = models.BooleanField(initial = None)
    info_earned = models.IntegerField(initial = None)