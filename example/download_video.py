import os
import asyncio
import aiohttp
import pandas as pd
from tqdm import tqdm
import glob
import warnings
import argparse
import sys

from requests.models import PreparedRequest
from sty import fg

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

def get_basename(url):
    return os.path.basename(url)[:-13]+".mp4"

def get_csvs(csv_folder):
    return glob.glob(os.path.join(csv_folder, "*.csv"))

# define a function to download videos from a csv file asynchronously
def download_videos(csv_path, max_task = 4, write_path = "./videos"):
    # read the csv file into a dataframe
    df = pd.read_csv(csv_path)
    # fill the missing values in video_link and video_id columns with empty strings
    df['video_link'] = df['video_link'].fillna("")#.astype(str)
    df['video_id'] = df['video_id'].fillna("")#.astype(str)

    # filter the dataframe to keep only the rows that have valid video links and need to be downloaded
    # filtered_df = df.loc[(df["video_link"]!= "") & (df["if_video"])]
    filtered_df = df.loc[(df["video_link"]!= "") & (df["if_video"]) & (df["if_video_downloaded"] == False)]

    game_name = df.iloc[0]["game_name"]
    write_path = os.path.join(write_path, game_name)

    # create the output directory if it does not exist
    os.makedirs(write_path, exist_ok=True)
    
    # check if there are any videos to download
    if len(filtered_df)>0:
        # download the videos asyncioly using aiohttp and semaphore
        # limit the number of asyncio tasks by max_task parameter
        semaphore = asyncio.Semaphore(max_task)
        name_list = [(get_basename(filtered_df.iloc[i]["video_link"])) for i in range(len(filtered_df))]

        task = [asyncio.ensure_future(\
            async_download_from_url(semaphore, filtered_df.iloc[i]["video_link"], \
                os.path.join(write_path, name_list[i]), df, \
                filtered_df.index[i])) for i in range(len(name_list))]

        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(task))

        # save the updated dataframe back to the csv file 
        df.to_csv(csv_path, index=False)

# define an async function to download a file from a url and save it to a destination path
async def async_download_from_url(semaphore, url, dst, df, index):
    # use semaphore to limit the number of concurrent tasks
    async with semaphore:
        # create an aiohttp session
        async with aiohttp.ClientSession() as session:
            # send a request to the url and get the response
            req = await fetch(session, url, dst)

            # get the file size from the response header
            file_size = int(req.headers['content-length'])
            print(f"{get_basename(url)} 视频总长度: {file_size/1000000}M")
            
            # check if the destination file already exists
            if os.path.exists(dst):
                # get the size of the existing file
                first_byte = os.path.getsize(dst)
            else:
                # set the initial byte to zero
                first_byte = 0
                
            # check if the existing file size is equal or larger than the expected file size
            if first_byte >= file_size:
                # # Check if the downloaded file size matches the expected file size
                # if os.path.getsize(dst) == file_size:
                    # # Update the corresponding row in the dataframe to indicate that the video is downloaded
                    # df.at[index, 'if_video_downloaded'] = True
                    # print("File already downloaded.")

                df.at[index, 'if_video_downloaded'] = True
                print("File already downloaded.")
                
                # return the file size without downloading anything    
                return file_size
            
            # create a header with range parameter to resume downloading from where it left off 
            header = {"Range": f"bytes={first_byte}-{file_size}"}
            # create a progress bar to show the download status 
            pbar = tqdm(
                total=file_size, initial=first_byte,
                unit='B', unit_scale=True, desc=dst)
            
            # send another request with header and progress bar and save the response content to destination path 
            await fetch(session, url, dst, pbar=pbar, headers=header)
            # Update if_video_downloaded column to True in the corresponding row of the DataFrame after downloading is complete 
            df.at[index, 'if_video_downloaded'] = True

# define an async function to send a get request to a url and return the response or save the content to a file
async def fetch(session, url, dst, pbar=None, headers=None):
    # check if headers are provided
    if headers:
        # send a get request with headers
        async with session.get(url, headers=headers) as req:
            # open the destination file in append mode
            with(open(dst, 'ab')) as f:
                # loop until there is no more content to read
                while True:
                    # read 1024 bytes from the response content
                    chunk = await req.content.read(1024)
                    # check if the chunk is empty
                    if not chunk:
                        # break the loop
                        break
                    # write the chunk to the file 
                    f.write(chunk)
                    # update the progress bar by 1024 bytes 
                    pbar.set_description("Downloading file " + fg.yellow + get_basename(url) +  fg.rs )
                    pbar.update(1024)
            # close the progress bar after writing is done 
            pbar.close()
    else:
        # send a get request without headers 
        async with session.get(url) as req:
            # return the response object 
            return req

if __name__ == "__main__":
    print(f'yes,you start downloading')
    warnings.filterwarnings("ignore")

    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input_csv_folder", help="input csv folder", \
        default = "./game_summary/game_videos/output")
    argParser.add_argument("-o", "--output_video_folder", help="output video folder", \
        default = "./videos")
    args = argParser.parse_args()

    csv_folder = args.input_csv_folder
    video_folder = args.output_video_folder

    csvs = get_csvs(csv_folder)

    for csv in csvs[1000:]:
    # for csv in csvs:
        print("Current csv file: ", os.path.basename(csv))
        download_videos(csv, max_task = 8, write_path = video_folder)
    print(f'yes, you end downloading')