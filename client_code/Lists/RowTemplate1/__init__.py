from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...Change_note import Change_note
from datetime import datetime, time , date , timedelta
from ...audit_history import audit_history
from .. import Lists


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
      
    today = date.today()
    print (today)
    if self.type_textbox.text =='Safety':
        self.type_textbox.foreground = '#f56b6b'
        self.type_textbox.bold = True
    if self.text_box_1.text =='1. High Priority':
          self.text_box_1.foreground = '#f56b6b'
    elif  self.text_box_1.text == '2. Medium Priority':
          self.text_box_1.foreground = 'theme:Secondary 500'
    if self.due_date_picker.date:
          print((self.due_date_picker.date.date()))
          if self.due_date_picker.date.date() < (today): 
              self.due_date_picker.foreground = '#f56b6b'
              self.due_date_picker.bold = True
    # if self.item['pick']:
    #       self.pick_textbox.bold =True
    # Any code you write here will run before the form opens.
# EDIT
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    change_copy = dict(list(self.item))

    if change_copy['difficulty'] and change_copy['payoff']:
        self.item['ips'] = change_copy['difficulty']*change_copy['payoff']
    if change_copy['severity'] and  change_copy['probability'] and change_copy['visibility']:
        self.item['rpn']  =change_copy['severity'] * change_copy['probability'] * change_copy['visibility']
        self.item['priority'] =change_copy['priority']
    self.refresh_data_bindings() 
    result = alert(content=Change_note(item=change_copy), title="Update Change Note", buttons=[], large=True)
    
    if result:
        loggedinuser = anvil.users.get_user()['email']
        anvil.server.call('update_change',self.item,change_copy, loggedinuser )

        self.refresh_data_bindings()   
        alert("Record Updated")
    else:
         alert(" Edit Cancelled")
#     save_clicked = alert(buttons=[("Save", True), ("Cancel", False)],
#       content=Change_note(item=change_copy),
#       title="Update Change",
#       large=True
# #       buttons=[("Save", True), ("Cancel", False)]
#     )
#     print('pick in form=',change_copy['pick'])
#     # Update the article if the user clicks save
#     if save_clicked:
#       anvil.server.call('update_change',self.item, change_copy)
#       print('change_copy=',change_copy)
#       # Now refresh the page
#     self.refresh_data_bindings()
#     pass
#   def edit_button_click(self, **event_args):
#     change_copy = dict(list(self.item))
#     change_copy['pick'] =self.item['pick']
#     change_copy['priority'] =self.item['priority']
#     # Open an alert displaying the 'ArticleEdit' Form
#     # set the `self.item` property of the ArticleEdit Form to a copy of the article to be updated
#     save_clicked = alert(buttons=[("Save", True), ("Cancel", False)],
#       content=Change_note_New(item=change_copy),
#       title="Update Change",
#       large=True
# #       buttons=[("Save", True), ("Cancel", False)]
#     )
#        # print('pick in form=',change_copy['pick'.])
#     # Update the article if the user clicks save
#     if save_clicked:
#       anvil.server.call('update_change',self.item, change_copy)
#       print('change_copy=',change_copy)
#       # Now refresh the page
#     self.refresh_data_bindings()
#     """This method is called when the button is clicked"""
    
#     pass

    
# stage history
  
    

  def delete_change_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('audit_history')
    # if confirm("Are you sure you want to archive {}?".format(self.item['title'])):
    #   anvil.server.call('delete_change_note', self.item)
    #   # self.item['stage'] = 'Archive'
     # self.parent.raise_event('x-refresh-change_notes')
      
      
      
    pass

  # def text_box_2_pressed_enter(self, **event_args):
  #   """This method is called when the user presses Enter in this text box"""
  #   pass

  def audit_history_button_click(self, **event_args):
     result = alert(content=audit_history(self.item['new_change_note_id'], self.item['title']), title="Audit", buttons=[("Cancel", False)], large=True)

  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    if confirm("Are you sure you want to archive {}?".format(self.item['title'])):
      anvil.server.call('delete_change_note', self.item)
    pass















