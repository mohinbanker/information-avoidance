from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    pass

class PRA(Page):
    pass

class Instructions(Page):
    pass

class Instructions2(Page):
    pass


page_sequence = [
    Introduction,
    PRA,
    Instructions,
    Instructions2
]
