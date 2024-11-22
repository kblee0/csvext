import argparse
import pandas as pd
import csv
import sys

def extract_columns_to_new_csv(args):
    """
    CSV 파일에서 특정 컬럼을 추출하여 새로운 CSV 파일을 생성합니다.

    Args:
        input_csv: 입력 CSV 파일의 경로
        column_list_csv: 추출할 컬럼 목록이 담긴 CSV 파일의 경로
        output_csv: 출력 CSV 파일의 경로
    """

    # 컬럼 목록 CSV 파일 읽기
    columns = pd.read_csv(args.column_list_csv, encoding=args.oenc, header=None).values.tolist()[0]

    # 입력 CSV 파일 읽기
    df = pd.read_csv(args.input_csv)

    # 지정된 컬럼 추출 및 병합
    new_df = pd.DataFrame()
    for column in columns:
        if column in df.columns:
            new_df[column] = df[column]

            for i in range(1,11):
                rcol = column if i == 0 else column + "." + str(i)
                if rcol in df.columns:
                    new_df[column] = new_df[column].astype(str) + ',' + df[rcol].astype(str)
                else:
                    break
        else:
            new_df[column] = ""

    # 새로운 CSV 파일로 저장
    new_df.to_csv(args.output_csv, encoding=args.oenc, index=False, header=(not args.noheader), quoting=csv.QUOTE_ALL)

if __name__ == "__main__":
    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(description='CSV Extractor.')
    parser.add_argument('input_csv', help='Input CSV file name')
    parser.add_argument('column_list_csv', help='column_list_csv CSV file name')
    parser.add_argument('output_csv', help='output_csv CSV file name')
    parser.add_argument('--ienc', help='Output file name', default='utf-8')
    parser.add_argument('--oenc', help='Output file name', default='utf-8')
    parser.add_argument('-n', '--noheader', help='Output file Header', action='store_true', default=False)

    args = parser.parse_args()

    input_csv = sys.argv[1]
    column_list_csv = sys.argv[2]
    output_csv = sys.argv[3]

    extract_columns_to_new_csv(args)