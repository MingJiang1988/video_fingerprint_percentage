from VideoFingerPrint import *
from multiprocessing import Process
import os
import sys


def compare_videos(file_content1, filecontent2):
    fingerprint = VideoFingerPrint()
    output_result = fingerprint.search_sig(file_content1, filecontent2)
    return output_result


def video_process(src, dst, fingerprint_obj):
    if not os.path.isfile(src) or not os.path.isfile(dst):
        print("[x] Not found file. Please check file path")
        print("[x] Src: "+ src +" Dst: " +dst)
        sys.exit(0)
    if fingerprint_obj.check_video(dst):
        if fingerprint_obj.check_video(src):
            sig_file1 = fingerprint_obj.generate_fingerprint(src)
            sig_file2 = fingerprint_obj.generate_fingerprint(dst)
            result = compare_videos(sig_file1, sig_file2)
            print("[!] Compare result: smiliary :" + str(result*100) + "% " +
                  src + " : " + dst)
        else:
            result_img_check = fingerprint_obj.search_image(src, dst)
            if result_img_check:
                print("[!] There is duplication image in " + dst)

    else:
        print("[x] dst file must be a video. Please check destination file")


def read_filelist(listfile):
    fingerprint_obj = VideoFingerPrint()
    procs = []
    with open(listfile) as f:
        lines = f.readlines()
        for line in lines:
            line = line.replace("\r\n", "").replace("\n","")
            src = line.split(",")[0]
            dst = line.split(",")[1]
            #compare_videos(src, dst)
            proc = Process(target=video_process, args=(src, dst, fingerprint_obj,))
            procs.append(proc)
            proc.start()
        for p in procs:
            p.join()
    f.close()


if __name__ == '__main__':
    option = 0
    if len(sys.argv)<2:
        print("[x] --Help")
        print("[!] Command: {python test.py listfile}")
        print("[!] Listfile format is follow {file1, file2}")
    list_file = sys.argv[1]
    if os.path.isfile(list_file):
        read_filelist(list_file)
    else:
        print("no such file exists at this time")
