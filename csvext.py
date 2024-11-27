import argparse
import csv
import glob

import pandas as pd


def extract_columns_to_new_csv(param: object):
    # 컬럼 목록 CSV 파일 읽기
    columns = pd.read_csv(param.columns, encoding=param.ienc, header=None).values.tolist()[0]
    write_mode = 'w'
    print_head = not param.noheader
    oencoding = param.oenc

    for filename in param.files:
        # 입력 CSV 파일 읽기
        df = pd.read_csv(filename, encoding=param.ienc, dtype=str)
        df.fillna('', inplace=True)

        # 지정된 컬럼 추출 및 병합
        new_df = pd.DataFrame()
        for column in columns:
            if column in df.columns:
                new_df[column] = df[column]

                for i in range(1,100):
                    rcol = column if i == 0 else column + "." + str(i)
                    if rcol in df.columns:
                        new_df[column] = new_df[column].astype(str) + ',' + df[rcol].astype(str)
                    else:
                        break
                if i > 1: new_df[column] = new_df[column].str.rstrip(',')
            else:
                new_df[column] = ""

        # 새로운 CSV 파일로 저장
        new_df.to_csv(param.output, mode=write_mode, encoding=param.oenc, index=False, header=print_head, quoting=csv.QUOTE_ALL)
        write_mode = 'a'
        print_head = False
        if oencoding == 'utf-8-sig': oencoding = 'utf-8'

if __name__ == "__main__":
    # ArgumentParser 객체 생성
    parser = argparse.ArgumentParser(prog='csvext', description='CSV Extractor.')
    parser.add_argument('-c', '--columns', metavar='column_csv_filename', required=True, help='columns csv file name')
    parser.add_argument('-o', '--output', metavar='output_filename', required=True, help='output csv file name')
    parser.add_argument('--ienc', metavar='input_encoding', help='input encoding (default utf-8)', default='utf-8')
    parser.add_argument('--oenc', metavar='output_encoding', help='output encoding (default utf-8-sig)', default='utf-8-sig')
    parser.add_argument('-n', '--noheader', help='no print csv header', action='store_true', default=False)
    parser.add_argument('files', nargs='+', help='Input csv file name')

    args = parser.parse_args()

    rfiles = []
    for file in args.files:
        rfiles.extend(sorted(glob.glob(file)))

    args.files = rfiles

    extract_columns_to_new_csv(args)