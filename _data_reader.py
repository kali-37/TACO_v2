import json 
import os
# import argparse




if __name__=='__main__':
    # parser= argparse.ArgumentParser()
    # parser.add_argument('--data', type=str, default=None)
    # args= parser.parse_args()
    # if args.data:
        # with open(args.data) as f:
            # data = json.load(f)
    _path0:str=os.path.dirname(os.path.abspath(__file__))
    _path='data/annotations.json'
    # get it's absolute path
    _path: str=os.path.join(_path0,_path)
    with open(file=_path,mode='r') as f:
        data = json.load(fp=f)
        print("HI")