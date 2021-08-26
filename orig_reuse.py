# Orig reuse tool v1
# This code will find the similar orig nodes, replace the connections with a main one and delete the remaining.

import maya.cmds as cmds

def orig_reuse(mainOrig = 'C_body_HIGEOShapeOrig', run=True):
    # list orig shapes
    origs = cmds.ls('*ShapeOrig')
    len(origs)
    # find the matching orig geometries
    mtch = []    
    for orig in origs:
        try:
            ret = cmds.polyCompare(mainOrig,orig,v=1,e=1,fd=1)
            if ret==0:
                mtch.append(orig)
        except:
            pass
    print mtch
    cmds.select(mtch)
    if mainOrig in origs:
        mtch.remove(mainOrig)
        if run: 
            if mtch:
                for orig in mtch:
                    try:   
                        # find outputs
                        wmCnn = cmds.listConnections('{}.worldMesh[0]'.format(orig),d=True,p=True)
                        print wmCnn
                        # replace outputs
                        # world Mesh
                        if wmCnn:
                            for cnn in wmCnn:
                                cmds.connectAttr('{}.worldMesh[0]'.format(mainOrig),cnn,f=True)
                        # out Mesh
                        omCnn = cmds.listConnections('{}.outMesh'.format(orig),d=True,p=True)
                        print omCnn
                        if omCnn:
                            for cnn in omCnn:
                                cmds.connectAttr('{}.outMesh'.format(mainOrig),cnn,f=True)
                        # delete remaining orig Shapes
                        cmds.delete(orig)
                    except:
                        pass

# RUN                       
higeoOrigs = cmds.ls('*HIGEOShapeOrig')
for hiOrig in higeoOrigs:
    orig_reuse(mainOrig = hiOrig, run=True)
                
