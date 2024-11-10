# iRacing Studio Analysis

> A Flask application for uploading and analyzing iRacing telemetry (`.ibt`) files to retrieve session and telemetry information.

## Introduction

This application allows users to upload iRacing telemetry files in `.ibt` format to view session metadata (e.g., weather and car setup) and telemetry data (e.g., lap times and throttle information). The data is displayed on an HTML page for easy viewing.

## Features

- **File Upload**: Securely upload `.ibt` telemetry files for processing.
- **Session Information Retrieval**: Extracts session metadata like weather and car setup.
- **Telemetry Data Extraction**: Retrieves telemetry data such as lap times and throttle values.
- **Secure Filename Handling**: Ensures safe storage of uploaded files with sanitized filenames.

## Credits

This project uses the [pyirsdk](https://github.com/kutu/pyirsdk) library to access iRacing telemetry data. Special thanks to the contributors of `pyirsdk` for making this project possible.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


# iRacing スタジオ アナリシス

> iRacing テレメトリ (`.ibt`) ファイルをアップロードおよび分析し、セッションとテレメトリ情報を取得するための Flask アプリケーション。

## 概要

このアプリケーションを使用すると、ユーザーは `.ibt` 形式の iRacing テレメトリ ファイルをアップロードし、セッションのメタデータ（天気、車両設定など）やテレメトリ データ（ラップタイム、スロットルデータなど）を表示できます。データは HTML ページに表示され、簡単に閲覧できます。

## 機能

- **ファイルアップロード**: `.ibt` テレメトリ ファイルの安全なアップロードが可能
- **セッション情報の取得**: 天候や車両設定などのセッション メタデータを抽出
- **テレメトリデータの抽出**: ラップタイムやスロットル値などのテレメトリ データを取得
- **安全なファイル名処理**: `werkzeug.utils.secure_filename` を使用してファイル名を安全に保存

## クレジット

このプロジェクトでは、iRacing テレメトリ データにアクセスするための [pyirsdk](https://github.com/kutu/pyirsdk) ライブラリを使用しています。`pyirsdk` の貢献者の皆様に感謝いたします。

## ライセンス

このプロジェクトは MIT ライセンスの下でライセンスされています。詳細については [LICENSE](LICENSE) ファイルをご覧ください。
