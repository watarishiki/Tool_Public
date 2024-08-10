このリポジトリはツール集になっています。以下に一覧を用意致しました。

# シーン同期ツール
MayaとUnreal Engineでシーンを同期することを目的としたツール群を制作しました。

## カスタムアトリビュートによるカテゴリ追加機能
選択したTransformノードにカテゴリ名カスタムアトリビュートをドロップダウンで追加し、その後のエクスポート時のフォルダ構造を決定します。

https://github.com/watarishiki/Tool_Public/blob/main/Maya/wrCreateCustomAttrSimple/wrCreateCustomAttrSimple.py
![result](https://github.com/watarishiki/Tool_Public/blob/main/GIF/CreateAttribute.gif)


## バッチエクスポート
選択ノード以下の「SM_」から始まるTransformノードを収集して自動決定した階層にFBX出力します。
出力先は前述の追加されたカテゴリ用カスタムアトリビュートと、ユーザーが設定するコンフィグファイルから決定されます。
同時に、子のShapeノードのuuidを連結した文字列をカスタムアトリビュートに加え、コピーペースト時の識別に用います。（一意に特定できれば良いのでファイルパス自体をアトリビュートにするなどを検討しています）

https://github.com/watarishiki/Tool_Public/blob/main/Maya/wrSceneConverter/wrSceneConverter.py
![result](https://github.com/watarishiki/Tool_Public/blob/main/GIF/BatchExport.gif)

## バッチインポート
指定したフォルダ以下のFBXのうちまだインポートしていないファイルを一括でインポートします。

https://github.com/watarishiki/Tool_Public/blob/main/UE/fbxImport.py
![result](https://github.com/watarishiki/Tool_Public/blob/main/GIF/BatchImport02.gif)

## マルチコピーペースト
Maya→UE間でシーンを同期できるように選択ノードのTransformをコピー＆ペーストします。
uuidを元に同一のオブジェクトはUEでインスタンスとして処理されます。
クリップボードを用いているので別途CSVファイルなどを使用する必要がありません。

https://github.com/watarishiki/Tool_Public/blob/main/Maya/wrSceneConverter/wrSceneCopyPaste.py
https://github.com/watarishiki/Tool_Public/blob/main/UE/wrUESceneCopyPaste.py
![result](https://github.com/watarishiki/Tool_Public/blob/main/GIF/MultiPaste.gif)

# バッチレンダリング
Unreal Engineでのムービー書き出しを支援するツールです。バッチファイル１つで複数シーケンサのレンダリングを行うことができます。
起動時にスクリプトを実行しますがバッチファイル内のみでの設定になっているので他の作業者に影響が及びません。

https://github.com/watarishiki/Tool_Public/tree/main/UE/BatchRender
![result](https://github.com/watarishiki/Tool_Public/blob/main/GIF/BatchRender.gif)
