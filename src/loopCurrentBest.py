from comp_gui_ann_runner import CompGuiAnnRunner
from grid import Grid
import ann_io
import sys
import getopt
import glob
import time

helptext = 'loopCurrentBest.py -A annfile'

try:
    opts, args = getopt.getopt(sys.argv[1:], "A:", ["ANNfile="])
except getopt.GetoptError:
    print helptext
    sys.exit()

for opt, arg in opts:
    if opt in ('-A', '--ANNfile'):
        ann_dir = arg

while True:
    for a in range(3):
            ann_files = glob.glob(ann_dir + str(a) + '/*.ann')
            nums = [x.split('.')[-2] for x in ann_files]
            nums = [int(x.split('/')[-1]) for x in nums]
            num = max(nums)

            ann_file = ann_dir + str(a) + '/' + str(num) + '.ann'
            n = ann_io.load(ann_file)
            runner = CompGuiAnnRunner(5, 5, 13, 3, True, 4, 100, draw_each=True)
            runner.run(n, iterations=200)
