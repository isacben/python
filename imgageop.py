# Image Optimizer
# Isaac Benitez Sandoval

from PIL import Image
from os import listdir, mkdir
from os.path import isfile, join
from datetime import datetime

path = "C:\\Users\\laptop\\Pictures\\squareguitar.com\\tailpiece ideas\\"
files = [f for f in listdir(path) if isfile(join(path, f))]
maxwith = 600
dest_path = path + "optimized_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S") + "\\"
mkdir(dest_path)

for file in files:
    foo = Image.open(path + file)
    ratio = maxwith/foo.size[0]
    foo = foo.resize((int(foo.size[0]*ratio),int(foo.size[1]*ratio)))
    foo.save(dest_path + file, optimize=True, quality=75)
