from ._anvil_designer import ListsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.tz
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from ..selection import selection
from ..Change_note import Change_note
from ..Searches.using_kwargs import search_using_kwargs
from ..fix_due_date import fix_due_date

class Lists(ListsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Login
    anvil.users.login_with_form()
    global loggedinuser
    loggedinuser =  anvil.users.get_user()['email']
#     self.loggedinuser.text = loggedinuser
    print('User=',loggedinuser)
    
    user_type = anvil.users.get_user()['user_type']
    
    result = anvil.server.call('get_datetime')
    self.repeating_panel_1.items = app_tables.change_notes.search(tables.order_by('change_date', ascending = False))
    
    # self.repeating_panel_1.items = app_tables.change_notes.search()
    self.hits_textbox.text = len(app_tables.change_notes.search())
    # functions= list({(r['function']) for r in app_tables.suppported_products.search()})

#Search Dropdowns =============================================================
    functions = app_tables.functions.search(tables.order_by('function'))
    functionlist =[]
    for row in functions:
       functionlist.append(row['function'])
    self.search_function_drop_down.items = functionlist
   
    users = app_tables.users.search(tables.order_by('email'))
    userlist =[]
    for row in users:
      userlist.append(row['email'])
    self.search_creator_dropdown.items = userlist
    self.search_investigator_dropdown.items = userlist
# priority
    priority =list({(r['priority']) for r in app_tables.change_notes.search(tables.order_by('priority'))})
    self.priority_search_dropdown.items = priority 
# Searches =======================================================================
#stage change     
    def stage_search_dropdown_change(self, **event_args): 
      """This method is called when an item is selected"""
      search_using_kwargs(self)
#Type
    
    def search_type_drop_down_change(self, **event_args):
      search_using_kwargs(self)

#Class
    def search_class_drop_down_change(self, **event_args):
      search_using_kwargs(self)

       
      
# Loading data from Excel ==========================================================

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Load_CSV')
    pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Lists')
    pass
  


  def stage_multi_select_drop_down_change(self, **event_args):
    """This method is called when the selected values change"""
    selectedstage = self.multi_select_drop_down_1.selected
    selection(self)


  def multi_select_drop_down_3_change(self, **event_args):
    """This method is called when the selected values change"""
    pass

  def classs_multi_select_drop_down_change(self, **event_args):
    """This method is called when the selected values change"""
    selectedclassid = self.classid_multi_select_drop_down.selected
    selection(self)
    pass



  def add_change_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Initialise an empty dictionary to store the user inputs
    content = Change_note()
    result = alert(content, buttons=[], title = 'New Change Note', large=True)
    print(result)
    if result:
        print('User=', loggedinuser)
        # change_note_id = (result['product_area'] ) #+ ' ' + result['user']  ) # + str( result['change_date']) + ' '
        app_tables.change_notes.add_row(**result)
        print('changes- updated')
        print('User=', loggedinuser)
        result['user_changed'] = loggedinuser
        result['when_changed'] = datetime.now()
        app_tables.change_notes_audit.add_row(**result)
        print('audit updated')
        
  def refresh_changes(self):

    self.repeating_panel_1.items = app_tables.change_notes.search()
    self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: x['change_date'], reverse=True )
    self.hits_textbox.text = len(app_tables.change_notes.search())

  def stage_search_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def search_type_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def search_class_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def search_function_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def search_product_area_drop_down_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def find_dups_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.task = anvil.server.call('find_dups_back')


  def delete_change(self, change_note, **event_args):
    # Delete the article
    anvil.server.call('delete_change', change_note)


  def refresh_change_notes(self, **event_args):
    self.stage_search_dropdown.selected_value = None
    self.search_type_drop_down.selected_value = None
    self.search_class_drop_down.selected_value = None
    self.text_search_textbox.text = None
    self.search_product_area_drop_down.selected_value = None
    self.search_function_drop_down.selected_value = None

    
    #Initial Search             
    results = app_tables.change_notes.search()

    self.repeating_panel_1.items = results
    #Hits
    self.hits_textbox.text = len(results)
    pass

  def clear_search_criteria_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #Set all fileds to None    
    self.stage_search_dropdown.selected_value = None
    self.search_type_drop_down.selected_value = None
    self.search_class_drop_down.selected_value = None
    self.id_search_textbox.text = None
    self.search_product_area_drop_down.selected_value = None
    self.search_function_drop_down.selected_value = None
    self.date_search_dropdown.selected_value =  None
    self.start_date_picker.date = None
    self.end_date_picker.date =None
    self.search_creator_dropdown.selected_value = None
    self.search_investigator_dropdown.selected_value = None
    self.priority_search_dropdown.selected_value = None
    # self.no_change_date_chkbox.checkbox = False
    #Initial Search             
    results = app_tables.change_notes.search(tables.order_by('change_date', ascending = False))

    self.repeating_panel_1.items = results
    #Hits
    self.hits_textbox.text = len(results)
    pass

  def date_search_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    self.start_date_picker.date = None
    self.end_date_picker.date =None
    search_using_kwargs(self)

  def submitted_in_last_90_days_tmn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.stage_search_dropdown.selected_value = 'Submitted'
    self.date_search_dropdown.selected_value = 'Last 90 Days'
    self.stage_search_dropdown.selected_value != 'Released'
    search_using_kwargs(self)
    pass

    
