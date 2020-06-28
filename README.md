# Name（リポジトリ/プロジェクト/OSSなどの名前）

Apacheログ解析プログラム

Apache HTTP サーバのアクセスログを解析するプログラム．

# Features

各時間帯毎のアクセス件数，リモートホスト別のアクセス件数について複数ファイルの入力や期間指定に対応している．  
また，メモリ不足解消のためにメモリ使用率をファイルから１行読むごとに観察し，指定の使用率を越えた場合その場で読み取りを中断させ，その時点で読み取れているデータのみで解析を行い，変数をリセットさせている．

# Requirement

* python            3.８     
* apache-log-parser 1.7.0　　．．．Apacheのログを生データから読み取る際に使用．
* psutil            5.7.0　　．．．メモリ使用率を観察する際に使用．

# Installation

```bash
pip install apache-log-parser
pip install psutil
```

# Usage

実行方法
```bash
git clone https://github.com/tkykt314/FixPoint_problems.git
cd FixPoint_problems
python analyse_log.py
```

実行に必要な標準入力  
  以下の入力は全て半角で行うものとする．  
  メモリの許容使用率  
  期間指定の有無(y:有， n:無)  
    nを選んだ場合，同ディレクトリ内に存在し，ファイル名が「access_log」で始まる全てのログファイルの全てのデータを解析する．  
    yを選んだ場合，fromからtoにかけて始点と終点となる日付を入力する．（YYYY MM DD : M及Dは１桁でも可）
    指定された期間内で，同様の解析を行うものとする．
```bash
python analyse_log.py
メモリ使用率を設定
90
期間を指定しますか？　 y or n
y
from
2005 1 1
to
2２２２　１２  31
解析終了
```
解析結果はcsvファイルに出力している．
指定期間が無しの場合，デフォルトでホスト毎，時間帯毎でそれぞれhost.csv,time.csvとなる．
有りの場合，期間の始点と終点を含み，以下のようなファイル名になる．(2005年1月1日〜2010年1月1日の場合)
結果内容は各csvファイルを参考されたし．

```bash
host_20050101_20100101.csv
time_20050101_20100101.csv
```



# Author

* 本田 祥己


