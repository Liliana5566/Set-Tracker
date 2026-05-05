import maya.cmds as mc

class MayaUI:  ## Maya UI Class ## 


    def __init__(self): ## setup UI window + variables ##
        self.window = "mySetWindow" 
        self.master_set = "MY_SET_GRP"

       
        self.ensure_master_set()

        if mc.window(self.window, exists=True):
            mc.deleteUI(self.window)

        self.window = mc.window(self.window, title="Set Manager", widthHeight=(300, 200))
        self.layout = mc.columnLayout(adjustableColumn=True) 

        mc.text(label="Selection Set Manager")

        self.set_name_field = mc.textField(placeholderText="Enter Set Name")

        mc.button(label="Create Set", command=self.create_set)
        mc.button(label="Add Selection to Set", command=self.add_to_set)
       

        mc.separator(height=10, style='in')
        mc.text(label="Existing Sets:")

        self.scroll = mc.scrollLayout(height=120)
        self.button_column = mc.columnLayout(parent=self.scroll, adjustableColumn=True)
        mc.showWindow(self.window)

        
        self.refresh_set_buttons()


    def ensure_master_set(self): ## Ensure master set exists ##
        if not mc.objExists(self.master_set):
            self.master_set = mc.sets(name=self.master_set, empty=True)
        return self.master_set 


    def create_set(self, *args): ## Create a new set ##
        name = mc.textField(self.set_name_field, q=True, text=True) 

        if not name: 
            mc.warning("Please enter a set name") 
            return 
        
        if mc.objExists(name):
            mc.warning("set already exists")
            return 

        mc.sets(name=name)  
        mc.warning(f"Set created: {name}") 


        mc.sets(name, add=self.ensure_master_set()) 

        self.refresh_set_buttons() 


    def add_to_set(self, *args):  ## Add selected objects to set ##
        name = mc.textField(self.set_name_field, q=True, text=True) 

        if not mc.objExists(name): 
            mc.warning("Set does not exist") 
            return  

        selection = mc.ls(sl=True)  

        if not selection:
            mc.warning("Select objects first") 
            return 

        mc.sets(selection, add=name)
        mc.warning(f"Added {len(selection)} objects to {name}") 


    def select_set(self, *args):   ## Select set from text input ##
        name = mc.textField(self.set_name_field, q=True, text=True)

        if not mc.objExists(name):
            mc.warning("Set does not exist")
            return

        members = mc.sets(name, q=True) or [] 
        mc.select(members)
        mc.warning(f"Selected contents of {name}") 


    def delete_set(self, set_name): ## Deletes a set ##

        if not mc.objExists(set_name):
            mc.warning("Set does not exist")
            return

        mc.delete(set_name)

        master = self.ensure_master_set()
        if mc.objExists(master):
            members = mc.sets(master, q=True) or []
            if set_name in members:
                mc.sets(set_name, remove=master)

        mc.warning(f"Deleted set: {set_name}")

        self.refresh_set_buttons()


    def refresh_set_buttons(self): ## Remakes UI buttons ##

        children = mc.columnLayout(self.button_column, q=True, ca=True)
        if children:
            for child in children:
                mc.deleteUI(child)

        
        sets = mc.sets(self.ensure_master_set(), q=True)

        if not sets:
            sets = []

        for s in sets:

            if not mc.objExists(s):
                continue

            mc.rowLayout(numberOfColumns=2, adjustableColumn=1, parent=self.button_column)

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


    def select_specific_set(self, set_name): ## Select set from UI button ##

        if not mc.objExists(set_name):
            mc.warning("Set no longer exists")
            return

        members = mc.sets(set_name, q=True) or []
        mc.select(members)
        mc.warning(f"Selected {set_name}")


## Launch ##
def Run():
    mayaUI = MayaUI()

Run()
