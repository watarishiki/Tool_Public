# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
from maya import cmds
from maya import OpenMaya as om

class SceneConv():
    __currentPath = os.path.dirname(__file__)
    __metaDataPath = os.path.join(__currentPath, "meta.json")
    with open(__metaDataPath) as f:
        __metadata = json.load(f)
    
    def __init__(self) -> None:
        self.current_path = cmds.workspace(q = True, rd = True)

    def get_category(self,node):
        """node Attributeの値とjsonを照らし合わせ、対応する値を返す

        Args:
            node (str):検索するノード名
        Returns:
            str:検索にヒットした場合そのValue、無ければ空文字
        """
        attrib = cmds.listAttr(node,ud=True) 
        category = ""
        try:
            category = cmds.getAttr(node+".category")
        except:
            print("has not Category attribute")
        val = self.__metadata[category] if category in self.__metadata.keys() else ""
        return val
    
    def get_nodes(self):
        """選択したノード以下のSM_が付くTransformノードを取得
        選択以下を再帰的に全収集した後その子供を集合から除外することでSMがついた最上位の親Transformノードだけ出力する。

        issue:listRelativesが直下の子にしか対応してないので再帰的に対応する
        issue:インスタンスを除外する
        
        """
        #選択したノード以下のSM_が付くTransformノードを取得
        nodes = cmds.ls(sl=True,tr=True,dag=True)
        # 'SM_' で始まるノードのみを選択
        nodes = [s for s in nodes if s.startswith('SM_')]
        childs = cmds.listRelatives(nodes,typ='transform',f=True)
        instances = []
        
        #SM_から始まるTransformノードの直下のShapeノードを取得して
        if childs:
            for child in childs:
                shapes = cmds.listRelatives(child, s=True, f=True)
                if not shapes:
                    continue
                for shape in shapes:
                    print(shape)
                    instances = cmds.listConnections(shape, type="transform", s=False, d=True)
                    if instances:
                        for instance in instances:
                            if instance in nodes:
                                nodes.remove(instance)

        if childs:
            nodes = list(set(nodes) - set(childs))
        self.nodes = nodes

    def set_shape_uuids(self,node):
        """
        指定されたノードの子孫のShapeノードのUUIDを取得し、カンマ区切りで結合した文字列を
        ノードのカスタムアトリビュートに設定する。

        Args:
            node (str): 処理対象のノード名
        """
        # 子孫のShapeノードのUUIDを取得
        shape_nodes = cmds.listRelatives(node, allDescendents=True, type='shape', f=True)
        shape_uuids = [cmds.ls(shape, uuid=True)[0] for shape in shape_nodes] if shape_nodes else []

        # UUIDをコロン区切りで結合
        concatenated_uuids = ':'.join(shape_uuids)

        #1こ上のTransformノードと選択したノード自身も追加
        shape_parent_nodes = cmds.listRelatives(shape_nodes, type='transform', p=True, f=True)
        shape_parent_nodes.append(node)

        for parent_node in shape_parent_nodes:
            # カスタムアトリビュートを追加し、結合したUUIDを設定
            if not cmds.attributeQuery('uuid', node=parent_node, exists=True):
                cmds.addAttr(parent_node, longName='uuid', dataType='string')
            cmds.setAttr(parent_node + '.uuid', concatenated_uuids, type='string')

    def export_FBXs(self, export_options):
        
        self.get_nodes()

        for node in self.nodes:
            #move to origin
            pivotPos = cmds.xform(node, q=True,sp=True,ws=True)
            trans = list(cmds.getAttr( node + ".translate" )[0])
            rot = list(cmds.getAttr( node + ".rotate" )[0])
            cmds.setAttr( node + ".translate", trans[0]+pivotPos[0]*-1.0,trans[1]+pivotPos[1]*-1.0, trans[2]+pivotPos[2]*-1.0, type="double3" )
            cmds.setAttr( node + ".rotate", 0,0,0, type="double3" )
            cmds.select(node)
            
            self.set_shape_uuids(node)

            #path setting
            dist_path = os.path.join(self.current_path,self.get_category(node),node.split('|')[-1],"FBX").replace("\\", "/")
            new_path = os.path.join(dist_path, "{}.fbx".format(node)).replace("\\", "/")
            if not os.path.isdir(dist_path):
                os.makedirs(dist_path)
            
            
            cmds.FBXPushSettings()
            #set export settings
            try:
                cmds.FBXResetExport()
                for option, value in export_options.items():
                    cmds.FBXProperty(option, "-v", value)                
                cmds.FBXProperty("Export|IncludeGrp|Geometry|Triangulate", "-v", 1)
                cmds.FBXProperty("Export|IncludeGrp|Animation", "-v", 0)
                cmds.FBXExportInputConnections("-v", 0)
                cmds.FBXExportCameras("-v", 0)
                cmds.FBXExportConstraints("-v", 0)
                cmds.FBXExportLights("-v", 0)
                om.MGlobal.executeCommand('FBXExport("-f", "{}", "-s")'.format(new_path))
            except:
                print("fail settings")
            else:
                print(f"{node} is exported to {new_path}")
            finally:
                cmds.FBXPopSettings()
                trans = list(cmds.getAttr( node + ".translate" )[0])
                cmds.setAttr( node + ".translate", trans[0]+pivotPos[0],trans[1]+pivotPos[1], trans[2]+pivotPos[2], type="double3" )
                cmds.setAttr( node + ".rotate", rot[0],rot[1], rot[2], type="double3" )

    def debug_category(self):
        self.get_nodes()
        for node in self.nodes:
            val = self.get_category(node)
            dist_path = os.path.join(self.current_path,self.get_category(node),node,"FBX")
            new_path = os.path.join(dist_path, "{}.fbx".format(node)).replace("\\", "/")
            print(new_path)
        shapes = cmds.listRelatives(self.nodes,typ='shape')
        print(shapes)

def main():
    conv = SceneConv()
    export_options = {
        "Export|IncludeGrp|Geometry|SmoothMesh": 0,
    }
    conv.export_FBXs(export_options)

def debug_main():
    conv = SceneConv()
    print("hello")

if __name__ == '__main__':
    main()