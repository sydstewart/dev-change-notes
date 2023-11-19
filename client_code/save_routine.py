from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from datetime import datetime, time , date , timedelta

from Validator.validator import Validator



def save_routine(self):
    """This method is called when the button is clicked"""
    if self.validator.are_all_valid():
      
          pick = self.pick_textbox.text
          if not self.text_box_1.text :        
              print('change_id=',self.text_box_1.text)
              year, counter = anvil.server.call('change_id_number')
              print('counter in save button=', counter)
              self.text_box_1.text = str(year) + '-' +str(counter)
              print('new change_id=',self.text_box_1.text)
          else:
              self.text_box_1.text =self.item['change_note_id']
          result = {
              'new_change_note_id' :  self.text_box_1.text,
              'title': self.text_area_1.text,
              'description': self.text_area_2.text,
              'function' : self.function_drop_down.selected_value,
              'product_area': self.product_area_drop_down.selected_value,
              'change_date' : self.date_picker_1.date,
              # 'change_search_date' : self.create_date_textbox.text,
              'stage' :self.stage_drop_down.selected_value,
              'user' :self.user_drop_down.selected_value,
              'type' :self.tyype_drop_down.selected_value,
              'classid' : self.class_drop_down.selected_value,
              'difficulty': self.difficulty_textbox.text,
              'payoff' : self.payoff_textbox.text,
              'ips' : self.difficulty_textbox.text  * self.payoff_textbox.text,
              'pick' : self.pick_textbox.text, # this involves the calculation using 'difficulty' and 'payoff'
              # involves an involved if statement - this wont save to the table
              'due_date' : self.due_date.date,
              'investigator' : self.investigator_dropdown.selected_value,
              'possible_solution' : self.possible_solution_textbox.text,
              'severity' : self.severity_number.text ,
              'probability' : self.probability_number.text,
              'visibility'  : self.visibility_number.text,
              'rpn' : self.severity_number.text * self.probability_number.text * self.visibility_number.text,
              'priority' : self.priority_textbox.text,
              'found_in_last_two_years':self.check_box_1.checked,
              'released_in_version' :self.released_verision_no_dropdown.selected_value,
              'found_in_version_no' : self.found_in_version_dropdown.selected_value
            }
          self.raise_event('x-close-alert', value=result)
    else:
      print(self.validator.are_all_valid())
