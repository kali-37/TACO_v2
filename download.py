'''
This script downloads TACO's images from Flickr given an annotation json file
Code written by Pedro F. Proenza, 2019
'''

import os.path
import argparse
import json
from PIL import Image
import requests
from io import BytesIO
import sys
import asyncio 
import aiohttp


async def writes_(content,file_path,i,nr_images):
    img =Image.open(BytesIO(content))
    if img._getexif():
        img.save(file_path, exif=img.info["exif"])
    else:
        img.save(file_path)
    bar_size = 30
    x = int(bar_size * i / nr_images)
    sys.stdout.write("%s[%s%s] - %i/%i\r" % ('Loading: ', "=" * x, "." * (bar_size - x), i, nr_images))
    sys.stdout.flush()
    i+=1



async def write_image(file_path,_all_data,i,nr_images) -> None:
    print(f'{i}/{nr_images}')
    for response in _all_data:
        content=await response.read()
        await  writes_(content=content,file_path=file_path,i=i,nr_images=nr_images)

async def main() -> None:
    tasks=[]
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--dataset_path', required=False, default= './data/annotations.json', help='Path to annotations')
    args = parser.parse_args()
    dataset_dir = os.path.dirname(args.dataset_path)

    async with aiohttp.ClientSession() as session:
        with open(args.dataset_path, 'r') as f:
            annotations = json.loads(f.read())
            nr_images = len(annotations['images'])
            for i in range(nr_images):

                image = annotations['images'][i]

                file_name = image['file_name']
                url_original = image['flickr_url']
                url_resized = image['flickr_640_url']

                file_path = os.path.join(dataset_dir, file_name)

                # Create subdir if necessary
                subdir = os.path.dirname(file_path)
                if not os.path.isdir(subdir):
                    os.mkdir(subdir)

                if not os.path.isfile(file_path):
                    # Load and Save Image
                    # response = requests.get(url_original)
                    print("Fetching for ...",url_original)
                    task=asyncio.create_task(session.get(url_original))
                    tasks.append(task)
                    if len(tasks)>=20:
                        _all_data=await asyncio.gather(*tasks)
                        await write_image(file_path,_all_data,i,nr_images)
                        tasks.clear()

            _all_data=await asyncio.gather(*tasks)
            await write_image(file_path,_all_data,i,nr_images)
            sys.stdout.write('Finished\n')

asyncio.run(main())













# '''
# This script downloads TACO's images from Flickr given an annotation json file
# Code written by Pedro F. Proenza, 2019
# '''

# from pydantic import BaseModel
# import os.path
# import json
# from typing import Any# type:ignore[reportAny]
# from PIL import Image
# import requests
# from io import BytesIO
# import sys

# from threading import Thread


# FILE_NAME = './data/annotations.json'

# dataset_dir = os.path.dirname(FILE_NAME)

# class ImageData(BaseModel):

#     id:int 
#     width:int
#     height: int
#     file_name: str
#     license: None|Any
#     flickr_url: str
#     coco_url: None|Any
#     date_captured: None|Any
#     flickr_640_url: None|str

# class Data(BaseModel):
#     info:dict[str,Any]
#     images:list[ImageData]
#     annotations:list[dict[str,Any]]
#     scene_annotations:list[dict[str,Any]]
#     licenses:list[Any]
#     categories:list[dict[str,Any]]
#     scene_categories:list[dict[str,Any]]



# def download(index:int,all_data:Data):
#     image = all_data.images[index]

#     file_name = image.file_name
#     url_original = image.flickr_url
#     url_resized = image.flickr_640_url

#     file_path = os.path.join(dataset_dir, file_name)

#     # Create subdir if necessary
#     subdir = os.path.dirname(file_path)
#     if not os.path.isdir(subdir):
#         os.mkdir(subdir)

#     if not os.path.isfile(file_path):
#         # Load and Save Image
#         response = requests.get(url_original)
#         img = Image.open(BytesIO(response.content)) # type:ignore[reportUnknownMemberType]
#         if img.getexif():
#             img.save(file_path, exif=img.info["exif"])# type:ignore[reportUnknownMemberType]
#         else:
#             img.save(file_path) # type:ignore[reportUnknownMemberType]

#     # Show loading bar
#     bar_size = 30
#     x = int(bar_size * index / nr_images)
#     _ = sys.stdout.write("%s[%s%s] - %i/%i\r" % ('Loading: ', "=" * x, "." * (bar_size - x), index, nr_images))
#     sys.stdout.flush()




# # Load annotations
# with open(FILE_NAME, 'r') as f:
#     all_data:Data = Data(**json.loads(f.read()))# type:ignore[reportAny]


# nr_images = len(all_data.images)
# ths:list[Thread] = []
# for index in range(nr_images):
#     print(f"{index} downlaoding... ")
#     t = Thread(target=download,args=(index,all_data))
#     t.start()
#     ths.append(t)

# for t in ths:
#     t.join()
# _  = sys.stdout.write('Finished\n')