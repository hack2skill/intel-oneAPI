
#!/usr/bin/env python
# coding=utf-8
# Copyright 2023 C5ailabs Team (Authors: Rohit Sroch) All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Preprocess course video subtitle (.vtt) file.
"""
import argparse
import os
import webvtt
from glob import glob

def preprocess_subtitle_vtt(subtitle_fpath, min_text_len=20):
    subtitles = webvtt.read(subtitle_fpath)

    preprocessed_subtitles = []
    current_subtitle = ""
    current_start = ""

    for subtitle in subtitles:
        subtitle_text = " ".join(subtitle.text.strip().split("\n")).strip()
        current_subtitle += subtitle_text + " "

        if len(current_subtitle) >= min_text_len:
            preprocessed_subtitles.append(webvtt.Caption(current_start, subtitle.end, text=current_subtitle.strip()))
            current_subtitle = ""
            current_start = ""
        elif not current_start:
            current_start = subtitle.start

    if current_subtitle:
        preprocessed_subtitles.append(webvtt.Caption(current_start, subtitle.end, text=current_subtitle.strip()))

    psubtitle = webvtt.WebVTT()
    psubtitle.captions.extend(preprocessed_subtitles)

    return psubtitle


def main(args):
    
    # format of courses folder structure is courses/{topic_name}/Study-Material/{week_name}/{subtopic_name}/subtitle-en.vtt
    path = os.path.join(args.course_dir, "*/Study-Material/*/*/*.vtt")
    subtitle_fpaths = glob(path)
    
    for subtitle_fpath in subtitle_fpaths:
        print("*"*100)
        print("Preprocess subtitle: {}".format(subtitle_fpath))
        psubtitle = preprocess_subtitle_vtt(
            subtitle_fpath, args.min_text_len)
        
        psubtitle_fpath = subtitle_fpath.replace(
            ".vtt", "-processed.vtt")
        #psubtitle_fpath = subtitle_fpath
        psubtitle.save(psubtitle_fpath)
        print("\n")
   

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Preprocess course video subtitle (.vtt) file")
    
    parser.add_argument(
        "--course_dir",
        type=str,
        help="base directory containing courses",
        default="../../dataset/courses"
    )
    parser.add_argument(
        "--min_text_len",
        type=int,
        default=500,
        help="Minimum length of each subtitle text (in chars)"
    )
    
    args = parser.parse_args()

    main(args)