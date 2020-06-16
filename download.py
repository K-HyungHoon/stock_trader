import datetime
import argparse
from lib.utils import download

if __name__ == "__main__":
    today = datetime.datetime.now().strftime('%Y%m%d')

    # parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--window_size', type=int, default=10)
    parser.add_argument('--data_path', type=str, default="./data")
    parser.add_argument('--start_date', type=str, default=today)
    parser.add_argument('--end_date', type=str, default=today)
    args = parser.parse_args()

    print("Data Download...")

    download(args.data_path, args.start_date, args.end_date, args.window_size)