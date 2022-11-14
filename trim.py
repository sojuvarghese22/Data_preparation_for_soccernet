





from argparse import ArgumentParser
import os
from time import time
from tqdm import tqdm

import json
import subprocess as sp
import shlex
import json
import json
import shutil
import math 
from datetime import datetime, date, timedelta, time

def access_json(path):
    
    with open(path) as f:
        data = json.load(f)

    bitrate = str(data["format"]["bit_rate"])
    b = (len(bitrate)-3)
    bitrate = int(bitrate[:b])
    bitrate = bitrate/1000

    
    return bitrate

# def frame_rate(path):
    
#     with open(path) as f:
#         data = json.load(f)

#     framerate = data['streams'][0]['r_frame_rate'].split('/')[0]
#     framerate = int(framerate)

    
#     return framerate


def frame_rate(path):
    print("fhhfhfhk", path)
    with open(path) as f:
        data = json.load(f)
    print("fffffffff")
    framerate = data['streams'][0]['r_frame_rate'].split('/')[0]
    framerate = int(framerate)

    return framerate

# def start_and_end_frame(timestamp):
#     min,sec = timestamp.split(':')
#     min,sec = int(min),int(sec)
#     converted_min_to_sec = min*60
#     add_converted_min_to_sec_with_sec = converted_min_to_sec + sec
    
#     totalframe = add_converted_min_to_sec_with_sec * 25

#     return totalframe

# def exact_frame_no(timestamp):
#     min,sec = timestamp.split(':')
#     min,sec = int(min),int(sec)
#     converted_min_to_sec = min*60
#     add_converted_min_to_sec_with_sec = converted_min_to_sec + sec
    
# def frame_rate(path):
#     with open(path) as f:
#     data = json.load(f)

#     framerate = data['streams'][0]['r_frame_rate'].split('/')[0]
#     framerate = int(framerate)

#     return framerate

# def start_and_end_frame(timestamp):
#     min,sec = timestamp.split(':')
#     min,sec = int(min),int(sec)
#     converted_min_to_sec = min*60
#     add_converted_min_to_sec_with_sec = converted_min_to_sec + sec
#     totalframe = add_converted_min_to_sec_with_sec * 25

#     return totalframe

def exact_frame_no(timestamp,path_of_json_file__created,span): 
    print("thisssssssssssssssssss",timestamp, span)
    min,sec = timestamp.split(':')
    min,sec = int(min),int(sec)
    converted_min_to_sec = min*60
    add_converted_min_to_sec_with_sec = converted_min_to_sec + sec
    print("ddddddddddddddddddddsssssssssssssssssssssssss",add_converted_min_to_sec_with_sec)
    framerate = frame_rate(path_of_json_file__created)
    print("framerate",framerate)
    total_frame_corresponding_to_timestamp = add_converted_min_to_sec_with_sec * framerate
    print("total_frame_corresponding_to_timestamp",total_frame_corresponding_to_timestamp) 
    total_seconds_with_span = add_converted_min_to_sec_with_sec + span
    print("total_seconds_with_span",total_seconds_with_span)
    total_frame_corresponding_to_timestamp_with_span = total_seconds_with_span * framerate
    print("total_frame_corresponding_to_timestamp_with_span",total_frame_corresponding_to_timestamp_with_span)
    return (total_frame_corresponding_to_timestamp,total_frame_corresponding_to_timestamp_with_span)



def get_clip_start_end(start_time, span):
    print("start___________________________________time",start_time)
    mins, secs = list(map(int, start_time.split(":")))
    print("minsmins",mins)
    print("secs",secs)
    
    end_mins=mins
    end_secs = secs+span
    print("end_secsend_secs",end_secs)
    if end_secs > 59:
        end_secs = end_secs - 59
        end_mins = mins + 1

    start_mins=mins
    start_secs = secs-1
    if start_secs < 0:
        start_secs = start_secs+60
        start_mins = mins - 1
    
    start_mins = str(start_mins).zfill(2)
    start_secs = str(start_secs).zfill(2)
    end_mins = str(end_mins).zfill(2)
    end_secs = str(end_secs).zfill(2)
    print("start_mins",start_mins)
    
    print("start_secs",start_secs)

    print("end_mins",end_mins)
    print("end_secs",end_secs)
    return ("{}:{}".format(start_mins, start_secs), "{}:{}".format(end_mins, end_secs))


