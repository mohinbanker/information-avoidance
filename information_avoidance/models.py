from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Mohin Banker'

doc = """
This is an oTree implementation of a lab experiment investigating financial impacts of information avoidance.
"""


class Constants(BaseConstants):
    rounds_per_supergame = 1
    num_supergames = 1
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
        initial = None,
        blank = True,
        choices = [[True, "Yes"], [False, "No"]],
        widget = widgets.RadioSelect(),
        doc = "True iff the player opted in to see information")

    investment = models.IntegerField(doc = "How many tokens the player chose to invest")
    not_invested = models.IntegerField(doc = "Number of tokens not invested")
    investment_return = models.IntegerField(doc = "Net profit from player's investment")
    earned = models.IntegerField(doc = "The payoff of the investment (gross)")
    earned_total = models.IntegerField(doc = "The total tokens earned in the round")
    previous_payoff = models.IntegerField(doc = "Total tokens earned before the current round")
    multiplier = models.FloatField(doc = "Multiplier used for investment outcome")
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
    
    info_option = models.CharField(initial = None, doc = "Gamble that player chose to view information for")
    info_investment = models.IntegerField(initial = None, doc = "Amount invested in information scenario")
    info_not_invested = models.IntegerField(doc = "Number of tokens not invested")
    info_investment_return = models.IntegerField(initial = None, doc = "Net profit from information investment")
    info_earned = models.IntegerField(initial = None, doc = "Sum of investment and investment return")
    info_earned_total = models.IntegerField(initial = None, doc = "Total tokens earned in this round (including tokens not invested)")
    info_multiplier = models.FloatField(doc = "Multiplier used for investment in information scenario")

    infoavoidance1 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "As part of a semi-annual medical checkup, your doctor asks you a series of questions. The answers to these questions can be used to estimate your life expectancy (the age you are predicted to live to). Do you want to know how long you can expect to live?",
        widget = widgets.RadioSelect())
    infoavoidance2 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "You provide some genetic material to a testing service to learn more about your ancestors. You are then told that the same test can, at no additional cost, tell you whether you have an elevated risk of developing Alzheimer's. Do you want to know whether you have a high risk of developing Alzheimer's?",
        widget = widgets.RadioSelect())
    infoavoidance3 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "At your annual checkup, you are given the option to see the results of a diagnostic test which can identify, among other things, the extent to which your body has suffered long-term effects from stress. Do you want to know how much lasting damage your body has suffered from stress?",
        widget = widgets.RadioSelect())
    infoavoidance4 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "Ten years ago, you had the opportunity to invest in two retirement funds: Fund A and Fund B. For the past 10 years, you have invested all your retirement savings in Fund A. Do you want to know the balance you would have, if you had invested in Fund B instead?",
        widget = widgets.RadioSelect())
    infoavoidance5 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "You decide to go to the theater for your birthday and give your close friend (or partner) your credit card so they can purchase tickets for the two of you, which they do. You aren't sure, but suspect that the tickets may have been expensive. Do you want to know how much the tickets cost?",
        widget = widgets.RadioSelect())
    infoavoidance6 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "You bought an electronic appliance at a store at what seemed like a reasonable, though not particularly low, price. A month has passed, and the item is no longer returnable. You see the same appliance displayed in another store with a sign announcing 'SALE.' Do you want to know the price you could have bought it for?",
        widget = widgets.RadioSelect())
    infoavoidance7 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "You gave a close friend one of your favorite books for her birthday. Visiting her apartment a couple of months later, you notice the book on her shelf. She never said anything about it; do you want to know if she liked the book?",
        widget = widgets.RadioSelect())
    infoavoidance8 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "Someone has described you as quirky, which could be interpreted in a positive or negative sense. Do you want to know which interpretation he intended?",
        widget = widgets.RadioSelect())
    infoavoidance9 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "You gave a toast at your best friend’s wedding. Your best friend says you did a good job, but you aren’t sure if he or she meant it. Later, you overhear people discussing the toasts. Do you want to know what people really thought of your toast?",
        widget = widgets.RadioSelect())
    infoavoidance10 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "As part of a fund-raising event, you agree to post a picture of yourself and have people guess your age (the closer they get, the more they win). At the end of the event, you have the option to see people's guesses. Do you want to learn how old people guessed that you are?",
        widget = widgets.RadioSelect())
    infoavoidance11 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "You have just participated in a psychological study in which all the participants rate one-anothers' attractiveness. The experimenter gives you an option to see the results for how people rated you. Do you want to know how attractive other people think you are?",
        widget = widgets.RadioSelect())
    infoavoidance12 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[1,"Definitely don't want to know"], [2, "Probably don't want to know"], [3, "Probably want to know"], [4, "Definitely want to know"]],
        verbose_name = "Some people seek out information even when it might be painful. Others avoid getting information that they suspect might be painful, even if it could be useful. How would you describe yourself?",
        widget = widgets.RadioSelect())
    infoavoidance13 = models.PositiveIntegerField(
        initial = None,
        blank = True,
        choices = [[4,"Strongly disagree"], [3, "Somewhat disagree"], [2, "Somewhat agree"], [4, "Strongly agree"]],
        verbose_name = "If people know bad things about my life that I don't know, I would prefer not to be told",
        widget = widgets.RadioSelect())