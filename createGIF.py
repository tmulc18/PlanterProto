import imageio
import os
import glob

use_sys_time = False
pic_root = "pic_"
file_folder = "timelapse_photos"
files = glob.glob(file_folder+"/*")

if use_sys_time:
    files.sort(key=os.path.getmtime)
else:
    files.sort(key=lambda x: int(x.split(pic_root)[-1]\
                                  .split('.')[0]         # remove extension
                                )
              )

with imageio.get_writer('c1.gif', mode='I') as writer:
    for filename in files:
        #t = int(filename.split('/img')[1].split('.png')[0])
        #if t<= 10000:
        image = imageio.imread(filename)
        writer.append_data(image)
