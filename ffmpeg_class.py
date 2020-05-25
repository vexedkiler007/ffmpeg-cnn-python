"""
a + b + c = how would that work?
a + b = creates a new class d

how is sum(a,b,c) related to a+b+c

ffmpeg -ss 30 -i input.wmv -c copy -t 10 output.wmv
"""
from typing import List
import subprocess
import os

n = 0


# creates different files for add operator don't judge me it was only way I found for add to work
def temp_file():
    global n
    n += 1
    return f"output{n}.MPG"


# deals with single video
class FfmpegVideo:
    """
    media_name = name of video file path
    name_all = wether or not to use entire video
    media_type = what video type
    media_time = what section of the video will be used
    media_output_path =

    """

    def __init__(self, media_absolute_path, media_name, media_all=True, media_time=None, media_output_path=None):
        self.media_absolute_path = media_absolute_path
        self.media_name: str = media_name
        self.media_all: bool = media_all
        self.media_time: List[int] = media_time
        self.media_output_path = media_output_path

    # combines one ffmpeg video with another a + b + c ....
    def __add__(self, other):
        output = temp_file()
        output_path = other.media_absolute_path

        if self.media_output_path is not None:
            output_path = self.media_output_path
        if other.media_output_path is not None:
            output_path = other.media_output_path

        command = f'ffmpeg -i "concat:{self.media_absolute_path}\\{self.media_name}|{other.media_absolute_path}\\{other.media_name}" -codec copy {output_path}\\{output}'
        print(command)
        subprocess.call(command)
        print("added")
        return FfmpegVideo(other.media_absolute_path, output)

    # changes video type any other video type "for the most part" if you need to use codec libx264 set to true
    def change_videotype(self, typevid: str, new_name: str, codec: bool = False, outputfile: str = None):

        outputfile = self.file_none_check(outputfile)

        command = f"ffmpeg  -i {self.media_absolute_path}\\{self.media_name} {self.media_absolute_path}\\{outputfile}.{typevid}"
        if typevid == "MPG" and codec:
            command = f"ffmpeg  -i {self.media_absolute_path}\\{self.media_name} -c:v libx264 -crf 18 {outputfile}\\{new_name}.{typevid}"
            print("cool")
        subprocess.call(command)

    # slices video from starttime and then !!!!slices end_time seconds!!!!
    def slice_video(self, typevid: str, new_name: str, end_time: int, start_time: int = 0, outputfile: str = None):

        outputfile = self.file_none_check(outputfile)

        if outputfile == None:
            outputfile = self.media_absolute_path
        command = f"ffmpeg -i {self.media_absolute_path}\\{self.media_name} -c copy -t {end_time} -ss {start_time}  {outputfile}\\{new_name}.{typevid}"
        print(command)
        subprocess.call(command)

    # takes screenshots of a file and puts it to specified folder
    def screenshot_video(self, outputfile: str = None, output_name = "out"):

        self.file_none_check(outputfile)

        command = f'ffmpeg -i "{self.media_absolute_path}//{self.media_name}"  "{outputfile}//{output_name}-%03d.jpg"'
        print(command)

        subprocess.call(command)


    def get_info(self):
        command = f"ffmpeg -i {self.media_absolute_path}/{self.media_name} -hide_banner"
        subprocess.call(command)


    #  checks if file  name exists
    def file_none_check(self, outputfile):
        if outputfile is None:
            outputfile = self.media_output_path
            if outputfile is None:
                outputfile = self.media_absolute_path
        return outputfile


# Deals with all videos in an entire folder
class FfmpegBulk(FfmpegVideo):

    def __init__(self, media_absolute_path, media_output_path, media_namelist=None, media_name=None):
        super().__init__(media_absolute_path, media_name=None)
        self.media_namelist: List[str] = media_namelist
        self.media_output_path = media_output_path
        self.media_name = media_name

    def __repr__(self):
        a = os.listdir(self.media_absolute_path)
        print(a)
        return str(a)

    def create_namelist(self):
        self.media_namelist = os.listdir(self.media_absolute_path)
        return self.media_namelist

    # id is used to identify which video batch to avoid overwrite
    # [id]output[video number in batch] - [picture number in video number]
    def screenshot_all_videos(self, id = "00", single_file = True):
        print("Make sure id is different to avoid overwrite!")
        print("Continue [y]")
        if input() is "y":
            if single_file:
                filename = f"{id}_all_batchvids"
                path = f"output_data/screenshots/{filename}"
                os.mkdir(path)
            for num, i in enumerate(self.media_namelist):
                print(i)
                self.media_name = i

                if not single_file:
                    filename = f"{id}screenshot{num}"
                    path = f"output_data/screenshots/{filename}"
                    os.mkdir(path)

                self.screenshot_video(outputfile=f"output_data/screenshots/{filename}", output_name=f"{id}output{num}")

    # Time format "00:00:00.00"
    # end_time can go over to encapsulate the entire video
    # typevid does not include "." , works with MOST video types
    def slice_all_videos(self, typevid, name_file, end_time, start_time = 0):
        for num, i in enumerate(self.media_namelist):
            name_file_temp = f"{name_file}{num}"
            self.media_name = i
            self.slice_video(typevid, name_file_temp, end_time=end_time, outputfile="output_data/slice_video", start_time=start_time)



