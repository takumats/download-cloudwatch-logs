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
python3 download_logs.py <LOG_GROUP> <LOG_STREAM>
```

```
python3 download_log_stream_logs.py <LOG_GROUP>
```

## 制限事項
* エントリー長が256KBを超える場合に元の行がそこで改行されていますが、それについての考慮がされていません。
