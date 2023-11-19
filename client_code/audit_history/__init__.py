from ._anvil_designer import audit_historyTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..Change_note import Change_note




class audit_history(audit_historyTemplate):
  def __init__(self, new_change_note_id, title, **properties):
  
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.text_box_1.text = new_change_note_id
    # self.project_column_textbox.text = project_column
    # # Any code you write here will run before the form opens.
    # print('Project board of line', project_board, project_column)
    self.repeating_panel_2.items = app_tables.change_notes_audit.search(tables.order_by('when_changed', ascending = False),new_change_note_id=new_change_note_id)
   
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

 