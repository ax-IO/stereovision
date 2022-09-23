from facesync.facesync import facesync
from facesync.utils import AudioAligner

# change file name to include the full
# video_file_G = ['/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Gauche/20200214_145835.MP4']
# target_audio_G = '/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Gauche/20200214_145835.wav'
# Intialize facesync class
# fs_G = facesync(video_files=video_file_G,target_audio=target_audio_G)
# Extracts audio from sample1.MP4
# fs_G.extract_audio()

# video_file_D = ['/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Droite/20200214_150021.MP4']
# target_audio_D = '/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Droite/20200214_150021.wav'
# Intialize facesync class
# fs_D = facesync(video_files=video_file_D,target_audio=target_audio_D)
# Extracts audio from sample1.MP4
# fs_D.extract_audio()


# video_files = ['/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Gauche/20200214_145835.MP4']
# target_audio = '/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Droite/20200214_150021.wav'
# Intialize facesync class
# fs = facesync(video_files=video_files,target_audio=target_audio)
# Extracts audio from sample1.MP4
# fs.extract_audio()

# Find offset by correlation
# self.target_audio : Original audio to which other files will be aligned to
# self.audio_files : List of audio files that needs to be trimmed (contient les audio provenant de extract_audio() càd le fichier son de video_files)
# fs.find_offset_corr(search_start=0,search_end=1,verbose=True)
# print(fs.offsets)
# Find offset by fast fourier transform
# fs.find_offset_dist()
# print(fs.offsets)

# video_files = ['/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Gauche/20200214_145835.MP4']
# target_audio = '/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Droite/20200214_150021.wav'
# Intialize facesync class
# fs = facesync(video_files=video_files,target_audio=target_audio)
# Trim video
# fs.trim_vids(offsets=[0.12])

video_files = ['/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Gauche/20200214_145835_trimmed.MP4']
target_audio = '/home/axiom/Documents/Source_Davy_fevrier_2020/Camera_Droite/20200214_150021.wav'
# Intialize facesync class
fs = facesync(video_files=video_files,target_audio=target_audio)
# Extracts audio from sample1.MP4
fs.extract_audio()
fs.find_offset_corr(search_start=0,search_end=1,verbose=True)
print(fs.offsets)

# %matplotlib notebook
# file_original = 'path/to/audio.wav'
# file_sample = 'path/to/sample.wav'
# AudioAligner(original=file_original, sample=file_sample)  