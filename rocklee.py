from pytube import YouTube
import os, subprocess, time, sys, logging, datetime, uuid, re

def download():
    directory = os.path.dirname(__file__)
    logging.basicConfig(filename=directory+'logs/rocklee.log',level=logging.INFO)
    
    timeStamp = datetime.datetime
    timeStart = time.time()
    urlYoutube = sys.argv[1]
    
    logging.info('%s [RockLee] Received %s' % (timeStamp.now(), urlYoutube))
    print('%s [RockLee] Received %s' % (timeStamp.now(), urlYoutube))

    audio = YouTube(urlYoutube).streams.get_by_itag(140)
    
    finalName = audio.title
    finalNameReplaced = re.sub('[^A-Za-z0-9]+', '_',finalName)
    finalNameReplacedFixed = finalNameReplaced + '.mp3'
    
    logging.info('%s [RockLee] Name: %s' % (timeStamp.now(),finalNameReplaced))
    
    tempName = 'Download' + str(uuid.uuid4())
    mp4File = tempName + '.mp4'
    mp3File = tempName + '.mp3'
    
    directoryFile = directory + mp4File
    
    ffmpegConvert = ('ffmpeg -hide_banner -loglevel panic -y -i ' + mp4File + ' '+ mp3File)
    
    logging.info('%s [RockLee] Download Started' % timeStamp.now())
    audio.download(directory,filename=tempName)
    logging.info('%s [RockLee] Download Finished' % timeStamp.now())
    
    while not os.path.exists(directoryFile):
        time.sleep(1)
    
    if os.path.isfile(directoryFile):
        def convert():
            logging.info('%s [RockLee] Conversion Started' % timeStamp.now())
            subprocess.call(ffmpegConvert, shell=True)

            logging.info('%s [RockLee] Conversion Finished' % timeStamp.now())
            
            os.rename(mp3File,finalNameReplacedFixed)

            ffprobeCommand = 'ffprobe -show_streams -show_entries format=bit_rate,filename,start_time:stream=duration,width,height,display_aspect_ratio,r_frame_rate,bit_rate -of json -v quiet -i '
            ffprobeCheck = subprocess.Popen(ffprobeCommand + finalNameReplacedFixed, stdout=subprocess.PIPE, shell=True, universal_newlines=True)
            ffprobeCheckOutput = ffprobeCheck.communicate()[0]
            
            os.rename(finalNameReplacedFixed,'downloads/' + finalNameReplacedFixed)
            os.remove(mp4File)

            print(ffprobeCheckOutput)
            
            timeElapsed = time.time() - timeStart
            logging.info('%s [RockLee] Time Elapsed: %s' % (timeStamp.now(), timeElapsed))
            print('%s [RockLee] Time Elapsed: %s' % (timeStamp.now(), timeElapsed))
            
            time.sleep(2)
        convert()
    else:
        logging.warning('%s [RockLee] %s isnt a file!' % (timeStamp.now(),directoryFile))
download()
