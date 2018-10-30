import imageio
import os
import glob


reverse = True
use_sys_time = False
pic_root = "pic_"
file_folder = "timelapse_photos"
output = "c_rewind.gif"
files = glob.glob(file_folder+"/*")

if use_sys_time:
    files.sort(key=os.path.getmtime)
else:
    files.sort(key=lambda x: int(x.split(pic_root)[-1]\
                                  .split('.')[0]         # remove extension
                                )
              )

with imageio.get_writer(output, mode='I') as writer:
    for filename in files:
        t = int(filename.split(pic_root)[-1].split('.')[0])
        #if t<= 10000:
        if t >= 54:
            image = imageio.imread(filename)
            writer.append_data(image)
    files.sort(key=lambda x: -1*int(x.split(pic_root)[-1]\
                                  .split('.')[0]         # remove extension
                                   )
              )


    if reverse:
        for filename in files:
            t = int(filename.split(pic_root)[-1].split('.')[0])
            #if t<= 10000:
            if t >= 54:
                image = imageio.imread(filename)
                writer.append_data(image)


