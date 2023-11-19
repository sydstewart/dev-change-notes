import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

def set_pick(self):
  if  self.difficulty_textbox.text >= 5 and self.payoff_textbox.text > 5:
    self.pick_textbox.text = "1. Implement"
  elif  self.difficulty_textbox.text <  5 and self.difficulty_textbox.text >= 1 and self.payoff_textbox.text >= 5:
    self.pick_textbox.text = "2. Challenge"
  elif self.difficulty_textbox.text >=5 and self.payoff_textbox.text  < 5 and self.payoff_textbox.text  >= 1:
    self.pick_textbox.text ="3. Possible"
  elif self.difficulty_textbox.text <  5 and self.difficulty_textbox.text >= 1  and  self.payoff_textbox.text < 5 and self.payoff_textbox.text >= 1:
    self.pick_textbox.text = "4. Kill"
  elif self.difficulty_textbox.text is None or self.payoff_textbox.text is None:
    self.pick_textbox.text =  "5 Not Defined."
  return  self.pick_textbox.text