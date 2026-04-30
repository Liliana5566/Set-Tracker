import maya.cmds as mc

class MayaUI:
    def __init__(self): #run automatically
        self.window = "mySetWindow" #stores a uqique name for the window so maya can track it


        self.master_set = "MY_SET_GRP"#

        # ensure master exists on startup
        self.ensure_master_set()#

        if mc.window(self.window, exists=True):#
            mc.deleteUI(self.window)#

        self.window = mc.window(self.window, title="Set Manager", widthHeight=(300, 200)) #this makes a new window with a set size and the name set mmanager

        self.layout = mc.columnLayout(adjustableColumn=True) #makes a vertical layout so they are stacked

        mc.text(label="Selection Set Manager") #adds a static label at the top of the UI

        self.set_name_field = mc.textField(placeholderText="Enter Set Name") #makes a text box where a user types the set name

        mc.button(label="Create Set", command=self.create_set) #adds a bnt that runs the fucnction "create set"
        mc.button(label="Add Selection to Set", command=self.add_to_set) #adds a bnt that runs the fuction "add to set"
       

        mc.separator(height=10, style='in')#
        mc.text(label="Existing Sets:")#

        self.scroll = mc.scrollLayout(height=120)#
        self.button_column = mc.columnLayout(parent=self.scroll, adjustableColumn=True)#

        mc.showWindow(self.window)#

        # build UI from Maya scene (NOT python memory)
        self.refresh_set_buttons()#


    def ensure_master_set(self):#
        # This prevents "No object matches name: MY_UI_SETS"
        if not mc.objExists(self.master_set):#
            self.master_set = mc.sets(name=self.master_set, empty=True)
        return self.master_set#


    def create_set(self, *args): # defines a fuction that creates a new selection set when called
        name = mc.textField(self.set_name_field, q=True, text=True) # this gets the text the user typed in the input field

        if not name: #checks if the user left the text box empty 
            mc.warning("Please enter a set name") # This is the warring text you get if you forget to type a name
            return #stops the fuction early if no name is given
        
        if mc.objExists(name):#
            mc.warning("set already exists")#
            return#

        mc.sets(name=name) #creates a new maya set with the given name 
        mc.warning(f"Set created: {name}") #prints a confirmation message


        mc.sets(name, add=self.ensure_master_set())#

        self.refresh_set_buttons()#


    def add_to_set(self, *args): # defines a fuction that adds selected objects to a set 
        name = mc.textField(self.set_name_field, q=True, text=True) #gets the given name from the ui

        if not mc.objExists(name): #checks if the set axtually exists in the scene
            mc.warning("Set does not exist") #warns the user if the set is missing
            return #stops the fuction early if the set dosent exist 

        selection = mc.ls(sl=True) #gets the current selection in maya 

        if not selection: #checks if nothing is selected
            mc.warning("Select objects first") #warns the user if selection is empty
            return #stops the fuction if nothing is selected 

        mc.sets(selection, add=name) #adds selected objects into the name set
        mc.warning(f"Added {len(selection)} objects to {name}") # confrims how many objects were added


    def select_set(self, *args): #defines a fuction that selects everything inside a set 
        name = mc.textField(self.set_name_field, q=True, text=True) # Gets the set name from the ui input 

        if not mc.objExists(name): #checks if the set exists
            mc.warning("Set does not exist") # warrning text if it dose not exist
            return #stops execution if invalid

        members = mc.sets(name, q=True) or []#
        mc.select(members)#
        mc.warning(f"Selected contents of {name}") #confirms selections


    def delete_set(self, set_name):#

        if not mc.objExists(set_name):#
            mc.warning("Set does not exist")#
            return#

        mc.delete(set_name)#

        # SAFE cleanup from master set
        master = self.ensure_master_set()#
        if mc.objExists(master):#
            members = mc.sets(master, q=True) or []#
            if set_name in members:#
                mc.sets(set_name, remove=master)#

        mc.warning(f"Deleted set: {set_name}")#

        self.refresh_set_buttons()#


    def refresh_set_buttons(self):#

        children = mc.columnLayout(self.button_column, q=True, ca=True)#
        if children:#
            for child in children:#
                mc.deleteUI(child)#

        # SAFE query using ensure_master_set
        sets = mc.sets(self.ensure_master_set(), q=True)#

        if not sets:#
            sets = []#

        for s in sets:#

            if not mc.objExists(s):#
                continue#

            mc.rowLayout(numberOfColumns=2, adjustableColumn=1, parent=self.button_column)#

            mc.button(
                label=s,
                command=lambda x, name=s: self.select_specific_set(name)
            )

            mc.button(
                label="X",
                width=30,
                command=lambda x, name=s: self.delete_set(name)
            )

            mc.setParent('..')


    def select_specific_set(self, set_name):

        if not mc.objExists(set_name):
            mc.warning("Set no longer exists")
            return

        members = mc.sets(set_name, q=True) or []
        mc.select(members)
        mc.warning(f"Selected {set_name}")


# RUN UI
def Run(): #defines which fuction and then launches the ui
    mayaUI = MayaUI() #makes an instance of ui class

Run() # calls the fuction to start everything