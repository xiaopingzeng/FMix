import numpy as np
import h5py
import multiprocessing
import os
from PIL import Image

SIZE = 256

imagenet_dir = '/ssd/ILSVRC2012/train'
target_dir = '/ssd/imagenet_hdf5/train'

subdirs = [d for d in os.listdir(imagenet_dir) if os.path.isdir(os.path.join(imagenet_dir, d))]

num_cpus = multiprocessing.cpu_count()
pool = multiprocessing.Pool(num_cpus)


def process(path):
    with open(path, 'rb') as f:
        img = Image.open(f)
        img = img.convert('RGB')
        return img.resize((SIZE, SIZE), Image.BILINEAR)


dest_list = []

for subdir in subdirs:
    from_dir = os.path.join(imagenet_dir, subdir)
    to_path = os.path.join(target_dir, subdir + '.hdf5')

    paths = os.listdir(from_dir)

    arr = np.array(pool.map(process, paths), dtype='uint8')
    with h5py.File(to_path, 'w') as f:
        f['data'] = arr

    for i, path in enumerate(paths):
        dest_list.append((subdir, i))

    print(subdir)
