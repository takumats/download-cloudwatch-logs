import argparse
import boto3
import re
import traceback
from datetime import datetime
import download_logs

LOG_STREAM_NAME_PREFIX = ''
LOG_STREAM_NAME_POSTFIX = 'xml'

def get_log_streams(client, log_group_name):
    """ログイベント取得"""

    # 初回リクエスト
    response = client.describe_log_streams(
        logGroupName=log_group_name
    )
    print('Count of log streams: ' + str(len(response['logStreams'])))
    print('nextToken: ' + response['nextToken'])

    # 取得したイベントを返す
    yield response['logStreams']

    while True:
        # nextForwardTokenを取得
        prev_token = response['nextToken']

        # 2回目以降のリクエスト
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            nextToken=prev_token
        )
        print('Count of log streams: ' + str(len(response['logStreams'])))
        print('nextToken: ' + response['nextToken'])

        # 取得したログストリームを返す
        yield response['logStreams']

        # nextTokenが前回と同じであればログストリームを最後まで取得した
        if response['nextToken'] == prev_token:
            break

def main():
    """メインメソッド"""

    try:
        # 引数定義
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument(
            '-r',
            '--region',
            metavar='REGION',
            default='ap-northeast-1',
            help='リージョンを指定する（デフォルト：ap-northeast-1）'
        )
        arg_parser.add_argument(
            'log_group',
            metavar='LOG_GROUP',
            help='ロググループ名を指定する'
        )

        # 引数取得
        args = arg_parser.parse_args()
        region = args.region
        log_group = args.log_group

        # CloudWatch Logs クライアント取得
        client = boto3.client('logs', region_name=region)

        # ログストリームを取得
        for log_streams in get_log_streams(client, log_group):
            for log_stream in log_streams:
                if len(LOG_STREAM_NAME_PREFIX) !=0 and not log_stream['logStreamName'].beginswith(LOG_STREAM_NAME_PREFIX):
                    continue
                if len(LOG_STREAM_NAME_POSTFIX) !=0 and not log_stream['logStreamName'].endswith(LOG_STREAM_NAME_POSTFIX):
                    continue

                download_logs.retrieve_events(region, log_group, log_stream['logStreamName'])

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()