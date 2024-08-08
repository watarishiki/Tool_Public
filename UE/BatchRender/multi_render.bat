@echo off
@rem "render_mode->single or folder シーケンサを複数レンダリングするか、１つレンダリングするか"
@rem "single mode -render_sequence,-render_levelが必須です。-render_sequence:レンダリングするシーケンサのSoft object path　-render_level:ロードするマップ"
@rem "folder mode -render_folder,-render_levelが必須です。-render_folder:レンダリングするシーケンサのルートディレクトリ object path　-render_level:ロードするマップ"
@rem "共通引数 -render_path:出力先　StartupObjects:起動時に実行するブループリントのパス"
@rem "mp4に変換する場合、ffmpegなどのコマンドラインエンコーダをダウンロードし、ExecutablePathを変更して下さい。"
@rem "必須プラグイン：Editor Scripting Utilities,Sequencer Scripting,Movie Render Queue"
@rem "このバッチファイルはuprojectと同じ階層に置いて下さい。各行末の「 ^」は変更しないでください。"
echo rendering start... 
"D:\LauncherUE4\Engine\UE_5.2\Engine\Binaries\Win64\UnrealEditor.exe" "%CD%\ThirdPerson52.uproject" ^
-render_mode=folder ^
-render_sequence=/Game/Cinematics/NewLevelSequence.NewLevelSequence ^
-render_folder=/Game/Cinematics ^
-render_path=D:\Movie ^
-render_level=/Game/ThirdPerson/Maps/ThirdPersonMap.ThirdPersonMap ^
-ini:EditorPerProjectUserSettings:[/Script/Blutility.EditorUtilitySubsystem]:StartupObjects=/Game/EUW/EUT_StartupRender.EUT_StartupRender ^
-ini:Engine:[/Script/MovieRenderPipelineCore.MoviePipelineCommandLineEncoderSettings]:ExecutablePath=D:\Application\ffmpeg-6.0-essentials_build\bin\ffmpeg.exe ^
-ini:Engine:[/Script/MovieRenderPipelineCore.MoviePipelineCommandLineEncoderSettings]:VideoCodec=libx264 ^
-ini:Engine:[/Script/MovieRenderPipelineCore.MoviePipelineCommandLineEncoderSettings]:AudioCodec=aac ^
-ini:Engine:[/Script/MovieRenderPipelineCore.MoviePipelineCommandLineEncoderSettings]:OutputFileExtension=mp4 ^