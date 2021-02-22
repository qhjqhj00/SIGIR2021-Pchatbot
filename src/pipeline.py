import os
import argparse
from split_user import Split
from  data_byusers_generator import  Generator
def set_args():
    """
    Sets up the training arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_fp', default='../data/sample.txt', type=str, required=False, help='source data directory')
    parser.add_argument('--user_data_dir', default='../data/sample_byuser_filter', type=str, required=False, help='user data directory')
    parser.add_argument('--model_data_dir', default='../data/sample_datasets', type=str, required=False, help='model data directory')
    return parser.parse_args()
    
def main():
    args = set_args()
    # split data to user file
    s = Split(args)
    s.split_data()
    # use user data to generate train/dev/test
    g = Generator(args)
    g.generate()
if __name__ == '__main__':
    main()