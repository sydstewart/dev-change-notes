from ._anvil_designer import RowTemplate6Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...audit_history import audit_history

class RowTemplate6(RowTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.column_panel_1.visible = False
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    changeid = self.item['new_change_note_id']
    when = self.item['when_changed']
    if self.column_panel_1.visible == False:
        self.column_panel_1.visible = True
        self.repeating_panel_1.items = app_tables.change_notes_audit.search(tables.order_by('when_changed', ascending = False),new_change_note_id=changeid, when_changed = when)
    else:
      self.column_panel_1.visible = False
    pass




