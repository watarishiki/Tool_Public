import unreal
import tkinter as tk
import pprint

class wrUESceneCopyPaste():
    def __init__(self) -> None:
        r = tk.Tk()
        r.withdraw()
        self.clip = r.clipboard_get()

    def parse_clipboard(self,clip):
        """クリップボードをパースしてアセット名、トランスフォームの辞書型のリストを出力
        args:
            clip(str):クリップボードの文字列
        return:
            dict:{通し番号（int）:[ラベル名、スタティックメッシュオブジェクト名、[transformの各数値9個（float）]]}の形の辞書
        """
        objs_dict = {}
        objs = clip.splitlines()
        for loop,obj in enumerate(objs):
            #create dict
            obj_dict = {}
            #get obj name and transform from clipboard
            data = obj.split(sep=',')
            if len(data) != 12:
                print("is not transform type")
                continue

            # get name
            obj_id = data[0]
            obj_label = data[1]
            obj_name = data[2]

            #get transform from clipboard
            array = [float(s) for s in data[3:]]
            obj_transform = unreal.Transform(location=unreal.Vector(array[0],array[2],array[1]),rotation=unreal.Rotator(array[3],array[5],array[4]*-1.0),scale=unreal.Vector(array[6],array[8],array[7]))
            objs_dict[loop] = [obj_id,obj_label,obj_name,obj_transform]

        return objs_dict

    def main(self):
        unreal.SystemLibrary.begin_transaction("UESceneCopyPaste",unreal.Text("ScenePaste"),None)
        assetregistry = unreal.AssetRegistryHelpers.get_asset_registry()

        #get asset info from asset registry
        list_asset_data = unreal.AssetRegistry.get_assets_by_path(assetregistry,"/Game/Environment",recursive=True)

                # Get the 'uuid' metadata for each asset and store it in a list
        list_asset_uuids = []
        for asset in list_asset_data:
            uuid = unreal.EditorAssetLibrary.get_metadata_tag(unreal.AssetRegistryHelpers.get_asset(asset), "FBX.uuid")
            list_asset_uuids.append(str(uuid) if uuid is not None else "nothing")
        
        print(f"uuid lists length:{len(list_asset_uuids)} lists:{list_asset_uuids}")

        list_asset_name = [str(list.asset_name) for list in list_asset_data]
        list_asset_path = [str(list.package_name) + '.' + str(list.asset_name) for list in list_asset_data]
        dict_asset_data = dict(zip(list_asset_uuids,list_asset_path))

        #get current level info
        current_actors = unreal.EditorLevelLibrary.get_all_level_actors()
        current_actor_labels = [current_actor.get_actor_label() for current_actor in current_actors]
        current_actor_ids = [str(current_actor.tags[0]) if len(current_actor.tags) != 0 else "None" for current_actor in current_actors]
        dict_current_actors = dict(zip(current_actor_ids,current_actors))
        #pprint.pprint(dict(zip(list_asset_name,list_asset_path)))

        #get scene data from clipboard
        clip_asset_data = self.parse_clipboard(self.clip)

        #sync ue scene every obj
        for asset_loop,asset in clip_asset_data.items():
            asset_id = asset[0]
            #convert label in |*|*|asset_name to */* folder and asset_name
            asset_label = asset[1].rsplit('|',1)[1]
            asset_folder = asset[1].rsplit('|',1)[0].replace('|','/').removeprefix('|')
            asset_name = asset[2]
            asset_transform = asset[3]

            print(f"Asset ID: {asset_id}, Asset Label: {asset_label}, Asset Folder: {asset_folder}, Asset Name: {asset_name}, Asset Transform: {asset_transform}")

            #sync actor if asset in content
            if asset_name in dict_asset_data.keys():
                #sync position if actor already spawned
                print("asset id is {}",asset_id)
                if asset_id in current_actor_ids:
                    print("{} is already placed.",asset_id)
                    current_actor = dict_current_actors[str(asset_id)]
                    unreal.SystemLibrary.transact_object(current_actor)
                    current_actor.set_actor_transform(asset_transform,sweep=True,teleport=True)
                    current_actor.set_actor_label(asset_label)
                    current_actor.set_folder_path(asset_folder)
                    continue

                #spawn actor and set actor property
                actor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor,asset_transform.get_editor_property("translation"),asset_transform.get_editor_property("rotation").rotator())
                unreal.SystemLibrary.transact_object(actor)
                actor.set_actor_scale3d(asset_transform.get_editor_property("scale3d"))
                actor = unreal.StaticMeshActor.cast(actor)
                actor.set_actor_label(asset_label)
                actor.set_folder_path(asset_folder)
                print(asset_label.rsplit('|',1)[0].replace('|','/'))
                tags = []
                tags.append(asset_id)
                actor.tags = tags


                #set component property
                static_mesh = unreal.SystemLibrary.load_asset_blocking(unreal.SystemLibrary.conv_soft_obj_path_to_soft_obj_ref(unreal.SoftObjectPath(dict_asset_data[asset_name])))
                actor.static_mesh_component.set_static_mesh(static_mesh)
                print(dict_asset_data[asset_name])
        unreal.SystemLibrary.end_transaction()

cp = wrUESceneCopyPaste()
cp.main()