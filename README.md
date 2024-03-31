# download-cloudwatch-logs
A Python script to download log messages from CloudWatch Logs to a file.

## setup
```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## usage
```
usage: download_logs.py [-h] [-r REGION] [--datefrom DATE_FROM] [--dateto DATE_TO] LOG_GROUP LOG_STREAM

positional arguments:
  LOG_GROUP             ロググループ名を指定する
  LOG_STREAM            ログストリーム名を指定する

options:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        リージョンを指定する(デフォルト:ap-northeast-1)
  --datefrom DATE_FROM  ログダウンロード範囲(開始日時:yyyymmddhhmmss)(デフォルト:指定なし)
  --dateto DATE_TO      ログダウンロード範囲(終了日時:yyyymmddhhmmss)(デフォルト:指定なし)
```

```
usage: download_log_stream_logs.py [-h] [-r REGION] [--prefix PREFIX] [--postfix POSTFIX] [--datefrom DATE_FROM] [--dateto DATE_TO] LOG_GROUP

positional arguments:
  LOG_GROUP             ロググループ名を指定する

options:
  -h, --help            show this help message and exit
  -r REGION, --region REGION
                        リージョン(デフォルト:ap-northeast-1)
  --prefix PREFIX       ログストリーム名prefix(デフォルト:指定なし)
  --postfix POSTFIX     ログストリーム名postfix(デフォルト:指定なし)
  --datefrom DATE_FROM  ログダウンロード範囲(開始日時:yyyymmddhhmmss)(デフォルト:指定なし)
  --dateto DATE_TO      ログダウンロード範囲(終了日時:yyyymmddhhmmss)(デフォルト:指定なし)
```

## 制限事項
* エントリー長が256KBを超える場合に元の行がそこで改行されていますが、それについての考慮がされていません。
