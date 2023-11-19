import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


def set_pick(self):

      if not self.difficulty_textbox.text ==0 and not self.payoff_textbox.text ==0:
          # if (self.difficulty_textbox.text) <= 10: #or int(self.difficulty_textbox.text) >= 1:
                      self.ips_textbox.text= self.difficulty_textbox.text * self.payoff_textbox.text
                      if  self.difficulty_textbox.text >= 5 and self.payoff_textbox.text >= 5:
                          self.pick_textbox.text = "1. Implement"
                      elif  self.difficulty_textbox.text <  5 and self.difficulty_textbox.text >= 1 and self.payoff_textbox.text >= 5:
                        self.pick_textbox.text = "2. Challenge"
                      elif self.difficulty_textbox.text >=5 and self.payoff_textbox.text  < 5 and self.payoff_textbox.text  >= 1:
                        self.pick_textbox.text ="3. Possible"
                      elif self.difficulty_textbox.text <  5 and self.difficulty_textbox.text >= 1  and  self.payoff_textbox.text < 5 and self.payoff_textbox.text >= 1:
                        self.pick_textbox.text = "4. Kill"
                      elif self.difficulty_textbox.text is None or self.payoff_textbox.text is None:  self.pick_textbox.text =  "5 Not Defined."
                      self.item['ips'] = self.difficulty_textbox.text * self.payoff_textbox.text 
                      self.item['pick'] = self.pick_textbox.text 
          # else:
          #     alert('Payoff must be betyween 1 and 10')