import unreal
import glob
import os

class fbxImport():
    def __init__(self, relative_fbx_path="../DCC"):
        # Unreal Engineプロジェクトのディレクトリを取得
        self.proj_dir = unreal.SystemLibrary.get_project_directory()
        # FBXファイルが格納されている相対パス
        self.relative_fbx_path = relative_fbx_path
        # FBXファイルのルートディレクトリのフルパスを生成
        self.fbx_root_dir = os.path.join(self.proj_dir, self.relative_fbx_path)

    def get_fbx_paths(self):
        # FBXファイルを検索するためのパスを生成
        match_path = os.path.join(self.fbx_root_dir, "**/*.fbx")
        # 指定されたパス以下のFBXファイルを全て取得
        self.fbx_paths = glob.glob(match_path, recursive=True)

        # パス内のバックスラッシュをスラッシュに置換し、特定の条件に合致するファイルのみをリストに追加
        self.fbx_paths = [
            s.replace('\\', '/')
            for s in self.fbx_paths
            if "_high" not in s
        ]

    def debug_fbx_info(self):
        # FBXファイルのパス情報を取得し、デバッグ情報として出力
        self.get_fbx_paths()
        print(self.fbx_paths)
        for file_path in self.fbx_paths:
            # 最初のFBXファイルのパスを取得してデバッグ出力
            file_path = self.fbx_paths[0]
            dir = file_path.split("../DCC/")[1]
            name = file_path.split('/')[-1].split('.')[0]
            dir = os.path.join("/Game", dir.split(name)[0], "Mesh")
            print(dir)
            print(name)
            print(file_path)

    def make_option(self):
        # FBXインポートオプションの設定
        op = unreal.FbxImportUI()
        # マテリアルのインポートを無効化
        op.import_materials = False
        # 自動生成の衝突処理を無効化
        op.static_mesh_import_data.auto_generate_collision = False
        # メッシュの結合を有効化
        op.static_mesh_import_data.combine_meshes = True
        self.op = op
    
    def make_task(self, fbx_path, destination_path, object_name):
        # FBXファイルのインポートタスクを作成


        # インポートタスクの設定
        task = unreal.AssetImportTask()
        task.automated = True
        task.destination_name = object_name
        task.destination_path = destination_path
        task.filename = fbx_path
        task.replace_existing = True
        return task

    def execute_tasks(self):
        """
        指定したパス以下のfbxファイルパスを収集しそれぞれに対して対応したContentsフォルダ内パスを作成する。新規作成のアセットに対してインポートを行う
        """
        self.get_fbx_paths()
        self.make_option()
        tasks = []
        import_list = []

        # ファイルごとに宛先パスを作成しFBXインポートタスクを追加
        for fbx_path in self.fbx_paths:
            #fbx_pathをEnvironment/Objects/furnitureのような中間パス、拡張子なしのファイル名に分解してContentsフォルダ用に再結合する
            name = fbx_path.split('/')[-1].split('.')[0]
            dir = fbx_path.split("../DCC/")[1]
            destination_path = os.path.join("/Game", dir.split(name)[0], "Mesh")

            # destination_pathが選択されているフォルダ以下である場合のみタスクを作成
            destination_asset = os.path.join(destination_path,name)
            if not unreal.EditorAssetLibrary.does_asset_exist(destination_asset):

                # if selected_folder in destination_path:
                task = self.make_task(fbx_path,destination_path,name)
                tasks.append(task)
                import_list.append(destination_asset)
                print(f"{destination_asset}is creating...")
            else:
                print(f"{destination_asset} is already created. skip")
        
        confirmation=unreal.EditorDialog.show_message(
            "以下のパスにFBXをインポートします。続行しますか？",
            "\n".join(import_list),
            unreal.AppMsgType.YES_NO
        )

        # ユーザーがYESを選択した場合のみタスクを実行
        if confirmation == unreal.AppReturnType.YES:
            # Unreal Engineのアセットツールを使用してタスクを実行
            atool = unreal.AssetToolsHelpers.get_asset_tools()
            atool.import_asset_tasks(tasks)

def main():
    # インポート処理の実行
    fbx = fbxImport("../DCC/Environment")
    fbx.execute_tasks()

main()