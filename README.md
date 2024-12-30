# iRacing Studio Analysis

A Flask-based web application designed to process, analyze, and display [iRacing](https://www.iracing.com/) telemetry data. The application supports file uploads, telemetry processing, and detailed data visualizations, offering insights into laps, sectors, throttle/brake usage, and more.

## Features

- **Telemetry File Upload**: Accepts iRacing telemetry files (`.ibt`) for processing.
- **Data Visualization**: Provides detailed charts and maps for telemetry insights.
  - **Charts**:
    - Lap time delta
    - Speed delta
    - Brake and throttle usage
    - Steering angle and torque
    - Lateral G-force and yaw
  - **Maps**:
    - Track map with speed, altitude, and sector data
    - Tire pressure, temperature, and ride height overlays
    - Shock deflection and velocity
- **Sector Analysis**: Breaks down lap times by track sectors with theoretical best lap calculations.
- **Advanced Data Insights**:
  - Throttle, brake, and coast time analysis.
  - Fuel usage reports.
  - Reference lap data with comparisons.
  - Weather conditions and sensor data.
- **Database Integration**: Retrieves preprocessed telemetry data for demonstration purposes.
- **Custom Jinja2 Filters**: Formats lap times, converts distances, and more.

## Demo

A live demo of the application is available **[here](http://ec2-13-52-127-109.us-west-1.compute.amazonaws.com/)**, hosted on an AWS EC2 instance (Free Tier).

https://github.com/user-attachments/assets/55d70c3b-ebd6-4ed5-8862-3d143ee80da9

## Installation

1. **Install Python**:
   - Download and install Python (version 3.8 or higher):
     - Visit the official [Python downloads page](https://www.python.org/downloads/).
     - Choose the appropriate installer for your operating system.
     - Ensure you check **"Add python.exe to PATH"** during installation (Windows users).

   - Verify the installation:
     ```bash
     python --version
     ```
     Or, if required:
     ```bash
     python3 --version
     ```
2. **Clone the Repository**:
   ```bash
   git clone https://github.com/doraemon09/iRacingStudioAnalysis.git
   ```
   ```bash
   cd iRacingStudioAnalysis
   ```
3. **Set Up Virtual Environment**:
   ```bash
   python -m venv venv
   ```
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install Required Packages**:
   - Install all dependencies listed in the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```
5. **Run the Application**:
   - **Local Mode**:
     ```bash
     python app.py --localhost
     ```
   - **Production Mode**:
     ```bash
     python app.py
     ```

## Usage

1. **Upload Telemetry Files**:
   - Navigate to the root URL (`http://127.0.0.1:5001` for local mode).
   - Upload `.ibt` files for processing.

2. **Explore Data**:
   - **Charts**:
     - View telemetry insights with interactive charts, including:
       - Lap time delta
       - Speed delta
       - Throttle and brake usage
       - Steering angle and torque
       - Lateral G-force and yaw
   - **Maps**:
     - Visualize telemetry data on track maps:
       - Speed and sector overlays
       - Altitude and lateral G-force data
       - Tire temperature and pressure
       - Ride height, shock deflection, and velocity insights

3. **Demo Mode**:
   - In production, access preloaded demo data from the database.

## Contribution

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Description"`).
4. Push to your branch (`git push origin feature-name`).
5. Submit a pull request.

## Acknowledgments

- This project utilizes the [pyirsdk library](https://github.com/kutu/pyirsdk) to access iRacing telemetry data. Special thanks to the contributors of `pyirsdk` for making this integration possible and enabling efficient telemetry processing.
- Built with [Flask](https://flask.palletsprojects.com/).
- Utilizes libraries like `pandas`, `numpy`, `sqlite3`, and `irsdk`.

## License

This project is licensed under the **Apache License 2.0**. See the `LICENSE` file for details.

---

# iRacingスタジオアナリシス

Flaskベースのウェブアプリケーションで、[iRacing](https://www.iracing.com/)のテレメトリーデータを処理、分析、表示するためのツールです。このアプリケーションはファイルのアップロード、テレメトリーデータの処理、詳細なデータの可視化をサポートしており、ラップ、セクター、スロットル/ブレーキ使用状況などの分析を提供します。

## 機能

- **テレメトリーファイルのアップロード**:
  - iRacingのテレメトリーファイル（`.ibt`）を処理します。
  
- **データの可視化**:
  - 詳細なチャートやマップでテレメトリーデータを視覚化します。
  - **チャート**:
    - ラップタイムデルタ
    - スピードデルタ
    - ブレーキとスロットルの使用状況
    - ステアリング角度とトルク
    - 横方向Gフォースとヨー
  - **マップ**:
    - トラックマップ上にスピードとセクターオーバーレイを表示
    - 高度と横方向Gフォースデータ
    - タイヤ温度と圧力のインサイト
    - ライドハイト、ショックディフレクション、ショック速度のデータ

- **セクター分析**:
  - トラックセクターごとにラップタイムを分割し、理論上の最速ラップを計算します。

- **高度なデータ分析**:
  - スロットル、ブレーキ、コーストタイムの分析
  - 燃料使用レポート
  - リファレンスラップデータの比較
  - 天候条件やセンサーデータの確認

- **データベース統合**:
  - デモ用に事前処理されたテレメトリーデータを取得できます。

- **カスタムJinja2フィルター**:
  - ラップタイムのフォーマット、距離の変換などに対応しています。

## デモ

アプリケーションのライブデモは **[こちら](http://ec2-13-52-127-109.us-west-1.compute.amazonaws.com/)** で利用可能で、AWS EC2インスタンス（無料枠）上でホストされています。

https://github.com/user-attachments/assets/96ba54cc-0e72-4529-a3d1-71cd4e144742

## インストール

1. **Pythonをインストール**:
   - Python（バージョン3.8以上）をダウンロードしてインストールします：
     - 公式サイトの[Pythonダウンロードページ](https://www.python.org/downloads/)にアクセスしてください。
     - お使いのOS（Windows、macOS、Linux）に適したインストーラーを選択します。
     - インストール中に「**Add python.exe to PATH**」にチェックを入れてください（Windowsユーザー）。

   - インストール後、以下のコマンドでPythonのインストールを確認してください：
     ```bash
     python --version
     ```
     または、Python 3を使用する場合：
     ```bash
     python3 --version
     ```
2. **リポジトリをクローン**:
   ```bash
   git clone https://github.com/doraemon09/iRacingStudioAnalysis.git
   ```
   ```bash
   cd iRacingStudioAnalysis
    ```
3. **仮想環境を設定**:
   ```bash
   python -m venv venv
   ```
   ```bash
   source venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```
4. **必要なパッケージのインストール**:
   - `requirements.txt`ファイルに記載されたすべての依存関係をインストールします：
     ```bash
     pip install -r requirements.txt
     ```
5. **アプリケーションを実行**:
   - **ローカルモード**:
     ```bash
     python app.py --localhost
     ```
   - **本番モード**:
     ```bash
     python app.py
     ```

## 使い方

1. **テレメトリーファイルをアップロード**:
   - ルートURL（ローカルモードの場合は`http://127.0.0.1:5001`）にアクセスします。
   - `.ibt`ファイルをアップロードして処理します。

2. **データの探索**:
   - **チャート**:
     - インタラクティブなチャートでテレメトリーデータを視覚化します。以下を含みます：
       - ラップタイムデルタ
       - スピードデルタ
       - スロットルとブレーキの使用状況
       - ステアリング角度とトルク
       - 横方向Gフォースとヨー
   - **マップ**:
     - トラックマップ上でテレメトリーデータを可視化します：
       - スピードとセクターオーバーレイ
       - 高度と横方向Gフォースデータ
       - タイヤの温度と圧力
       - ライドハイト、ショックディフレクション、および速度のインサイト

3. **デモモード**:
   - 本番環境では、データベースから事前にロードされたデモデータにアクセスできます。

## 貢献

1. リポジトリをフォークします。
2. 新しいブランチを作成します（`git checkout -b feature-name`）。
3. 変更をコミットします（`git commit -m "Description"`）。
4. 自分のブランチにプッシュします（`git push origin feature-name`）。
5. プルリクエストを送信します。

## 謝辞

- このプロジェクトは、iRacingのテレメトリーデータにアクセスするために[pyirsdkライブラリ](https://github.com/kutu/pyirsdk)を利用しています。`pyirsdk`の貢献者の方々に感謝いたします。
- [Flask](https://flask.palletsprojects.com/)で作成されています。
- `pandas`、`numpy`、`sqlite3`、`irsdk`などのライブラリを利用しています。

## ライセンス

このプロジェクトは**Apache License 2.0**のもとでライセンスされています。詳細は`LICENSE`ファイルをご覧ください。
