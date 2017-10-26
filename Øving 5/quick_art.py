from PIL import Image,ImageDraw
from PIL import ImageFilter
from PIL import ImageEnhance
import shutil



# 2.2 The Imager Class

class Imager():
    _pixel_colors = {"red":(255,0,0), "green": (0,255,0), "blue": (0,0,255), "white": (255,255,255), "black": (0,0,0),
                     "purple rain":(104,33,101), "pink kimmy":(224,32,203), "blue waves":(32,94,224),
                     "techi green":(119,204,98), "mustard":(240,216,72)}

    def __init__(self,fid=False,image=False,width=100,height=100,background="black",mode="RGB"):
        self.fid = fid # The image file
        self.image = image # A PIL image object
        self.xmax = width; self.ymax = height # These can change if there’s an input image or file
        self.mode = mode
        self.init_image(background=background)

    def init_image(self,background="black"):
        if self.fid: self.load_image()
        if self.image: self.get_image_dims()
        else: self.image = self.gen_plain_image(self.xmax,self.ymax,background)
        # Load image from file
    def load_image(self):
        self.image = Image.open(self.fid) # the image is actually loaded as needed (automatically by PIL)
        if self.image.mode != self.mode:
            self.image = self.image.convert(self.mode)
    # Save image to a file. Only if fid has no extension is the type argument used.
    def dump_image(self,fid,type="gif"):
        fname = fid.split(".")
        type = fname[1] if len(fname) > 1 else type
        self.image.save(fname[0]+"."+type,format=type)
    def get_image(self):
        return self.image

    def set_image(self,im): self.image = im

    def display(self): self.image.show()

    def get_image_dims(self):
        self.xmax = self.image.size[0]
        self.ymax = self.image.size[1]

    def gen_plain_image(self,w,h,color,mode="RGB"):
        return Image.new(mode,(w,h),self.get_color_rgb(color))

    def get_color_rgb(self,colorname):
        return Imager._pixel_colors[colorname]

    def resize(self,new_width,new_height):
        return Imager(image=self.image.resize((new_width,new_height)))

    def scale(self,xfactor,yfactor):
        return self.resize(round(xfactor*self.xmax),round(yfactor*self.ymax))


    # 2.2.1 Pixel Access and Manipulation
    def get_pixel(self, x, y):
        return self.image.getpixel((x, y))

    def set_pixel(self, x, y, rgb):
        self.image.putpixel((x, y), rgb)

    def combine_pixels(self, p1, p2, alpha=0.5):
        return tuple([round(alpha * p1[i] + (1 - alpha) * p2[i]) for i in range(3)])

    def map_image(self, func):
        return Imager(image=Image.eval(self.image, func))  # eval creates a new image.

    def map_image2(self, func):
        im2 = self.image.copy()

        for i in range(self.xmax):
            for j in range(self.ymax):
                im2.putpixel((i, j), func(im2.getpixel((i, j))))
        return Imager(image=im2)

    def map_color_wta(self, thresh=0.34):

        # Local function
        def wta(p):  # p is an RGB tuple
            s = sum(p);
            w = max(p)

            if s > 0 and w / s >= thresh: # threshold
                return tuple([(x if x == w else 0) for x in p])
            else:
                return (0, 0, 0)
            return self.map_image2(wta, self.image)


    # part 2.2.2 Combining Images
    def paste(self, im2, x0=0, y0=0):
        self.image.paste(im2.image, (x0, y0, x0 + im2.xmax, y0 + im2.ymax))

    def reformat(self, fname, dir=None, ext="jpeg", scalex=1.0, scaley=1.0):
        im = self.scale(scalex, scaley)

        im.dump_image(fname, dir=dir, ext=ext)

    def concat_vert(self, im2=False, background="black"):
        im2 = im2 if im2 else self  # concat with yourself if no other imager is given.
        im3 = Imager()
        im3.xmax = max(self.xmax, im2.xmax)
        im3.ymax = self.ymax + im2.ymax
        im3.image = im3.gen_plain_image(im3.xmax, im3.ymax, background)
        im3.paste(self, 0, 0)
        im3.paste(im2, 0, self.ymax)
        return im3

    def concat_horiz(self, im2=False, background="black"):
        im2 = im2 if im2 else self  # concat with yourself if no other imager is given.

        im3 = Imager()
        im3.ymax = max(self.ymax, im2.ymax)
        im3.xmax = self.xmax + im2.xmax
        im3.image = im3.gen_plain_image(im3.xmax, im3.ymax, background)
        im3.paste(self, 0, 0)
        im3.paste(im2, self.xmax, 0)
        return im3

    def morph(self, im2, alpha=0.5):
        im3 = Imager(width=self.xmax, height=self.ymax)  # Creates a plain image
        for x in range(self.xmax):
            for y in range(self.ymax):
                rgb = self.combine_pixels(self.get_pixel(x, y), im2.get_pixel(x, y), alpha=alpha)
                im3.set_pixel(x, y, rgb)
        return im3

    def morph4(self, im2):
        im3 = self.morph(im2, alpha=0.66)
        im4 = self.morph(im2, alpha=0.33)
        return self.concat_horiz(im3).concat_vert(im4.concat_horiz(im2))

    def tunnel(self, levels=3, scale=0.75):
        if levels == 0:
            return self
        else:
            child = self.scale(scale, scale)  # child is a scaled copy of self
            child.tunnel(levels - 1, scale)  # Recursion
            dx = round((1 - scale) * self.xmax / 2);
            dy = round((1 - scale) * self.ymax / 2)
            self.paste(child, dx, dy)
        return self

    def mortun(self, im2, levels=5, scale=0.75):
        return self.tunnel(levels, scale).morph4(im2.tunnel(levels, scale))


    # FilterPackage
    def draw_a_cross(self):
        im = self.image

        draw = ImageDraw.Draw(im)
        draw.line((0, 0) + im.size, fill=128, width=15)
        draw.line((0, im.size[1], im.size[0], 0), fill=128, width=15)
        del draw
        return Imager(image=im)

    # Created methods
    def collage(self):
        # resize image to 1/4 size and add 4 images to original image
        portion = self.scale(0.5, 0.5)
        # paste image in the upper right
        self.paste(portion, 0, 0)
        # lower right
        self.paste(portion, 0, int(self.ymax / 2))
        # upper left
        self.paste(portion, int(self.xmax / 2), 0)
        # lower left
        self.paste(portion, int(self.xmax / 2), int(self.ymax / 2))
        return Imager(image=self.image)

    def shift_color(self,RGB):
        R,G,B = RGB
        for x_pixel in range(self.xmax):
            for y_pixel in range(self.ymax):
                im_R,im_G,im_B = self.get_pixel(x_pixel,y_pixel)
                im_R += R
                im_G += G
                im_B += B
                pixel_RGB = (im_R,im_G,im_B)
                self.set_pixel(x_pixel,y_pixel,pixel_RGB)

        return Imager(image=self.image)

    def pop_art(self,dim, colorshift):
        if dim == 4:
            # resize image to 1/4 size and add 4 images to original image
            portion = self.scale(0.5, 0.5)
            self.paste(portion, 0, 0)
            shift_red = portion.shift_color((colorshift,0,0))
            self.paste(shift_red, 0, int(self.ymax / 2))
            # reset red shift
            reset_red =  portion.shift_color((-colorshift,0,0))
            shift_green = portion.shift_color((0, colorshift,0))
            self.paste(shift_green, int(self.xmax / 2), 0)
            # reset green shift
            reset_green =  portion.shift_color((0,-colorshift,0))
            shift_blue = portion.shift_color((0,0, colorshift))
            self.paste(shift_blue, int(self.xmax / 2), int(self.ymax / 2))
        if dim==9:
            portion = self.scale(0.33,0.33)

            # First row
            # paste original image
            self.paste(portion, 0, 0)

            # apply filter purple rain
            purple_rain = self._pixel_colors["purple rain"]
            shift_green = portion.shift_color(purple_rain)
            self.paste(shift_green, int(self.xmax / 3), 0)
            # reset purple rain
            R_pr,G_pr,B_pr =self._pixel_colors["purple rain"]
            reset_pr = (-R_pr,-G_pr,-B_pr)
            reset_green = shift_green.shift_color(reset_pr)

            # apply filter mustard
            mustard = self._pixel_colors["mustard"]
            apply_mustard = reset_green.shift_color(mustard)
            self.paste(apply_mustard,int(self.xmax*2/3),0)
            # reset mustard
            R_ms,G_ms,B_ms = self._pixel_colors["mustard"]
            reset_ms = (-R_ms,-G_ms,-B_ms)
            reset_mustrad =apply_mustard.shift_color(reset_ms)

            # Second row

            shift_red = reset_mustrad.shift_color(self._pixel_colors["techi green"])
            self.paste(portion, 0, int(self.ymax / 3))
            # reset red shift
            reset_red = portion.shift_color(self._pixel_colors["purple rain"])
            shift_blue = portion.shift_color(self._pixel_colors["purple rain"])
            self.paste(shift_blue, int(self.xmax / 3), int(self.ymax / 3))


        if dim == 1:
            # resize image to 1/4 size and add 4 images to original image
            portion = self.scale(0.5, 0.5)
            self.paste(portion, 0, 0)
            portion1 = Imager(image=self.image)
            # apply filter purple rain
            purple_rain = self._pixel_colors["purple rain"]
            shift_green = portion.change_background(purple_rain)
            self.paste(shift_green, int(self.xmax / 3), 0)
            # reset purple rain
            R_pr, G_pr, B_pr = self._pixel_colors["purple rain"]
            reset_pr = (-R_pr, -G_pr, -B_pr)
            reset_green = portion.change_background(reset_pr)

            # apply filter mustard
            mustard = self._pixel_colors["mustard"]
            apply_mustard = portion1.change_background(mustard)
            self.paste(apply_mustard, int(self.xmax * 2 / 3), 0)
            # reset mustard
            R_ms, G_ms, B_ms = self._pixel_colors["mustard"]
            reset_ms = (-R_ms, -G_ms, -B_ms)
            portion.change_background(reset_ms)


        return Imager(image=self.image)

    def change_background(self,color):
        for x_pixel in range(self.xmax):
            for y_pixel in range(self.ymax):
                im_R, im_G, im_B = self.get_pixel(x_pixel, y_pixel)
                # if pixel is almost completely white
                if im_R>250 and im_G > 250 and im_B > 250:
                    self.set_pixel(x_pixel,y_pixel,color)
        return Imager(image=self.image)



def main():
    Guido = "Guido_van_Rossum.jpg"
    Einstein = "einstein_patentoffice.jpg"
    # initialize image object
    image = Image.open(Einstein)
    #shutil.copy("image.png", "image2.png")
    # initialize imager object
    imager = Imager(Einstein,image)
    #imager.collage()
    #imager.change_background(imager._pixel_colors["techi green"])
    #imagedraw = imager.draw_a_cross()
    pop_art = imager.pop_art(9,50)
    pop_art.display()
    #imager.display()

main()
