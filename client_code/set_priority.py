import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
# This is a module.


def set_priority(self):
  if self.severity_number.text and  self.probability_number.text and self.visibility_number.text :
        self.rpn_number.text = self.severity_number.text * self.probability_number.text * self.visibility_number.text
        if self.rpn_number.text > 100:
          self.priority_textbox.text = "1. High Priority"
          self.due_date.date = self.date_picker_1.date +timedelta(days=31) 
        elif self.rpn_number.text <= 72 :
          self.priority_textbox.text = "3. Low Priority"
          self.due_date.date = self.date_picker_1.date +timedelta(days=1095) 
        elif self.rpn_number.text > 72 and self.rpn_number.text <= 100:
           self.priority_textbox.text = "2. Medium Priority"
           self.due_date.date= self.date_picker_1.date +timedelta(days=365) 
        elif self.rpn_number.text == 0:
          self.priority_textbox.text ='4. Not Defined'
          self.due_date.date = self.date_picker_1.date  
        self.item['rpn '] = self.rpn_number.text
        self.item['priority']= self.priority_textbox.text
        self.item['due_date'] =self.due_date.date
         
 
    