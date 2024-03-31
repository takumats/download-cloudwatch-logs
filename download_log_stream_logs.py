import argparse
import boto3
import re
import traceback
from datetime import datetime
import download_logs

def get_log_streams(client, log_group_name):
    """ログストリーム取得"""

    # 初回リクエスト
    response = client.describe_log_streams(
        logGroupName=log_group_name
    )
    print('Count of log streams: ' + str(len(response['logStreams'])))
    yield response['logStreams']

    # nextTokenがなければ次はない
    if 'nextToken' not in response:
        return
    #print('nextToken: ' + response['nextToken'])

    # 取得したイベントを返す


    while True:
        # nextForwardTokenを取得
        prev_token = response['nextToken']

        # 2回目以降のリクエスト
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            nextToken=prev_token
        )
        print('Count of log streams: ' + str(len(response['logStreams'])))
        yield response['logStreams']

        # nextTokenがないか前回と同じであればログストリームを最後まで取得した
        if 'nextToken' not in response or response['nextToken'] == prev_token:
            break
        #print('nextToken: ' + response['nextToken'])


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
            help='リージョン(デフォルト:ap-northeast-1)'
        )
        arg_parser.add_argument(
            '--prefix',
            metavar='PREFIX',
            default='',
            help='ログストリーム名prefix(デフォルト:指定なし)'
        )
        arg_parser.add_argument(
            '--postfix',
            metavar='POSTFIX',
            default='',
            help='ログストリーム名postfix(デフォルト:指定なし)'
        )
        arg_parser.add_argument(
            '--datefrom',
            metavar='DATE_FROM',
            default='',
            help='ログダウンロード範囲(開始日時:yyyymmddhhmmss)(デフォルト:指定なし)'
        )
        arg_parser.add_argument(
            '--dateto',
            metavar='DATE_TO',
            default='',
            help='ログダウンロード範囲(終了日時:yyyymmddhhmmss)(デフォルト:指定なし)'
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
        log_stream_name_prefix = args.prefix
        log_stream_name_postfix = args.postfix
        event_date_from = datetime.strptime(args.datefrom, '%Y%m%d%H%M%S') if args.datefrom != '' else datetime.min
        event_date_to = datetime.strptime(args.dateto, '%Y%m%d%H%M%S') if args.dateto != '' else datetime.max

        # CloudWatch Logs クライアント取得
        client = boto3.client('logs', region_name=region)


        # ログストリームを取得
        for log_streams in get_log_streams(client, log_group):
            for log_stream in log_streams:
                if len(log_stream_name_prefix) !=0 and not log_stream['logStreamName'].beginswith(log_stream_name_prefix):
                    continue
                if len(log_stream_name_postfix) !=0 and not log_stream['logStreamName'].endswith(log_stream_name_postfix):
                    continue
                
                first_event_date = datetime.fromtimestamp(log_stream['firstEventTimestamp']/1000.0)
                last_event_date = datetime.fromtimestamp(log_stream['lastEventTimestamp']/1000.0)
                if first_event_date < event_date_from:
                    continue
                if event_date_to < last_event_date:
                    continue

                download_logs.retrieve_events(region, log_group, log_stream['logStreamName'], event_date_from, event_date_to)

    except Exception as e:
        traceback.print_exc()


if __name__ == '__main__':
    main()