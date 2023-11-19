from ._anvil_designer import Change_noteTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from ..pick_calc import set_pick
from Validator.validator import Validator
from ..set_priority import set_priority
from ..set_pick import set_pick
from ..save_routine import save_routine
# from form_checker import validation

class Change_note(Change_noteTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # if not self.date_picker_1.date:
    #     self.date_picker_1.date = datetime.today()

    
    self.validator = Validator()
    self.validator.between(component=self.difficulty_textbox,
                           error_label=self.diff_label,
                           events=['lost_focus', 'change'],
                           min_value=0,
                           max_value=10,
                           include_min=True,
                           include_max=True)
    self.validator.between(component=self.payoff_textbox,
                           error_label=self.pay_label,
                           events=['lost_focus', 'change'],
                           min_value=0,
                           max_value=10,
                           include_min=True,
                           include_max=True)
    self.validator.between(component=self.severity_number,
                        error_label=self.no_severity_label,
                        events=['lost_focus', 'change'],
                        min_value=0,
                        max_value=10,
                        include_min=True,
                        include_max=True)
    self.validator.between(component=self.probability_number,
                        error_label=self.no_probability_label,
                        events=['lost_focus', 'change'],
                        min_value=0,
                        max_value=10,
                        include_min=True,
                        include_max=True)
    self.validator.between(component=self.visibility_number,
                        error_label=self.no_visibility_label,
                        events=['lost_focus', 'change'],
                        min_value=0,
                        max_value=10,
                        include_min=True,
                        include_max=True)
    self.validator.required(component=self.user_drop_down,
                            error_label=self.no_user_label,
                            events=['change'])
    self.validator.required(component=self.date_picker_1,
                            error_label=self.no_date_label,
                            events=['change'])
    self.validator.required(component=self.text_area_1,
                            error_label=self.no_title_label,
                            events=[ 'lost_focus','change'])
                            # format='regex@(\d{3}).*(\d{3}).*(\d{4})@(\1) \2-\3')
    # self.validator.require_dropdown_field(self.user_drop_down, self.no_user_label) 
    self.validator.required(component=self.product_area_drop_down,
                            error_label=self.no_product_area_lbl,
                            events=['change'])
    self.validator.required(component=self.function_drop_down,
                            error_label=self.no_function_lbl,
                            events=['change'])
    self.validator.required(component=self.stage_drop_down,
                            error_label=self.no_stage_lbl,
                            events=['change'])
    self.validator.required(component=self.class_drop_down,
                            error_label=self.no_class_lbl,
                            events=['change'])
    self.validator.required(component=self.tyype_drop_down,
                            error_label=self.no_type_label,
                            events=['change'])
    
    if self.payoff_textbox.text is None or self.payoff_textbox.text == 0:
      self.payoff_textbox.text = 0
      self.ips_textbox.text = 0
      self.pick_textbox.text = "5 Not Defined."
    if self.difficulty_textbox.text is None or self.difficulty_textbox.text == 0:
      self.difficulty_textbox.text = 0
      self.ips_textbox.text = 0
      self.pick_textbox.text = "5 Not Defined."
      
    if self.severity_number.text is None or self.severity_number.text == 0:
      self.severity_number.text = 0
      self.rpn_number.text = 0
      self.priority_textbox.text ='4. Not Defined'
    
    if self.probability_number.text is None or self.probability_number.text == 0:
      self.probability_number.text  = 0
      self.rpn_number.text = 0
      self.priority_textbox.text ='4. Not Defined'
    
    if self.visibility_number.text is None or self.visibility_number.text == 0:
       self.visibility_number.text = 0
       self.rpn_number.text = 0
       self.priority_textbox.text ='4. Not Defined'

    if self.payoff_textbox.text is None or self.payoff_textbox.text == 0:
         self.payoff_textbox.text = 0
         self.ips_textbox.text = 0
    if self.difficulty_textbox.text is None or self.difficulty_textbox.text == 0:
      self.difficulty_textbox.text = 0
      self.ips_textbox.text = 0
    if self.severity_number.text is None or self.severity_number.text == 0:
      self.severity_number.text = 0
      self.rpn_number.text = 0
    if self.probability_number.text is None or self.probability_number.text == 0:
      self.probability_number.text  = 0
      self.rpn_number.text = 0
    if self.visibility_number.text is None or self.visibility_number.text == 0:
       self.visibility_number.text = 0
       self.rpn_number.text = 0
       self.priority_textbox.texxt ='4 No'
    # Any code you write here will run before the form opens.
    if (self.payoff_textbox.text or self.payoff_textbox.text ==0) and \
       (self.difficulty_textbox.text or self.difficulty_textbox.text) ==0:
         self.ips_textbox.text = self.payoff_textbox.text * self.difficulty_textbox.text
         self.item['ips']  =  self.difficulty_textbox.text  * self.payoff_textbox.text
         self.item['pick'] = self.pick_textbox.text
  
    if (self.severity_number.text or self.severity_number.text ==0) and \
        (self.probability_number.text or self.probability_number.text ==0) and \
        (self.visibility_number.text or self.visibility_number.text ==0):
            self.rpn_number.text = self.severity_number.text * self.probability_number.text * self.visibility_number.text
            self.item['priority'] =self.priority_textbox.text
            self.item['rpn'] =0
          
    # Any code you write here will run when the form opens.

#load functions into dropdown    
    functions = app_tables.functions.search(tables.order_by('function'))
    functionlist =[]
    for row in functions:
       functionlist.append(row['function'])
    print(functionlist)
#     functionlist = functionlist.sort()
    self.function_drop_down.items = functionlist 
# Load users into dropdown    
    users = app_tables.users.search(tables.order_by('email'))
    userlist = []
    for row in users:
       userlist.append(row['email'])
    self.user_drop_down.items =userlist
    self.investigator_dropdown.items = userlist
# load found_in_version_no
    version = list({(r['Live_version_no']) for r in app_tables.suppported_products.search(tables.order_by('Live_version_no'))})
    # versionlist = []
    # for row in version:
    #   print (row['Live_version_no'])
    #    # versionlist.append(row['Live_version_no'])
    self.found_in_version_dropdown.items =version
    self.released_verision_no_dropdown.items = version

    
    
    
  def payoff_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if not self.difficulty_textbox.text == 0 and not self.payoff_textbox.text  == 0:
         set_pick(self)
                     
    else:
        self.pick_textbox.text =  "5 Not Defined."
        
        # alert('Difficulty must be between 1 and 10')
   

    


  def add_function_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    #     self.function_multi_select_drop_down.items = list({(r['function']) for r in  app_tables.change_notes.search(tables.order_by('function'))})
    t = TextBox(placeholder="New Function")
    alert(content=t,
          title="Enter a New Function")
    print(f"You entered: {t.text}")
    self.item['function'] = t.text
    app_tables.functions.add_row(function = t.text)
#     self.function_multi_select_drop_down.selected = t.text
#     self.function_multi_select_drop_down.refresh_data_bindings()
    functionlist =[]
    functions = app_tables.functions.search(tables.order_by('function'))
    for row in functions:
       functionlist.append(row['function'])
    print(functionlist)
#     functionlist = functionlist.sort()
    self.function_drop_down.items= functionlist 
    self.function_drop_down.selected_value = t.text



  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    change_copy = dict(list(self.item))
    # Open an alert displaying the 'ArticleEdit' Form
    # set the `self.item` property of the ArticleEdit Form to a copy of the article to be updated
    button_2clicked = alert(
      content=Change_note(item=change_copy),
      title="Update Change",
      large=True,
      buttons=[("Save", True), ("Cancel", False),"self.button_2", True]
    )
    # Update the arti
    if button_2_clicked:
       anvil.server.call('update_change', self.item, change_copy)

      # Now refresh the page
       self.refresh_data_bindings()
    pass
   
    
# Stage history
  def button_3_click(self,  **event_args):
    """This method is called when the button is clicked"""
    self.stage_drop_down.selected_value= "Under Investigation"
    t = app_tables.change_notes.get(change_note_id=self.text_box_1.text)
    print(t['change_note_id'])
    change_note_id = t['change_note_id']
    self.item['stage'] = "Under Investigation"
    print(self.item['stage'])
    app_tables.stage_log.add_row(change_note_id = change_note_id,changed_from = last_stage, Stage_change_date= datetime.now(), changed_to = self.item['stage']   )
    
   

  def save_button_click(self,  **event_args):
    """This method is called when the button is clicked"""
    save_routine(self)


  def difficulty_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if not self.difficulty_textbox.text == 0 and not self.payoff_textbox.text == 0:
         set_pick(self)
                     
    else:
        self.pick_textbox.text =  "5 Not Defined."
        
        # alert('Difficulty must be between 1 and 10')
    
  pass

  def ips_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if  self.difficulty_textbox.text >= 5 and self.payoff_textbox.text > 5:
       self.pick_textbox.text = "1. Implement"
    elif  self.difficulty_textbox.text <  5 and self.difficulty_textbox.text >= 1 and self.payoff_textbox.text >= 5:
       self.pick_textbox.text = "2. Challenge"
    elif self.difficulty_textbox.text >=5 and self.payoff_textbox.text  < 5 and self.payoff_textbox.text  >= 1:
      self.pick_textbox.text ="3. Possible"
    elif self.difficulty_textbox.text <  5 and self.difficulty_textbox.text >= 1  and  self.payoff_textbox.text < 5 and self.payoff_textbox.text >= 1:
      self.pick_textbox.text = "4. Kill"
    elif self.difficulty_textbox.text is None or self.payoff_textbox.text is None:
      self.pick_textbox.text =  "5 Not Defined."
#     self.refresh_data_bindings()
    pass


  def severity_number_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if not self.date_picker_1.date:   
        alert(' Please enter a Change Note Create Date before calculating the RPN so that a Due Date can be calculated, depending on the priority set.')
    else: 
        set_priority(self)


  def probability_number_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if not self.date_picker_1.date:   
        alert(' Please enter a Change Note Create Date before calculating the RPN so that a Due Date can be calculated, depending on the priority set.')
    else: 
        set_priority(self)

     
  def visibility_number_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if not self.date_picker_1.date:   
        alert(' Please enter a Change Note Create Date before calculating the RPN so that a Due Date can be calculated, depending on the priority set.')
    else: 
        set_priority(self)

     


  def change_cancel_btn_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('x-close-alert', value=None)
    pass

  def priority_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if self.priority_textbox.text == 'Medium Priority':
       self.due_date.date = self.date_picker_1.date +timedelta(days=365) 
    elif self.priority_textbox.text == 'High Priority':
       print('High')
       self.due_date.date = self.date_picker_1.date + timedelta(days=31) 
    elif self.priority_textbox.text == 'Low Priority':
       self.due_date.date = self.date_picker_1.date + timedelta(days=1825)
    else:
       self.due_date.date = self.date_picker_1.date 

  def bottom_cancel_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event('x-close-alert', value=None)
    pass

  def bottom_save_btn_click(self, **event_args):
    """This method is called when the button is clicked"""#
    save_routine(self)
    pass

  def difficulty_textbox_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def IPS_textbox_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass








    
























