from PySide2 import QtGui
import maya.cmds as cmds
import re

class wrSceneCopyPaste():
    def getTransform(self,node):
        """transformノードから位置取得し汎用に整形する
        Args:
            node(str):transformノード
        Returns:
            str:汎用型の位置情報
        """

        # トランスレーション、ローテーション、スケール値を取得
        trans = cmds.getAttr(node + ".translate")
        rot = cmds.getAttr(node + ".rotate")
        scale = cmds.getAttr(node + ".scale")

        # 値を結合し、テキスト形式で出力
        tform = trans + rot + scale
        cliptext = str(tform)

        # 不要な文字を除去してフォーマット整形
        cliptext = cliptext.replace('(', '')
        cliptext = cliptext.replace(')', '')
        cliptext = cliptext.replace('[', '')
        cliptext = cliptext.replace(']', '')        
        return cliptext
    
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

    def getScene(self):
        """
        選択したノードの子孫ノードの内、「SM_」から始まるTransformノードに対して
        uuid, フルパス, uuidカスタムアトリビュートの値, Transform値を取得しクリップボードに保存する
        """
        nodes = []

        # 選択したノードの子孫ノードを取得+自分自身
        selections = cmds.ls(sl=True, dag=True, long=True,type="transform")
        for selection in selections:
            print(f"selected node : {selection}")
            last_element = selection.split('|')[-1]
            if last_element.startswith("SM_"):
                nodes.append(selection)

        scene_text = ""
        
        print(f"selected node count : {len(nodes)}")

        # 各ノードについて情報を収集
        for node in nodes:
            # UUIDの取得
            uuid = cmds.ls(node, uuid=True)[0]  

            # カスタムアトリビュート'uuid'の値を取得存在しない場合値を設定
            custom_uuid = ""
            if cmds.attributeQuery('uuid', node=node, exists=True):
                custom_uuid = cmds.getAttr(node + '.uuid')
            else:
                self.set_shape_uuids(node)
                custom_uuid = cmds.getAttr(node + '.uuid')



            # Transform値の取得
            transform_value = self.getTransform(node)

            # UUID, フルパス, カスタムUUID, Transform値をカンマ区切りで結合
            obj_info = f"{uuid},{node},{custom_uuid},{transform_value}\n"
            scene_text += obj_info  
            print(obj_info)  # デバッグ用にコンソールに出力

        # クリップボードにテキストをセット
        cb = QtGui.QClipboard()
        cb.setText(scene_text)
    
def main():
    cp = wrSceneCopyPaste()
    cp.getScene()

if __name__ == '__main__':
    main()