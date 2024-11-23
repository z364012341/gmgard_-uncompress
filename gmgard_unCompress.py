# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import zipfile
import py7zr
import pyzipper

# http://www.rarlab.com/rar/UnRARDLL.exe  然后需要配置环境变量
from unrar import rarfile
import shutil
import gmgard_rename

pyfilePath = os.path.split(os.path.realpath(__file__))[0]


pyfileName = __file__.split("\\")[-1]

G_PasswordList = [
    ['GCWHHZ', "utf8"],
    ['gmgard.com', "utf8"],
    ['艾莉絲在練劍', "utf8"],
    ['鬼畜王汉化组', "utf8"],
    ['gmgard.us', "utf8"],
    ['夢之行蹤', "utf8"],
    ['夢之行蹤236', "utf8"],
    ['茄哩啡', "utf8"],
    ['夢之行蹤240', "utf8"],
    ['夢之行蹤245', "utf8"],
    ['STARS', "utf8"],
    ['moetrace', "utf8"],
    ['神之领域', "utf8"],
    ['4k', "utf8"],
    ['龙之维塔', "utf8"],
    ['loli', "utf8"],
    ['CoconutCakeSorbet', "utf8"],
    ['cangku.icu', "utf8"],
    ['blackcatunderthemoon', "utf8"],
    ['HRLM', "utf8"],
    ['zz12zzxx', "utf8"],
    ['lblse', "utf8"],
    ['夢之行蹤249', "utf8"],
    ['xiaoa685', "utf8"],
    ['cc', "utf8"],
    ['LSFS', "utf8"],
    ['玖秀拉', "utf8"],
]

G_TempDirPath = os.path.join(pyfilePath, "temp")
G_Temp2DirPath = os.path.join(pyfilePath, "temp2")
G_OutDirPath = os.path.join(pyfilePath, "out")
G_ResourcesDirPath = os.path.join(pyfilePath, "resources")
G_PngOutDirPath = os.path.join(G_OutDirPath, "gmgard.us")
G_EpubOutDirPath = os.path.join(G_OutDirPath, "不可以涩涩")

class UnCompress:
    def __init__(self, file_path, output_path, password=None):
        self.file_path = file_path                  # 输入文件路径
        self.output_path = output_path              # 输出文件路径
        # self.password = password.encode('utf8')                 # 压缩密码
        self.password = password[0]
        self.encode = password[1]      # 压缩密码

    # zip解压缩
    def unzip_file(self):
        print("unzip_file")
        try:
            # with zipfile.ZipFile(file=self.file_path, mode='r') as fp:
            with pyzipper.AESZipFile(file=self.file_path, mode='r') as fp:
                fp.extractall(self.output_path, pwd=self.password.encode('utf8').decode('cp437').encode('cp437'))
            return True
        except Exception as ex:
            print(ex)
            return False


    # 7z解压缩
    def un7z_file(self):
        print("un7z_file")
        try:
            with py7zr.SevenZipFile(self.file_path, 'r', password=self.password) as fp:
                fp.extractall(path=self.output_path)
            return True
        except Exception as ex:
            print(ex)
            return False

    # RAR解压缩
    def unrar_file(self):
        print("unrar_file")
        cmdStr = 'UnRAR.exe x "{}" {} -p{} -inul -y'.format(self.file_path, self.output_path, self.password)
        ret = os.system(cmdStr)
        if ret == 0:
            return True
        else:
            return False

    def unrar_file_WinRAR(self):
        print("unrar_file")
        cmdStr = 'WinRAR.exe x "{}" {} -o+ -p{} -inul -ibck -y'.format(self.file_path, self.output_path, self.password)
        os.system(cmdStr)
        if not is_allEmptyDir(self.output_path):
            return True
        else:
            return False


    def run(self):
        file_state = False
        if not os.path.exists(self.file_path):
            return file_state
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)


        file_state = self.unrar_file_WinRAR()

        if not file_state:
            # zip解压缩
            if zipfile.is_zipfile(self.file_path):
                file_state = self.unzip_file()

            # 7z解压缩
            if py7zr.is_7zfile(self.file_path):
                file_state = self.un7z_file()

            # RAR解压缩
            if rarfile.is_rarfile(self.file_path):
                file_state = self.unrar_file()




        if file_state:
            # 还原乱码的汉字
            for root, dirs, files in os.walk(self.output_path):
                for name in files:
                    # print(name.encode("cp437").decode(encoding="gbk"))
                    # 文件名从utf-8解码成unicode字符串
                    try:
                        original_name = name.encode("cp437").decode(encoding="gbk")
                        os.rename(os.path.join(root, name), os.path.join(root, original_name))
                    except Exception as ex:
                        pass
                        # print(ex)

        return file_state


# 支持的图片格式
IMAGE_EXTENSIONS = [
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp"
]

def is_image_file(filename):
    """
    判断给定的文件名是否是一个图片文件名
    """
    _, ext = os.path.splitext(filename) # 获取文件名的扩展名
    return ext.lower() in IMAGE_EXTENSIONS

def is_book_file(filename):
    _, ext = os.path.splitext(filename) # 获取文件名的扩展名
    return ext.lower() == ".epub" or ext.lower() == ".pdf"

