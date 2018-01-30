from FingerPrint import *
from PIL import Image
import cv2


class VideoFingerPrint():
    def __init__(self):
        pass
    
    def generate_fingerprint(self, file1):
        fp = FingerPrint()
        result = fp.generate(file1)
        return result

    def search_sig(self, file_content1, file_content2):
        fp = FingerPrint()
        percent = fp.comareFingerPrint(file_content1, file_content2)

        return percent

    def check_video(self, file):
        try:
            Image.open(file)
        except IOError:
            return True
        return False

    def dhash(self, image, hash_size=8):
        image = image.convert('L').resize((hash_size + 1, hash_size), Image.ANTIALIAS)
        difference = []
        for row in xrange(hash_size):
            for col in xrange(hash_size):
                pixel_left = image.getpixel((col, row))
                pixel_right = image.getpixel((col + 1, row))
                difference.append(pixel_left > pixel_right)

        decimal_value = 0
        hex_string = []
        for index, value in enumerate(difference):
            if value:
                decimal_value += 2 ** (index % 8)
            if (index % 8) == 7:
                hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
                decimal_value = 0
        return ''.join(hex_string)

    def search_image(self, imgname, videoname):
        pick_img = cv2.imread(imgname)
        pick_img = cv2.cvtColor(pick_img, cv2.COLOR_BGR2RGB)
        pil_im1 = Image.fromarray(pick_img)
        selected_img = pil_im1.convert('LA')
        hash1 = self.dhash(selected_img)
        vidcap = cv2.VideoCapture(videoname)
        while vidcap.isOpened():
            success, image = vidcap.read()
            if success:
                cv2_im2 = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                pil_im2 = Image.fromarray(cv2_im2)
                gray_pil_img2 = pil_im2.convert('LA')
                hash_frame = self.dhash(gray_pil_img2)

                if hash1 == hash_frame:
                    print("[!] found "+imgname+" duplication image in video "+videoname)
                    return True
            cv2.waitKey(1)