#SORTS==================================================================================================
  def ips_check_box_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.ips_check_box.checked == True:
              self.priority_sort_checkbox.checked = False
              self.RPN_sort_checkbox.checked = False
              self.pick_sort_chkbox.checked = False
              self.change_note_date_search_chkbox.checked = False
              self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['ips']), reverse=True )
        else:
              self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['ips']), reverse=False )
  
  def pick_sort_chkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.pick_sort_chkbox.checked == True:
          self.priority_sort_checkbox.checked = False
          self.RPN_sort_checkbox.checked = False
          self.ips_check_box.checked = False
          self.change_note_date_search_chkbox.checked == False
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['pick']  ), reverse=False )
    else:
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['pick']), reverse= True )

  def RPN_sort_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.RPN_sort_checkbox.checked == True:
          self.ips_check_box.checked = False
          self.pick_sort_chkbox.checked = False
          self.priority_sort_checkbox.checked = False
          self.change_note_date_search_chkbox.checked == False
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['rpn']  ), reverse=True )
    else:
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['rpn']), reverse=False )

  def priority_sort_checkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.priority_sort_checkbox.checked == True:
          self.ips_check_box.checked = False
          self.pick_sort_chkbox.checked = False
          self.RPN_sort_checkbox.checked = False
          self.change_note_date_search_chkbox.checked == False
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['priority']), reverse=False )
    else:
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['priority']), reverse=True )
    pass

  def change_note_date_search_chkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.change_note_date_search_chkbox.checked == True:
          self.ips_check_box.checked = False
          self.pick_sort_chkbox.checked = False
          self.RPN_sort_checkbox.checked = False
          self.priority_sort_checkbox.checked == False
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['change_date']), reverse=False )
    else:
          self.repeating_panel_1.items = sorted([r for r in self.repeating_panel_1.items], key = lambda x: (x['change_date']), reverse=True )

  def  id_search_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    search_using_kwargs(self)
    pass

  def search_title_and_description_click(self, **event_args):
    """This method is called when the button is clicked"""
    t = TextBox(placeholder="Enter Search text")
    alert(content=t,
      title="Text Search  ")
 
    results = anvil.server.call('text_search_changes', t.text)
    self.repeating_panel_1.items = results
    self.hits_textbox.text  = len(results)

    pass


  def start_date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.date_search_dropdown.selected_value = None
    search_using_kwargs(self)
    pass

  def end_date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    self.date_search_dropdown.selected_value = None
    search_using_kwargs(self)
    pass

  def search_creator_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass
    
  def search_investigator_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def no_change_date_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    search_using_kwargs(self)
    pass

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    fix_due_date()
    pass

  def populate_blank_fields_click(self, **event_args):
    """This method is called when the button is clicked"""
    t = app_tables.change_notes.search()
    count = 0
    count1 = 0
    for row in t:
      if row['priority'] == None:
        row['priority'] = '4. Not Defined'
        count =count +1
        print('count=',count)
    alert(' Priority changed to 4. Not Defined=', count)
    if row['priority'] == 'High Priority':
          t['priority'] = '1. High Priority'
          count1 =count1 +1
    alert(' Priority changed to 1. High Priority=', count1)
    pass

  def add_functions_click(self, **event_args):
    """This method is called when the button is clicked"""
    app_tables.functions.delete_all_rows()
    functions = list({(r['function']) for r in  app_tables.change_notes.search(tables.order_by('function'))})

    for i in functions:
       print(i)
       functionexist = app_tables.functions.get(function = i)
       if not functionexist:
         app_tables.functions.add_row(function = i)
    pass

  def over_due_chkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    search_using_kwargs(self)
    pass

  def priority_search_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    search_using_kwargs(self)
    pass

  def restore_table_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Load_CSV')
    pass

  def log_out_click(self, **event_args):
    """This method is called when the button is clicked"""
    # self.content_panel_1.clear()
    self.column_panel_1.clear()
    
    anvil.users.logout()
    
    anvil.users.login_with_form()
    open_form('Lists')
    pass

  def due_date_sort_chkbox_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    if self.due_date_sort_chkbox.checked == True:
          self.ips_check_box.checked = False
          self.pick_sort_chkbox.checked = False
          self.priority_sort_checkbox.checked = False
          self.RPN_sort_checkbox.checked = False
          self.change_note_date_search_chkbox.checked == False
          self.repeating_panel_1.items = app_tables.change_notes.search(tables.order_by('due_date', ascending = False), \
                                                                        type ='Safety', classid = 'Defect'   \
                                                                       , stage = q.none_of('Released', 'Reviewed', 'Rejected'))
    else:     
                                                                                           
          self.repeating_panel_1.items = app_tables.change_notes.search(tables.order_by('due_date', ascending = True), \
                                                                        type ='Safety', classid = 'Defect', \
                                                                        stage = q.none_of('Released', 'Reviewed', 'Rejected'))
    
    
    
  
    
    pass




























   


 

























