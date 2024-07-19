# -*- coding: utf-8 -*-
#!/usr/bin/env python
import datetime
import shutil
import os
import os
import io
import sys
import os.path
import re

root_path = "./gmgard.us"
pyfilePath = os.path.split(os.path.realpath(__file__))[0]

pyfileName = __file__.split("\\")[-1]


def batch_rename(src_path):
    print("batch_rename:" + src_path)
    filenames = os.listdir(src_path)

    for filename in filenames:
        old_name = os.path.join(src_path, filename)
        if os.path.isdir(old_name):
            continue

        reResult = is_sub_package(filename)
        if reResult == True:
            continue

        change_name = filename.replace('.', "_").replace(' ', '_')+ ".zip"
        # change_name = change_name.replace(' ', '')

        new_name = os.path.join(src_path, change_name)
        if os.path.exists(new_name):
            continue
        os.rename(old_name, new_name)

def is_sub_package(filename):
    _, ext = os.path.splitext(filename)

    reResult = re.findall(r".7z.\d{3}$", filename)
    if len(reResult) > 0:
        return True
    else:
        return False

def is_sub_package_001(filename):
    _, ext = os.path.splitext(filename)

    reResult = re.findall(r".7z.001$", filename)
    if len(reResult) > 0:
        return True
    else:
        return False

def is_sub_package_other(filename):
    if is_sub_package(filename) and not is_sub_package_001(filename):
        return True
    else:
        return False


if __name__ == "__main__":
    batch_rename(pyfilePath)
