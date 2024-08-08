事前準備
mp4で出力するには外部ツールのコマンドラインエンコーダが必要になります。ここではffmpegというソフトを使用してます
以下でffmpegをダウンロード、好きな場所に配置
https://ffmpeg.org/

使い方
1.EUT_StartupRender.uasset（ブループリント）、MPMC_mp4.uasset（レンダリングコンフィグデータ）をプロジェクト内のContentの好きな場所に配置
2.EUT_StartupRender.uassetを開き、変数In presetにMPMC_mp4を設定
3.multi_render.batを.uprojectと同じ階層に配置、テキストエディタで開いて引数に渡す内容をプロジェクト環境に応じて変更
4.プロジェクトで必須プラグイン：Editor Scripting Utilities,Sequencer Scripting,Movie Render Queueを有効化
5.multi_render.batをダブルクリック

バッチファイルの引数
10行目:UnrealEditor.exeの場所を絶対パスで記載します。その後uprojectの名前を記載します例）"D:\LauncherUE4\Engine\UE_5.2\Engine\Binaries\Win64\UnrealEditor.exe" "%CD%\ThirdPerson52.uproject"
-render_mode:	モード選択になります。render_modeをsingle or folderで入力して下さい。シーケンサを複数レンダリングするか、１つレンダリングするか
-render_sequence: sigleモード時にレンダリングするシーケンサーのSoft object path
-render_folder:	folderモード時にレンダリングするフォルダ以下のpath
-render_path:	出力先のフォルダ
-render_level:	レンダリングするPLマップのSoft object path
-ini:EditorPerProjectUserSettings:[/Script/Blutility.EditorUtilitySubsystem]:StartupObjects:	EUT_StartupRender.uassetのSoft object path
-ini:Engine:[/Script/MovieRenderPipelineCore.MoviePipelineCommandLineEncoderSettings]:ExecutablePath	ffmpegの絶対パス

ちなみに「 ^」はバッチファイルの改行文字なので消さないでください。

レンダリングコンフィグの変更：
MPMC_mp4（エンコーダを使ったMP4出力のプリセット）以外にもカスタマイズしたい場合MovieRenderQueueの画面からプリセットの保存ができるので保存後EUT_StartupRender.uassetを開き、変数In presetにセットして下さい。


Soft object pathの記法(UE5.1以降)
簡単に記載するにはContent Browserで右クリックしてペースト、'’で囲まれた部分を抽出するのが良いです。
例）
/Script/LevelSequence.LevelSequence'/Game/Cinematics/NewLevelSequence.NewLevelSequence'→/Game/Cinematics/NewLevelSequence.NewLevelSequence

---