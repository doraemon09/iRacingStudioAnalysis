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

## Setup Instructions

Follow these steps to set up and run the application locally.

### 1. Create the "uploads" folder
At the root of your project directory, create a folder named `uploads`. This is where uploaded files will be stored.
```bash
mkdir uploads
```

### 2. Install Python 3.13.0
Make sure you have [Python 3.13.0](https://www.python.org/downloads/) installed on your machine.
To check if you already have Python installed, run the following command:
```bash
python --version
```
If Python is not installed, download and install Python 3.13.0 from the official website linked above.

### 3. Install Required Dependencies
The project requires several Python packages. You can install them using `pip`.
Run the following commands to install the required packages:
```bash
pip install flask
pip install pyyaml
pip install pandas
pip install pyirsdk
```

### 4. Start the Application
Once everything is installed and configured, you can start the Flask development server by running:
```bash
flask run
```
By default, the server will be accessible at `http://127.0.0.1:5000/` in your browser.

### 5. Accessing the Application
Open your web browser and go to `http://127.0.0.1:5000/` to access the application.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---

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

## セットアップ手順

以下の手順に従って、アプリケーションをローカル環境でセットアップして実行してください。

### 1. 「uploads」フォルダーの作成
プロジェクトディレクトリのルートに`uploads`という名前のフォルダーを作成してください。ここにアップロードされたファイルが保存されます。
```bash
mkdir uploads
```

### 2. Python 3.13.0 のインストール
[Python 3.13.0](https://www.python.org/downloads/) がマシンにインストールされていることを確認してください。すでにインストールされているか確認するには、以下のコマンドを実行します：
```bash
python --version
```
もしPythonがインストールされていない場合は、上記の公式サイトからPython 3.13.0をダウンロードしてインストールしてください。

### 3. 必要な依存関係のインストール
このプロジェクトにはいくつかのPythonパッケージが必要です。`pip`を使用してインストールできます。以下のコマンドを実行して必要なパッケージをインストールしてください：
```bash
pip install flask
pip install pyyaml
pip install pandas
pip install pyirsdk
```

### 4. アプリケーションの起動
すべてのインストールと設定が完了したら、以下のコマンドでFlask開発サーバーを起動できます：
```bash
flask run
```
デフォルトでは、サーバーはブラウザで `http://127.0.0.1:5000/` にアクセスすることで利用可能です。

### 5. アプリケーションへのアクセス
ウェブブラウザを開き、`http://127.0.0.1:5000/` にアクセスしてアプリケーションを使用できます。

## ライセンス

このプロジェクトは Apache License 2.0 の下でライセンスされています。詳細については [LICENSE](LICENSE) ファイルをご覧ください。
