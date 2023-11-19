from ._anvil_designer import LocalTZLabelTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class LocalTZLabel(LocalTZLabelTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def form_refreshing_data_bindings(self, **event_args):
    if self.item:
      self._date = self.item.astimezone(anvil.tz.tzlocal())
      self.label_1.text = self._date.strftime(self._format)
    else:
      self._date = self.item
      self.label_1.text = self.none_text
    
  @property
  def format(self):
    return self._format
  
  @format.setter
  def format(self, format):
    self._format = format
    self.refresh_data_bindings()
  