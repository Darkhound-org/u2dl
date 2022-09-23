# Copyright 2022 Darkhound-org

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# u2dl - youtube downloader 
# version - 2022.09.21

try:
    # Importing all necessary libraries
    import pytube
    import click
    import os
    from ffmpeg_progress_yield import FfmpegProgress
    import sys
    from art import *
    import time
    import contextlib
    from pathlib import Path
    import urllib.request
    import webbrowser
    from rich.console import Console
    import subprocess
    from pytube import YouTube
    from halo import Halo
    from rich.live import Live
    from tqdm import tqdm
    from pytube import Playlist
except ImportError:
    print('\n[ERROR] Failed importing modules. Make sure the venv is activated or try running ''pip install recquirements.txt''')    

def lazy(str,delay): # types any str slowly. Speed can be changed using the delay ->float 
    ''' Prints text slowly '''
    for letter in str + '\n':
            sys.stdout.write(letter)
            sys.stdout.flush()
            time.sleep(delay)     

cwd = os.getcwd() # Current working dir . Path to the folder where the script is located
console = Console()

@click.version_option('2022.09.21',prog_name='u2dl' ) # version flag

@click.group(invoke_without_command=True, no_args_is_help=True) 
@click.option('--license','-li',is_flag=True,help='A brief info about the project license')
@click.option('--docs','-d',is_flag=True,help='Opens the documentation [in your browser]')
@click.option('--ffmpeg','-f',is_flag=True,help='Get ffmpeg.exe')
@click.option('--dev','--developer',is_flag=True,help='A brief info about the developer')
def cli(license,docs,dev,ffmpeg):
    '''
    u2dl - Terminal youtube video downloader\n
    Home page: https://darkhound-org.github.io/u2dl/\n
    Github: https://github.com/Darkhound-org/u2dl

    '''
    if license:

        print('''

Copyright 2022 Darkhound-org
SPDX-License-Identifier: Apache-2.0  
    
    ''')
    elif docs:
        print('\n[view(v) / exit(e)] Enter v to read the documentation [default: v]')
        doc = ''
        while doc != 'e':
            doc = input(' > ')
            if doc == 'v':
                print('Viewing Docs...') 
                time.sleep(0.3)
                webbrowser.open('https://darkhound-org.github.io/u2dl/') 
                break
            elif doc == 'e':
                break
            elif doc == '':
                print('Viewing Docs...')
                time.sleep(0.3)
                webbrowser.open('https://darkhound-org.github.io/u2dl/')
                break    

    elif dev:
        developer = 'Darkhound-org'
        print('\n\t\t\tWe '+'Love'+' CLI')
        
        print('''

        Darkhound-org develops applications [games too..] programmed in different languages [python,golang,lua..etc]

        Website: https://darkhound-org.github.io/
        Github o(^•x•^)o : https://github.com/darkhound-org
        Member(s) : Scott Lang

        ''') 
    elif ffmpeg:
        # For downloading Ffmpeg builds
        print('Get Ffmpeg build from BtbN or get ffmpeg.exe only [get_builds(gb) / get_now(gn) / e(exit)][default : get_now(gn)]')
        fc = ''
        while fc != 'e':
            fc = input(' > ')
            if fc.lower() == 'gb':
                print('[INFO] Opening https://github.com/BtbN/FFmpeg-Builds/releases in your default browser... ')
                time.sleep(0.2)
                webbrowser.open('https://github.com/BtbN/FFmpeg-Builds/releases')
            elif fc.lower() == 'gn':
                print('[INFO] Downloading ffmpeg.exe... [source : https://github.com/Darkhound-org/Glixxko/releases/download/071039/ffmpeg.exe]')    
                spinner = Halo(text='\nDownloading...  ', spinner='dots')
                spinner.start()
                urllib.request.urlretrieve("https://github.com/Darkhound-org/Glixxko/releases/download/071039/ffmpeg.exe", 'ffmpeg.exe')
                spinner.stop()
                print('\n[INFO] ffmpeg.exe in '+cwd)
            elif fc == '':
                print('[INFO] Downloading ffmpeg.exe... [source : https://github.com/Darkhound-org/Glixxko/releases/download/071039/ffmpeg.exe]')    
                spinner = Halo(text='\nDownloading...  ', spinner='dots')
                spinner.start()
                urllib.request.urlretrieve("https://github.com/Darkhound-org/Glixxko/releases/download/071039/ffmpeg.exe",'ffmpeg.exe')
                spinner.stop()
                print('\n[INFO] ffmpeg.exe in '+cwd)
            elif fc.lower() == 'e':
                break

            else:
                print('\n'+fc+' is not a valid command. Enter a valid command [ gb / gn / e [default: gn] ]')