def is_allEmptyDir(dirPath):
    result = True
    for root, dirs, files in os.walk(dirPath):
        if len(files)>0:
            result = False
            break;

    return result


def _doTryUnCompressOneFile(filePsth, outPath):
    if os.path.exists(outPath):
        shutil.rmtree(outPath)

    for onePassword in G_PasswordList:
        name = os.path.splitext(os.path.split(filePsth)[1])[0]  # 获取文件名
        if gmgard_rename.is_sub_package_other(name):
            continue
        print("do uncompress {};  onePassword={}".format(name, onePassword))
        change_name = name.replace('.', "").replace(' ', '')
        uncompressPath = os.path.join(outPath, change_name)
        uncomOb = UnCompress(filePsth, uncompressPath, onePassword)
        ret = uncomOb.run()
        del uncomOb
        if ret:
            print("{} is success;".format(filePsth))
            return True
        else:
            print("{} is incorrect; next onePassword".format(onePassword))
    print("{} is fail;".format(filePsth))
    return False

def _copyFileAndMakedirs(src_file, dst_file):
    dst_dir, fileName = os.path.split(dst_file)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    shutil.copyfile(src_file, dst_file)


def _doTryRecurveUnCompressOneFile(filePath):
    compressRet = _doTryUnCompressOneFile(filePath, G_TempDirPath)
    if compressRet:
        for dirpath, dirnames, filenames in os.walk(G_TempDirPath):
            for fileName in filenames:
                src_file = os.path.join(dirpath, fileName)
                stats = os.stat(src_file)
                if stats.st_size < 1048576*512:
                    if is_image_file(fileName):
                        dst_file = src_file.replace(G_TempDirPath, G_PngOutDirPath)
                        _copyFileAndMakedirs(src_file, dst_file)
                        continue
                    elif is_book_file(fileName):
                        dst_file = src_file.replace(G_TempDirPath, G_EpubOutDirPath)
                        _copyFileAndMakedirs(src_file, dst_file)
                        continue

                dst_file = os.path.join(G_Temp2DirPath, fileName)
                _copyFileAndMakedirs(src_file, dst_file)
        return True
    else:
        return False


def _doResourcesDir():
    gmgard_rename.batch_rename(G_ResourcesDirPath)

    for root, dirs, files in os.walk(G_ResourcesDirPath):
        for name in files:
            filePath = os.path.join(root, name)
            ret = _doTryRecurveUnCompressOneFile(filePath)
            if ret:
                os.remove(filePath)
    _doTemp2DirDir()

def _doTemp2DirDir():
    # 把temp2文件夹中的文件拷贝到资源目录再次解压
    needNext = False
    for root, dirs, files in os.walk(G_Temp2DirPath):
        for name in files:
            # if gmgard_rename.is_sub_package_other(name):
            #     continue
            filePath = os.path.join(root, name)
            stats = os.stat(filePath)
            if stats.st_size > 10485760:
                needNext = True
                movePath = filePath.replace(G_Temp2DirPath, G_ResourcesDirPath)
                shutil.move(filePath, movePath)
    if needNext == True:
        _doResourcesDir()

def dealFileName(str):
    return str.replace('?', "_").replace(';', '_').replace(' ', '_').replace('・', '_').replace('♥', '_')

def needDirReanme(dirName):
    return True
    # return dirName.find('?') >= 0 or dirName.find(';') >= 0 or dirName.find(' ') or dirName.find('♥') >= 0 or dirName.find('・') >= 0

def renameDir(dirParentPath, dirName, index):
    dirPath = os.path.join(dirParentPath, dirName)
    dirNameList = os.listdir(dirPath)
    for childDir in dirNameList:
        item_path = os.path.join(dirPath, childDir)
        if os.path.isdir(item_path):
            index = renameDir(dirPath, childDir, index+1)

    dirNmaeIndex = index + 1
    change_name = 'rename_%d'%dirNmaeIndex
    new_name = os.path.join(dirParentPath, change_name)
    if not os.path.exists(new_name):
        shutil.move(dirPath, new_name)
    return dirNmaeIndex

if __name__ == "__main__":
    if not os.path.exists(G_OutDirPath):
        os.makedirs(G_OutDirPath)

    _doResourcesDir()
    renameDir(G_OutDirPath, "gmgard.us", 0)
    # dirNmaeIndex = 0
    # for count in range(0, 10):
    #     # 改了文件夹名字会导致后续的路径失效, 直接来个10次应该ok了
    #     for root, dirs, files in os.walk(G_PngOutDirPath):
    #         for name in dirs:
    #             dirPath = os.path.join(root, name)
    #             if needDirReanme(name) >= 0:
    #                 dirNmaeIndex = dirNmaeIndex + 1
    #                 change_name = 'rename_%d'%dirNmaeIndex
    #                 new_name = os.path.join(root, change_name)
    #                 if os.path.exists(new_name):
    #                     continue
    #                 os.rename(dirPath, new_name)

    # for root, dirs, files in os.walk(G_OutDirPath):
    #     for name in files:
    #         filePath = os.path.join(root, name)
    #         change_name = dealFileName(name)
    #         new_name = os.path.join(root, change_name)
    #         if os.path.exists(new_name):
    #             continue
    #         os.rename(filePath, new_name)

