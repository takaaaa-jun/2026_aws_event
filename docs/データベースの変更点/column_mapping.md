# データベースカラム対応表

データベース設計で定義された英語のカラム名と、インポート対象のCSVファイル（日本語ヘッダー）の対応表です。

## 1. clinic テーブル (クリニック情報)

| カラム名 (English) | データ型 | CSV対応ヘッダー (日本語) | 補足 |
| :--- | :--- | :--- | :--- |
| `clinic_id` | `int` | `No` | 主キー（自動採番） |
| `clinic_name` | `varchar` | `施設名` | |
| `clinic_postcode` | `text` | `〒` | 郵便番号 |
| `clinic_address` | `text` | `所在地1` + `所在地2` | 2つのカラムを結合して登録 |
| `clinic_tel` | `text` | `℡` | 電話番号 |
| `opening_date` | `text` | `開　 設 年月日` | 開設日 |
| `establisher` | `text` | `解説者` / `開設者` | 一般用CSVは「解説者」、歯科用は「開設者」 |
| `general_bed` | `int` | `一般病床` | 歯科の場合は空（NULL） |
| `recuperation_bed` | `int` | `療養病床` | 歯科の場合は空（NULL） |
| `remarks` | `text` | `備考` | |
| `signpost_flag` | `bool` | - | （本インポートでは使用せず空） |

## 2. latitude_longitude テーブル (緯度経度)

| カラム名 (English) | データ型 | CSV対応ヘッダー (日本語) | 補足 |
| :--- | :--- | :--- | :--- |
| `ll_id` | `int` | - | 主キー（自動採番） |
| `clinic_id` | `int` | - | `clinic`テーブルへの外部キー |
| `latitude` | `float` | `緯度` | |
| `longitude` | `float` | `経度` | |

## 3. department テーブル (診療科名)

| カラム名 (English) | データ型 | 説明 |
| :--- | :--- | :--- |
| `department_id` | `int` | 主キー（自動採番） |
| `department_name` | `text` | 診療科名（CSVヘッダーの「内科」「歯科」などから自動作成） |
