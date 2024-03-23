# 参考サイト)
# * https://qiita.com/ozzy3/items/fd79d07f42215298e38d
# * https://qiita.com/takumats/items/0bfa11e8909e27e09044
import argparse
import boto3
import re
import traceback
from datetime import datetime

def get_log_events(client, log_group_name, log_stream_name):
    """ログイベント取得"""

    # 初回リクエスト
    response = client.get_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        startFromHead=True
    )
    print('Count of events: ' + str(len(response['events'])))
    print('nextForwardToken: ' + response['nextForwardToken'])

    # 取得したイベントを返す
    yield response['events']

    while True:
        # nextForwardTokenを取得
        prev_token = response['nextForwardToken']

        # 2回目以降のリクエスト
        response = client.get_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            nextToken=prev_token
        )
        print('Count of events: ' + str(len(response['events'])))
        print('nextForwardToken: ' + response['nextForwardToken'])

        # 取得したイベントを返す
        yield response['events']

        # nextForwardTokenが前回と同じであればログイベントを最後まで取得した
        if response['nextForwardToken'] == prev_token:
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
        arg_parser.add_argument(
            'log_stream',
            metavar='LOG_STREAM',
            help='ログストリーム名を指定する'
        )

        # 引数取得
        args = arg_parser.parse_args()
        region = args.region
        log_group = args.log_group
        log_stream = args.log_stream

        # ファイル名に使用できない文字を置換
        replaced_log_stream = re.sub('[\\/:*?"<>|]', '_', log_stream)

        # 出力ファイル名
        output_filename = 'aws_logs_' + replaced_log_stream + '.txt'

        # CloudWatch Logs クライアント取得
        client = boto3.client('logs', region_name=region)

        # ファイルオープン
        with open(output_filename, 'w', encoding='UTF-8') as f:

            # ログイベントを取得
            for events in get_log_events(client, log_group, log_stream):

                # ログのタイムスタンプとメッセージを抽出
                #messages = [datetime.fromtimestamp(event.get('timestamp')/1000).isoformat()
                #            + '\t' + event.get('message') for event in events]
                messages = [event.get('message') + '\n' for event in events]

                # ファイル出力
                f.writelines(messages)

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()