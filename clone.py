# Requires Python 2.7+

import os
import shutil

name19 = "shaderpackage019.sdp"
for i in range(1, 19):
    fileID = "{:0>3d}".format(i)
    shutil.copyfile(name19, "shaderpackage" + fileID + ".sdp")