@click.command(help='''

Download single videos and playlists from Youtube

Syntax: u2dl get -l(or)-p(or)i <link> -s <path> -a(flag not valid for playlists and info) 

[Note] : When converting make sure the downloaded file is in the working directory. Ffmpeg recquired for conversion.\n
[Note] : You can place Ffmpeg in the working directory or add to environment path variable.
    ''')
@click.option('--link','-l',help='Takes the Youtube url')
@click.option('--playlist','-p',help='Takes the playlist url')
@click.option('--audio','-a',is_flag=True,help='Convert to high quality mp3 format.\n[Note] : Ffmpeg recquired for conversion. Read docs for more details.')
@click.option('--save_to','-s',help='Takes the download location [path]')
@click.option('--info','-i',help='Display all available information about a Youtube video')
def get(link,audio,save_to,playlist,info):
    # Download single videos and playlists from Youtube 

    if playlist:
            pl = Playlist(playlist)
            print('\n[see(display all urls in the playlist) / d(downloads all urls in the playlist) / e(exit) / help(h)(show this message)] Enter see / d / e / h [default: see]')
            pl_ch = ''
            while pl_ch != 'e':
                pl_ch = input(' > ')
                if pl_ch.lower() == 'see':
                    print('\n\t',pl.title)
                    for urls in pl.video_urls:
                        with Live(refresh_per_second=1):
                            print(urls)
                elif pl_ch.lower() == 'd':
                    print('\nPlaylist name: '+pl.title)
                    print('\n[INFO] Downoading highest resolution of videos from the given playlist')
                    print('\n[DEBUG] Downloading may take longer than expected . There may be a delay after processing.')
                    spinner = Halo(text='\nProcessing...  ', spinner='dots')
                    if audio:    
                        print('\n[INFO] --audio(-a) flag not valid for playlists.') # If the user accidentally inputs -a flag
                    else:
                        pass
                    spinner.start()
                    for vd in pl.videos:
                        time.sleep(0.6)
                        spinner.stop()
                        if save_to:

                            for i in tqdm(range(1000),desc='Downloading...'):
                            

                                vd.streams.get_highest_resolution().download(save_to) #save_to -> path
                                pass
                                
                        else: 
                            for i in tqdm(range(1000),desc='Downloading...'):
                            

                                vd.streams.get_highest_resolution().download()
                                pass
                                
                         
                elif pl_ch.lower() == 'e':
                    break
                elif pl_ch == '':
                    print('\n\t',pl.title)
                    for urls in pl.video_urls:
                        with Live(refresh_per_second=1):
                            print(urls)
                elif pl_ch.lower() == 'h':
                    print('\n[see(display all urls in the playlist) / d(downloads all urls in the playlist) / e(exit) / help(h)(show this message)] Enter see / d / e / h [default: see]')
                elif pl_ch.lower() == 'help':
                    print('\n[see(display all urls in the playlist) / d(downloads all urls in the playlist) / e(exit) / help(h)(show this message)] Enter see / d / e / h [default: see]')  
                else:
                    print('\n'+pl_ch+' is not a valid command. Enter a valid command [ see / d / e / h [default: see] ]')
    
    elif info:
        it = YouTube(info)
        if audio:
            print('\n[INFO] --audio(-a) flag not valid for info option.') # If the user accidentally inputs -a flag
        else:
            pass    
        print('Title: '+it.title)
        print('URL: '+it.embed_url)
        print('Thumbnail url: '+it.thumbnail_url)
        print('Length: '+str(it.length))
        print('Published date: '+str(it.publish_date))
        print('Channel url: '+it.channel_url)
        print('\n[v(view the description of the video in terminal) / s(save description to a file) / e(exit) / help(h)(show this message)] Enter v / s / e / h [default : s]')
        desc_ch = ''
        while desc_ch != 'e':
            desc_ch = input(' > ')
            if desc_ch.lower() == 'v':
                print('\nDesciption: ')
                print(it.description)
            elif desc_ch.lower() == 's':
                try:

                    with open('desc.txt','w',encoding="utf-8") as f:
                        with contextlib.redirect_stdout(f):
                            print('\nDesciption: ')
                            print(it.description)
                    print('[INFO] Description saved to '+cwd+'\desc.txt')  
                except Exception:
                    print('[ERROR] Failed writing description ..!! ') 
            elif desc_ch == '':
                try:

                    with open('desc.txt','w',encoding="utf-8") as f:
                        with contextlib.redirect_stdout(f):
                            print('\nDesciption: ')
                            print(it.description)
                    print('[INFO] Description saved to '+cwd+'\desc.txt')  
                except Exception:
                    print('[ERROR] Failed writing description ..!! ')          
            elif desc_ch.lower() == 'help':
                print('\n[v(view the description of the video in terminal) / s(save description to a file) / e(exit) / help(h)(show this message)] Enter v / s / e / h [default : s]')
            elif desc_ch.lower() == 'h':
                print('\n[v(view the description of the video in terminal) / s(save description to a file) / e(exit) / help(h)(show this message)] Enter v / s / e / h [default : s]')
            elif desc_ch.lower() == 'e':
                break       
            else:
                print('\n'+desc_ch+' is not a valid command. Enter a valid command [ v / s / e / h [default: s] ]')


    else:

        try:   
            yt = YouTube(link)  
        except pytube.exceptions.AgeRestrictedError:    
            print('\n[WARNING] Video is age restricted, and cannot be accessed without OAuth.')
        except pytube.exceptions.ExtractError: 
            print('\n[ERROR] Failed extracting data')  
        except pytube.exceptions.HTMLParseError:                          # Handling exceptions
            print('\n[ERROR] HTML could not be parsed')     
        except pytube.exceptions.LiveStreamError:
            print('\n[WARNING] Cannot download a live streaming video')    
        except pytube.exceptions.MembersOnly:
            print('\n[WARNING] Video is members-only. YouTube has special videos that are only viewable to users who have subscribed to a content creator. ref: https://support.google.com/youtube/answer/7544492?hl=en')    
        except pytube.exceptions.VideoPrivate:
            print('\n[WARNING] Cannot access private videos')
        except pytube.exceptions.VideoRegionBlocked:
            print('\n[WARNING] Video blocked in your region')
        except pytube.exceptions.VideoUnavailable:
            print('\n[ERROR] Video unavailable. Check the url once more')
        else:    
            print('Title: '+yt.title)
            print('\nType/Format >','\t','Resolution >','\t','file size')
            spinner = Halo(text='\nProcessing...  ', spinner='dots')
            spinner.start()
            if audio:
                for lks in yt.streams:

                    print(str(lks.mime_type)+ ' > ' +str(lks.resolution) + ' > ' +str(lks.filesize/(1024*1024))+' MB')
                    spinner.stop()        
                print('\nCopy and paste the stream you want to download [ e(exit) / h(highest resolution) / help(show this message) ]')
                yt_ch = ''
                while yt_ch != 'e':
                    yt_ch = input(' > ')
                    if yt_ch.lower() == 'h':
                        print('\n[INFO] Downloading highest resolution of the given url : '+str(yt.streams.get_highest_resolution()))
                        if save_to:

                            for i in tqdm(range(1000),desc='Downloading...'):
                            

                                yt.streams.get_highest_resolution().download(save_to) #save_to -> path
                                pass
                        else: 
                            for i in tqdm(range(1000),desc='Downloading...'):
                            

                                yt.streams.get_highest_resolution().download()
                                pass   
                        try:

                            def_file_name = yt.streams.get_highest_resolution().default_filename
                            new_file_name = Path(yt.streams.get_highest_resolution().default_filename).stem+'.mp3'
                            cmd = [
                                "ffmpeg" , "-i" , def_file_name , new_file_name
                            ]   
                            ff = FfmpegProgress(cmd)
                            for progress in ff.run_command_with_progress():
                                txt_prog = '[ '+'Converting... > '+f"{progress} / 100"+' %'+' ]'
                                time.sleep(0.8)
                                print(txt_prog)
                        except FileNotFoundError:
                            ffpath = cwd+'\ffmpeg.exe'
                            if os.path.isfile(ffpath) == False:
                                print('\n[ERROR] Failed converting video !!')
                                print('[WARNING] Ffmpeg not in current working directory [ '+cwd+' ]')
                                print('[INFO] Ignore above warning if ffmpeg is added to environment path variable. ')
                            else:
                                print('[ERROR] File missing..!! Make sure the downloaded video is in the same dir as the script ')    
                                
                            


                        
                            
                        
                    elif yt_ch.lower() == 'e':
                            break
                    elif yt_ch == '':
                        print('\nEnter a stream or [e / h][for more details enter : help]')

                    elif yt_ch.lower() == 'help':
                        print('\nCopy and paste the stream you want to download [ e(exit) / h(highest resolution) / help(show this message) ]')
        
                    else:    
                        split_ytls = yt_ch.split(' > ')    
                        t_f = split_ytls[0]
                        reso = split_ytls[1]
                        sz = int(split_ytls[2].split('.')[0])
                        if sz <= 5:
                            rg = 50
                        elif sz <= 10:
                            rg = 100                    # Determining the range of progress bar from the file size
                        elif sz <= 100:
                            rg = 1000
                        else:
                            rg = 1000                  
                        
                        print('\n[INFO] Downloading '+str(yt.streams.filter(mime_type=t_f,res=reso).first()))
                        if save_to:

                            for i in tqdm(range(rg),desc='Downloading...'):
                                yt.streams.filter(mime_type=t_f,res=reso).first().download(save_to) #save_to -> path
                                pass  
                        else:
                            for i in tqdm(range(rg),desc='Downloading...'):
                                yt.streams.filter(mime_type=t_f,res=reso).first().download() 
                                pass 
                        try:    
                            def_file_name = yt.streams.filter(mime_type=t_f,res=reso).first().default_filename
                            new_file_name = Path(yt.streams.filter(mime_type=t_f,res=reso).first().default_filename).stem+'.mp3'
                            cmd = [
                                "ffmpeg" , "-i" , def_file_name , new_file_name
                            ]
                            ff = FfmpegProgress(cmd)
                            for progress in ff.run_command_with_progress():
                                txt_prog = '[ '+'Converting... > '+f"{progress} / 100"+' %'+' ]'
                                time.sleep(0.8)
                                print(txt_prog)
                        except FileNotFoundError:
                            ffpath = cwd+'\ffmpeg.exe'
                            if os.path.isfile(ffpath) == False:
                                print('\n[ERROR] Failed converting video !!')
                                print('[WARNING] Ffmpeg not in current working directory [ '+cwd+' ]')
                                print('[INFO] Ignore above warning if ffmpeg is added to environment path variable. ')
                            else:
                                print('[ERROR] File missing..!! Make sure the downloaded video is in the same dir as the script ')    
                                        
            else:
                for lks in yt.streams:
                    print(str(lks.mime_type)+ ' > ' +str(lks.resolution) + ' > ' +str(lks.filesize/(1024*1024))+' MB')
                    spinner.stop()
                    print('\nCopy and paste the stream you want to download [ e(exit) / h(highest resolution) / help(show this message) ]')
                    yt_ch = ''
                    while yt_ch != 'e':
                        yt_ch = input(' > ')
                        if yt_ch.lower() == 'h':
                            print('\n[INFO] Downloading highest resolution of the given url : '+str(yt.streams.get_highest_resolution()))
                            if save_to:

                                for i in tqdm(range(1000),desc='Downloading...'):
                                    yt.streams.get_highest_resolution().download(save_to)
                                    pass
                            else:
                                for i in tqdm(range(1000),desc='Downloading...'):
                                    yt.streams.get_highest_resolution().download()
                                    pass

                        elif yt_ch.lower() == 'e':
                            break
                        elif yt_ch == '':
                            print('\nEnter a stream or [e / h][for more details enter : help]')

                        elif yt_ch.lower() == 'help':
                            print('\nCopy and paste the stream you want to download [ e(exit) / h(highest resolution) / help(show this message) ]')
            
                        else:    
                            split_ytls = yt_ch.split(' > ')    
                            t_f = split_ytls[0]
                            reso = split_ytls[1]
                            sz = int(split_ytls[2].split('.')[0])
                            if sz <= 5:
                                rg = 50 
                            elif sz <= 10:
                                rg = 100              # Determining the range of progress bar from the file size
                            elif sz <= 100:
                                rg = 1000
                            else:
                                rg = 1000                  
                            
                            print('\n[INFO] Downloading '+str(yt.streams.filter(mime_type=t_f,res=reso).first()))
                            if save_to:

                                for i in tqdm(range(rg),desc='Downloading...'):
                                    yt.streams.filter(mime_type=t_f,res=reso).first().download(save_to)  # save_to -> path
                                    pass
                            else:
                                for i in tqdm(range(rg),desc='Downloading...'):
                                    yt.streams.filter(mime_type=t_f,res=reso).first().download() 
                                    pass
                                
            


cli.add_command(get)                     





if __name__=="__main__":
    cli()           
        
        