def main(args):
    dictionary_for_event_name = {'Corner':'cr','Throw-in':'th','Yellow card':'yc','Red card':'rc','Substitution':'sub'}
    # Input path
    matches_dir_path = os.path.abspath(os.path.join(os.getcwd(), args.in_dir))
    print( matches_dir_path)
    for premier_league in os.listdir(matches_dir_path):



    #list_of_matches = os.listdir(matches_dir_path)
        current_wor_dir = os.getcwd()
    # Store all clips in this directory 
        
        if not os.path.isdir(args.out_dir):
            os.mkdir(args.out_dir)
        out_dir_path = os.path.abspath(os.path.join(os.getcwd(), args.out_dir))
        print("out_dir_path",out_dir_path)
        # path_till_premier_league_for_processed_videos = os.path.join(args.out_dir,premier_league)
        # print("path_till_premier_league_for_processed_videos",path_till_premier_league_for_processed_videos)
        # if not os.path.isdir(path_till_premier_league_for_processed_videos):
        #     os.mkdir(path_till_premier_league_for_processed_videos)
      
        path_till_premier_league = os.path.join(matches_dir_path, premier_league)
        print("path_till_premier_league",path_till_premier_league)
        for match_dir in tqdm(os.listdir(path_till_premier_league)):
            print("match_dir",match_dir)
            #- INPUT  --
            # single match - input path
            match_dir_path = os.path.abspath(os.path.join(path_till_premier_league, match_dir))
            print("match_dir_path",match_dir_path)
            # match_dir_split = match_dir.split(" ")
            # updated_match_dir = "\ ".join(match_dir_split)

            # single match - videos 
            match_first_half_video_path = os.path.join(match_dir_path, "1_720p.mkv")
            match_second_half_video_path = os.path.join(match_dir_path, "2_720p.mkv")
            print("match_first_half_video_path",match_first_half_video_path)
            print("match_first_half_video_path",match_second_half_video_path)
            # single match labels
            try: 
                with open(os.path.join(match_dir_path, "Labels-v2.json"), "r") as json_file:
                    labels = json.load(json_file)
                    annotations = labels["annotations"]

            except:
                continue
            #print("labelslabelslabels",labels)    
            #- OUTPUT  --
            # single match - extracted clips path 
            out_premier_league_path = os.path.join(out_dir_path, premier_league)   
            print("out_match_path",out_premier_league_path)
            if not os.path.isdir(out_premier_league_path):
                os.mkdir(out_premier_league_path)
            out_match_path = os.path.join(out_premier_league_path, match_dir)   
            #print("out_match_path",out_matchbit_rate_for_created_json = frame_rate(path_of_json_file__created)athout_match_path",out_match_path)
            ######source_json_file_path = os.path.join(match_dir_path, "Labels-v2.json")
            print("out_match_pathout_match_pathout_match_pathout_match_path",out_match_path)
            #shutil.copyfile(original, target)
            #shutil.copyfile(source_json_file_path, destination_path_for_json_file)
            #shutil.copy(source_json_file_path, out_match_path)
            if not os.path.isdir(out_match_path):
                os.mkdir(out_match_path)
            # single match - action paths
            command_match_first_half_path = "\ ".join(match_first_half_video_path.split(" "))
            print("command_match_first_half_path",command_match_first_half_path)
            command_match_second_half_path = "\ ".join(match_second_half_video_path.split(" "))
            print("command_match_second_half_path",command_match_second_half_path)
                        
            

                        
            for action in tqdm(args.actions):
                count=1
                action_clips_path = os.path.join(out_match_path, action)
                print("action_clips_path",action_clips_path)
                if not os.path.isdir(action_clips_path):
                    print("yuyu")
                    os.mkdir(action_clips_path)

                for annotation in annotations:
                    action_label = annotation["label"]
                    action_gametime = annotation["gameTime"]
                    action_visibility = annotation["visibility"]

                    half_time, _, time_stamp = action_gametime.split(" ")
                    print("......................................................................................")
                    print("half_time",half_time)
                    print("time_stamp",time_stamp)
                    if action == action_label and action_visibility == "visible":
                        if action == 'Substitution':
                            action_clip_path = os.path.join(action_clips_path, "{}_{}_{}-{}.mp4".format(dictionary_for_event_name[action],half_time,time_stamp.split(':')[0],time_stamp.split(':')[1]))
                            print("action_clip_path",action_clip_path)
                            
                            
                            start, end = get_clip_start_end(time_stamp, 2)
                            print("startstartstart",start)
                            print("endendend",end)
                            clip_start = start
                            # min,sec = time_stamp.split(':')
                            # min,sec  = int(min),int(sec)
                            min,sec = clip_start.split(':')
                            min_and_sec = datetime(2000,3,12,00,int(min),int(sec))
                            complete_time_with_time = min_and_sec + timedelta(seconds=2)
                            
                            a = str(complete_time_with_time).split(' ')[1].split(':')[0:2]
                            b = ':'.join(a)
                            
                            if b == '00:00':
                                # print("bdskjbfjkdsbfkjbdsbjfbsjk")
                                # print("rrrrrrrrrrrrrrrrrrrrrrrr",str(complete_time_with_time).split(' ')[1])
                                clip_end = str(complete_time_with_time).split(' ')[1].split('00:')[-1]
                            else:

                                clip_end = str(complete_time_with_time).split(' ')[1].split('00:')[1]
                            
                            json_data = labels
                            annotation_json = json_data['annotations']
                            for annotation in annotation_json:
                                if action_gametime == annotation['gameTime']:
                                    annotation['clip_start_end'] = [clip_start,clip_end]
                                    break
                            
                            #print("labelslabelslabels",labels)
                            
                            if half_time == "1":
                                output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames = os.path.join(os.getcwd(),'start_end_time_and_corresponding_frames')
                                os.system("ffprobe -v quiet -print_format json -show_format -show_streams {} > {}.json".format(command_match_first_half_path,output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames))
                                path_of_json_file__created = output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames + '.json'
                                #start_and_end_frame(clip_start,path_of_json_file__created)
                                startFrame, endFrame = exact_frame_no(clip_start,path_of_json_file__created,2)
                                
                                #print("herehererererreerereretereteretereret", startFrame, endFrame)
                                
                            
                            if half_time == "2":
                                output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames = os.path.join(os.getcwd(),'start_end_time_and_corresponding_frames')
                                os.system("ffprobe -v quiet -print_format json -show_format -show_streams {} > {}.json".format(command_match_second_half_path,output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames))
                                path_of_json_file__created = output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames + '.json'
                                print("DDDDDDDDDDDDDDDDDDDDDDDDDD",path_of_json_file__created)
                                print(clip_start,"clip_start")
                                startFrame, endFrame = exact_frame_no(clip_start,path_of_json_file__created,2)

                            json_data = labels
                            annotation_json = json_data['annotations']
                            for annotation in annotation_json:
                                if action_gametime == annotation['gameTime']:
                                    annotation['clip_start_end'] = [clip_start,clip_end]
                                    annotation['clip_start_end_frame'] = [startFrame, endFrame]
                                    break
                            
                                #print("herehererererreerereretereteretereret", startFrame, endFrame)
                                
     
                            
                            
                            
                            
                                # clip_end = str(complete_time_with_time).split(' ')[1].split('00:')[1]
                                # clip_end = end
                            # print("clip_start",clip_start)
                            # print("clip_end",clip_end)
                            #t = datetime(2000, 2, 13,0,5,5)command_match_first_half_path

                            # print("befor_action_clips_path",action_clips_path)
                            # print("action",action)
                            # print("action_label",action_label)
                            # print("action_gametime",action_gametime) 
                            # print("time_stamp",time_stamp)
                        else:





                            action_clip_path = os.path.join(action_clips_path, "{}_{}_{}-{}.mp4".format(dictionary_for_event_name[action],half_time,time_stamp.split(':')[0],time_stamp.split(':')[1]))
                            print("action_clip_path",action_clip_path)

                            # print(t)  # 👉️ 09:30:13
                            # print(t- timedelta(seconds=4))
                            
                            start, end = get_clip_start_end(time_stamp, 3)
                            clip_start = start
                            # min,sec = time_stamp.split(':')
                            # min,sec  = int(min),int(sec)
                            min,sec = clip_start.split(':')
                            print("min,secmin,secmin,sec",min,sec)
                            min_and_sec = datetime(2000,3,12,00,int(min),int(sec))
                            print("min_and_secmin_and_secmin_and_sec",min_and_sec)
                            complete_time_with_time = min_and_sec + timedelta(seconds=3)
                            print("complete_time_with_timecomplete_time_with_time",complete_time_with_time)
                            
                            a = str(complete_time_with_time).split(' ')[1].split(':')[0:2]
                            b = ':'.join(a)
                            
                            if b == '00:00':
                                # print("bdskjbfjkdsbfkjbdsbjfbsjk")
                                # print("rrrrrrrrrrrrrrrrrrrrrrrr",str(complete_time_with_time).split(' ')[1])
                                clip_end = str(complete_time_with_time).split(' ')[1].split('00:')[-1]
                            else:

                                clip_end = str(complete_time_with_time).split(' ')[1].split('00:')[1]
                            
                            if half_time == "1":
                                output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames = os.path.join(os.getcwd(),'start_end_time_and_corresponding_frames')
                                os.system("ffprobe -v quiet -print_format json -show_format -show_streams {} > {}.json".format(command_match_first_half_path,output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames))
                                path_of_json_file__created = output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames + '.json'
                                #start_and_end_frame(clip_start,path_of_json_file__created)
                                startFrame, endFrame = exact_frame_no(clip_start,path_of_json_file__created,2)
                                
                                #print("herehererererreerereretereteretereret", startFrame, endFrame)
                                
                            
                            if half_time == "2":
                                output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames = os.path.join(os.getcwd(),'start_end_time_and_corresponding_frames')
                                os.system("ffprobe -v quiet -print_format json -show_format -show_streams {} > {}.json".format(command_match_second_half_path,output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames))
                                path_of_json_file__created = output_for_json_file_for_action_start_end_exact_time_and_corresponding_frames + '.json'
                                print("DDDDDDDDDDDDDDDDDDDDDDDDDD",path_of_json_file__created)
                                print(clip_start,"clip_start")
                                startFrame, endFrame = exact_frame_no(clip_start,path_of_json_file__created,2)

                            
                            
                            # print("clip_endclip_end",clip_end)
                            # print("onlyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",str(complete_time_with_time).split(' ')[1].split('00:'))
                            # print("onlyonlyonlyonlyonly",clip_end)
                            
                            # if "1 - 00:16" == action_gametime:
                            #     exit()
                            
                            # print("clip_endclip_end",clip_end)
                            # print("labelslabelslabels",labels)
                            
                            json_data = labels
                            annotation_json = json_data['annotations']
                            for annotation in annotation_json:
                                if action_gametime == annotation['gameTime']:
                                    annotation['clip_start_end'] = [clip_start,clip_end]
                                    annotation['clip_start_end_frame'] = [startFrame, endFrame]
                                    
                                    break

                                # clip_end = str(complete_time_with_time).split(' ')[1].split('00:')[1]
                                # clip_end = end
                            # print("clip_start",clip_start)
                            # print("clip_end",clip_end)
                            #t = datetime(2000, 2, 13,0,5,5)
                        
                        
                        ## if needed can remove below code 




                        # command_match_first_half_path = "\ ".join(match_first_half_video_path.split(" "))
                        # print("command_match_first_half_path",command_match_first_half_path)
                        # command_match_second_half_path = "\ ".join(match_second_half_video_path.split(" "))
                        # print("command_match_second_half_path",command_match_second_half_path)
                        
                        command_action_clip_path = "\ ".join(action_clip_path.split(" "))
                        print("command_action_clip_path",command_action_clip_path)
                        print("check this one")
                        
                        if half_time == "1":
                            path_for_json_file = os.path.join(current_wor_dir,'video')
                            print("path_for_json_file",path_for_json_file)
                            os.system("ffprobe -v quiet -print_format json -show_format -show_streams {} > {}.json".format(command_match_first_half_path,path_for_json_file))
                            
                            bit_rate = access_json('/home/soju/trim_video_vverse/video.json')
                            
                            os.system("ffmpeg -ss 00:{} -to 00:{} -i {}  -b:v {}M {}".format(start, end, command_match_first_half_path, bit_rate, command_action_clip_path))
                            
                            count+=1

                        elif half_time == "2":
                            

                            path_for_json_file = os.path.join(current_wor_dir,'video')
                            os.system("ffprobe -v quiet -print_format json -show_format -show_streams {} > {}.json".format(command_match_second_half_path,path_for_json_file))
                            
                            
                            bit_rate = access_json('/home/soju/trim_video_vverse/video.json')
                        
                            os.system("ffmpeg -ss 00:{} -to 00:{} -i {}  -b:v {}M  {}".format(start, end, command_match_second_half_path, bit_rate, command_action_clip_path))
                        
                            count+=1
            # print()
            # print()
            # print()
            # print()
            # print()
            # print()
            # print()
            # print("out_match_pathout_match_path",out_match_path)
            # print("Dddddd",)

            match_name_for_json_file = out_match_path.split('/')[-1]
            with open(os.path.join(out_match_path,match_name_for_json_file), "w") as outfile:
                json.dump(json_data, outfile) 
                     
            

def get_args(): 
    ap = ArgumentParser()
    ap.add_argument("--in_dir", help="Path to directory containing matches(each match - 1&2 halfs + Labels-v2.json", required=True)
    ap.add_argument("--actions", help="Give actions as list", default=["Corner", "Red card", "Yellow card", "Throw-in", "Substitution" ])
    
    ap.add_argument("--out_dir", help="Path to store action clips", default="trying4")
    args = ap.parse_args()

    return args


if __name__ == "__main__":
    args = get_args()

    main(args)























