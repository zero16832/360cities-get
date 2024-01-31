import sys
from urllib.parse import urlparse, urljoin
from os.path import basename, exists, join
import os
from PIL import Image
from tqdm import tqdm
args = sys.argv[1:]

def combine(target, path):
    print(target)
    print("\n")
    # print(os.listdir(target))
    files = os.listdir(target)
    backfiles = []
    frontfiles = []
    leftfiles = []
    rightfiles = []
    upfiles = []
    downfiles = []
    backres = [0,0]
    frontres = [0,0]
    leftres = [0,0]
    rightres = [0,0]
    upres = [0,0]
    downres = [0,0]
    for file in files:
        if file.startswith("back"):
            im = Image.open(os.path.join(target, file))
            width, height = im.size
            backfiles.append([file, width, height])
        if file.startswith("front"):
            im = Image.open(os.path.join(target, file))
            width, height = im.size
            frontfiles.append([file, width, height])
        if file.startswith("left"):
            im = Image.open(os.path.join(target, file))
            width, height = im.size
            leftfiles.append([file, width, height])
        if file.startswith("right"):
            im = Image.open(os.path.join(target, file))
            width, height = im.size
            rightfiles.append([file, width, height])
        if file.startswith("up"):
            im = Image.open(os.path.join(target, file))
            width, height = im.size
            upfiles.append([file, width, height])
        if file.startswith("down"):
            im = Image.open(os.path.join(target, file))
            width, height = im.size
            downfiles.append([file, width, height])


    # filename, width, height, position down from top, position right from left


    for i in range(len(downfiles)):
        fileinfo = downfiles[i][0].split("-")
        fileinfo[2] = fileinfo[2].split(".")[0]
        downfiles[i].append(fileinfo[1])
        downfiles[i].append(fileinfo[2])
        # if along top, add up widths
        if downfiles[i][3] == '0':
            downres[1] = downres[1] + downfiles[i][1]
        # if along left, add up heights
        if downfiles[i][4] == '0':
            downres[0] = downres[0] + downfiles[i][2]
    for i in range(len(upfiles)):
        fileinfo = upfiles[i][0].split("-")
        fileinfo[2] = fileinfo[2].split(".")[0]
        upfiles[i].append(fileinfo[1])
        upfiles[i].append(fileinfo[2])
        # if along top, add up widths
        if upfiles[i][3] == '0':
            upres[1] = upres[1] + upfiles[i][1]
        # if along left, add up heights
        if upfiles[i][4] == '0':
            upres[0] = upres[0] + upfiles[i][2]
    for i in range(len(rightfiles)):
        fileinfo = rightfiles[i][0].split("-")
        fileinfo[2] = fileinfo[2].split(".")[0]
        rightfiles[i].append(fileinfo[1])
        rightfiles[i].append(fileinfo[2])
        # if along top, add up widths
        if rightfiles[i][3] == '0':
            rightres[1] = rightres[1] + rightfiles[i][1]
        # if along left, add up heights
        if rightfiles[i][4] == '0':
            rightres[0] = rightres[0] + rightfiles[i][2]
    for i in range(len(leftfiles)):
        fileinfo = leftfiles[i][0].split("-")
        fileinfo[2] = fileinfo[2].split(".")[0]
        leftfiles[i].append(fileinfo[1])
        leftfiles[i].append(fileinfo[2])
        # if along top, add up widths
        if leftfiles[i][3] == '0':
            leftres[1] = leftres[1] + leftfiles[i][1]
        # if along left, add up heights
        if leftfiles[i][4] == '0':
            leftres[0] = leftres[0] + leftfiles[i][2]
    for i in range(len(frontfiles)):
        fileinfo = frontfiles[i][0].split("-")
        fileinfo[2] = fileinfo[2].split(".")[0]
        frontfiles[i].append(fileinfo[1])
        frontfiles[i].append(fileinfo[2])
        # if along top, add up widths
        if frontfiles[i][3] == '0':
            frontres[1] = frontres[1] + frontfiles[i][1]
        # if along left, add up heights
        if frontfiles[i][4] == '0':
            frontres[0] = frontres[0] + frontfiles[i][2]
    for i in range(len(backfiles)):
        fileinfo = backfiles[i][0].split("-")
        fileinfo[2] = fileinfo[2].split(".")[0]
        backfiles[i].append(fileinfo[1])
        backfiles[i].append(fileinfo[2])
        # if along top, add up widths
        if backfiles[i][3] == '0':
            backres[1] = backres[1] + backfiles[i][1]
        # if along left, add up heights
        if backfiles[i][4] == '0':
            backres[0] = backres[0] + backfiles[i][2]

    print(downfiles)
    print(downres)
    im = Image.new('RGB', (downres[1], downres[0]))
    for i in tqdm(range(len(downfiles))):
        im2 = Image.open(os.path.join(target, downfiles[i][0]))
        im.paste(im2, (512*(int(downfiles[i][4])), 512*(int(downfiles[i][3]))))
    im.save(os.path.join(path, f"down-{downres[0]}x{downres[1]}.png"))
    im = Image.new('RGB', (upres[1], upres[0]))
    for i in tqdm(range(len(upfiles))):
        im2 = Image.open(os.path.join(target, upfiles[i][0]))
        im.paste(im2, (512*(int(upfiles[i][4])), 512*(int(upfiles[i][3]))))
    im.save(os.path.join(path, f"up-{upres[0]}x{upres[1]}.png"))
    im = Image.new('RGB', (rightres[1], rightres[0]))
    for i in tqdm(range(len(rightfiles))):
        im2 = Image.open(os.path.join(target, rightfiles[i][0]))
        im.paste(im2, (512*(int(rightfiles[i][4])), 512*(int(rightfiles[i][3]))))
    im.save(os.path.join(path, f"right-{rightres[0]}x{rightres[1]}.png"))
    im = Image.new('RGB', (leftres[1], leftres[0]))
    for i in tqdm(range(len(leftfiles))):
        im2 = Image.open(os.path.join(target, leftfiles[i][0]))
        im.paste(im2, (512*(int(leftfiles[i][4])), 512*(int(leftfiles[i][3]))))
    im.save(os.path.join(path, f"left-{leftres[0]}x{leftres[1]}.png"))
    im = Image.new('RGB', (frontres[1], frontres[0]))
    for i in tqdm(range(len(frontfiles))):
        im2 = Image.open(os.path.join(target, frontfiles[i][0]))
        im.paste(im2, (512*(int(frontfiles[i][4])), 512*(int(frontfiles[i][3]))))
    im.save(os.path.join(path, f"front-{frontres[0]}x{frontres[1]}.png"))
    im = Image.new('RGB', (backres[1], backres[0]))
    for i in tqdm(range(len(backfiles))):
        im2 = Image.open(os.path.join(target, backfiles[i][0]))
        im.paste(im2, (512*(int(backfiles[i][4])), 512*(int(backfiles[i][3]))))
    im.save(os.path.join(path, f"back-{backres[0]}x{backres[1]}.png"))
    print("Done!")
    


# 00 01
# 10 11























if len(args) == 0:
    print('Usage: combiner.py <URL>')
    sys.exit(1)

for arg in args:
    path = basename(urlparse(arg).path)
    if exists(path):
        print("Download detected")
        innerfolders = next(os.walk(path))[1]
        if len(innerfolders) == 0:
            print("No resolutions detected, attempting download")
            exec(open(f"pano-get.py").read())
            exec(open(f"combiner.py").read())
        if len(innerfolders) == 1:
            print("One resolution available, combining...")
            combine(os.path.join(path, innerfolders[0]), path)
        if len(innerfolders) > 1:
            print("Multiple resolutions available, please select one:")
            for i in range(len(innerfolders)):
                print(str(i) + ": " + innerfolders[i])
            selection = input("Enter Number: ")
            print("You selected " + innerfolders[int(selection)])
            combine(os.path.join(path, innerfolders[int(selection)]), path)
    else:
        print("No download detected, attempting download")
        exec(open(f"pano-get.py").read())
        exec(open(f"combiner.py").read())