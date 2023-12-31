from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.repeating_panel_1.items = app_tables.change_notes_audit.search(tables.order_by('when_changed', ascending = False),new_change_note_id=new_change_note_id)
    # Any code you write here will run before the form opens.