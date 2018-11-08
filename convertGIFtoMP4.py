import ffmpy

gif_name = "c_rewind.gif"
output = "output_rewind.mp4"
ff = ffmpy.FFmpeg(inputs={gif_name:None},outputs={output:None})
ff.run()
