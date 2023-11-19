import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
# from .Lists import Lists
# This is a module.
# You can define variables and functions here, and use them from any form. For example, in a top-level form:
#
#    from . import Module1
#
#    Module1.say_hello()
#

def selection(self, **event_args):
    selectedlist = self.multi_select_drop_down_1.selected
    selectedstage = self.stage_multi_select_drop_down.selected
    selectedclass = self.classid_multi_select_drop_down.selected
#     print (selectedlist)
#     print(selectedstage)
    
    if selectedlist and not selectedstage :
      print('Type')
      self.repeating_panel_1.items = app_tables.change_notes.search(type=q.any_of(*selectedlist))
      self.text_box_2.text=len(app_tables.change_notes.search(type=q.any_of(*selectedlist)))
      
    elif  selectedlist and selectedstage and not selectedclass: 
          print('Both')
          print (selectedlist)
          print(selectedstage)
          self.repeating_panel_1.items = app_tables.change_notes.search(q.all_of( 
                                                                                stage = q.any_of(*selectedstage),
                                                                                type = q.any_of(*selectedlist)
                                                                              #  classid = q.any_of(*selectedclass)
                                                                                 ))
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: x['change_date'], reverse=True )
#
          self.text_box_2.text=len(app_tables.change_notes.search(q.all_of(
                                                                        stage = q.any_of(*selectedstage),
                                                                        type   =q.any_of(*selectedlist)
                                                                    )))
    elif  selectedlist and selectedstage and selectedclass: 
          print('three')
          print (selectedlist)
          print(selectedstage)
          print(selectedclass)
          self.repeating_panel_1.items = app_tables.change_notes.search(q.all_of( 
                                                                                stage = q.any_of(*selectedstage),
                                                                                type = q.any_of(*selectedlist), 
                                                                               classid = q.any_of(*selectedclass)
                                                                                 ))
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: x['change_date'], reverse=True )
#
          self.text_box_2.text=len(app_tables.change_notes.search(q.all_of(
                                                                        stage = q.any_of(*selectedstage),
                                                                        type   =q.any_of(*selectedlist),
                                                                        classid = q.any_of(*selectedclass)
                                                                      )))                                                                
   
    elif  selectedstage and not  selectedlist :
          print('Stage')
          self.repeating_panel_1.items = app_tables.change_notes.search(stage = q.any_of(*selectedstage))
    #     self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: x['change_date'], reverse=True )
    #     self.text_box_2.text = len(app_tables.change_notes.search(stage = self.search_stage_dropdown.selected_value))
          self.text_box_2.text=len(app_tables.change_notes.search(stage = q.any_of(*selectedstage)))
    
    else:
      
      self.repeating_panel_1.items = app_tables.change_notes.search()
  