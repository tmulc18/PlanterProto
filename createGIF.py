import imageio
import os
import glob


file_folder = "timelapse_photos"
files = glob.glob(file_folder+"/*")
files.sort(key=os.path.getmtime)

with imageio.get_writer('c1.gif', mode='I') as writer:
    for filename in files:
        #t = int(filename.split('/img')[1].split('.png')[0])
        #if t<= 10000:
        image = imageio.imread(filename)
        writer.append_data(image)
