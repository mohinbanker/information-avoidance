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
    treatments = ["self", "no_self", "other", "no_other"]

    tokens_per_subgame = int(30/rounds_per_supergame)
    num_rounds = num_supergames * rounds_per_supergame
    name_in_url = 'information_avoidance'
    players_per_group = None

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
        initial = None,
        blank = False,
        choices = [[True, "Yes"], [False, "No"]],
        widget = widgets.RadioSelect(),
        doc = "True iff the player opted in to see information")
    outcome = models.BooleanField(doc = "True iff player's investment paid off")
    tokens = models.IntegerField(initial = 0, doc = "Player's current number of tokens")
    investment = models.IntegerField(doc = "How many tokens the player chose to invest")
    earned = models.IntegerField(doc = "The payoff of the investment (gross)")
    chosen_option = models.CharField(
    	initial = None,
    	choices = [["A", "Option A: 4x with 50% probability and 0x with 50% probability"],
    			   ["B", "Option B: 1.5x with 80% probability and 0.5x with 20% probability"]],
    	blank = False,
    	widget = widgets.RadioSelect(),
        doc = "The lottery game chosen by the player in this round")
    
    previous_option = models.CharField(
    	initial = None,
    	choices = [["A", "Option A: 4x with 50% probability and 0x with 50% probability"],
    			   ["B", "Option B: 1.5x with 80% probability and 0.5x with 20% probability"]],
    	blank = False,
    	widget = widgets.RadioSelect(),
        doc = "The lottery game chosen by the player in the previous round")
    