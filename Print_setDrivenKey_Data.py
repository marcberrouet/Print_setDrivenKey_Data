"""
@author Marc H Berrouet 2022 - marc.berrouet@gmail.com

Description: Prints out any unknown set driven keys data in any random scene.

Example usage:
 Make sure that your scene has set driven key data in it, then run the script in the script editor to get the results.

"""

import maya.mel as mm
import maya.cmds as mc

def cmdPrint(nameFilter = '*', UI = True):
    
    '''
    Procedures that prints out the python command
    for creating the setDrivenKey present in the scene
    '''			    

    # get all the SETDRIVENKEY animCrvs (animCurveUL)

    command = ''## SET DRIVEN KEYS \n'    
    keys = mc.ls (nameFilter, typ = 'animCurve')
    for animCrv in keys:
        skip = 0
        #print 'SET DRIVEN KEY CURVE --> '+animCrv +'\n'    
        
        # get the DRIVER and check if it is a Set Driven Key (input connection is not None)
        connection = mc.listConnections(animCrv+'.input', scn = 1, p = 1)
        if connection == None: skip = 1
        
        if skip == 0:
            driverObj = connection[0].split('.')[0]
            driverAttr = connection[0].split('.')[1]
            
            # get the DRIVEN
            connection = mc.listConnections(animCrv+'.output', scn = 1, p = 1)
            drivenObj = connection[0].split('.')[0]
            drivenAttr = connection[0].split('.')[1]
                          
            # get the keys indicesof the curveAnimNode
            idx = mc.getAttr(animCrv+'.keyTimeValue', mi = 1)
            
            # for every index (key) get the Time a
            for id in idx:
                drivenValue = mc.getAttr(animCrv+'.keyTimeValue['+str(id)+'].keyTime')
                driverValue = mc.getAttr(animCrv+'.keyTimeValue['+str(id)+'].keyValue') 
                command = command +"mc.setDrivenKeyframe('"+drivenObj+"', at = '"+drivenAttr+"', cd = '"+driverObj+"."+driverAttr+"', driverValue = "+str(drivenValue)+", value = "+str(driverValue)+")\n"    
                       
    # print command    
    if UI == True: 
        # UI
        if mc.window('printed', ex = 1): mc.deleteUI('printed')
        mc.window('printed')
        mc.rowColumnLayout()
        #mc.rowColumnLayout(nc = 2, cw = [(1,350),(2,350)])
        #mc.button()
        mc.button(label = 'test script', c = "exec(mc.scrollField('textCommand', q = 1, text = 1))")
        mc.scrollLayout(w = 1000, h = 700, p = 'printed')
        mc.scrollField('textCommand', text  = command, w = 1000, h = 2000)
        mc.showWindow('printed')
                    
    return command
    
cmdPrint()    
