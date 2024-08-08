import pymel.core as pm 
input = pm.promptBox('Create Category','Category','OK','Cancel') 
if input: 
    nodes = pm.ls(sl=True)
    for node in nodes:
        node.addAttr(shortName='category',longname='Category',dataType='string',defaultValue=input)