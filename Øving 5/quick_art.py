from PIL import Image, ImageDraw, ImageEnhance
import random



# 2.2 The Imager Class

class Imager():
    _pixel_colors = {"red":(255,0,0), "green": (0,255,0), "blue": (0,0,255), "white": (255,255,255), "black": (0,0,0),
                     "purple rain":(104,33,101), "pink kimmy":(224,32,203), "blue waves":(12,74,204),
                     "techi green":(119,204,98), "mustard":(220,216,72), "geraldine":(250,140,130), "sunburn":(242,58,58),
                     "dreaming of":(141,17,142),"delete the past":(29,50,78),"akuma fluff":(121,195,35)}

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



    def pop_art(self,dim):

        # importing some colors
        purple_rain = self._pixel_colors["purple rain"]
        mustard = self._pixel_colors["mustard"]
        pink_kimmy = self._pixel_colors["pink kimmy"]
        techi_green = self._pixel_colors["techi green"]
        blue_waves = self._pixel_colors["blue waves"]
        geraldine = self._pixel_colors["geraldine"]
        sunburn = self._pixel_colors["sunburn"]
        dreaming_of = self._pixel_colors["dreaming of"]
        akuma_fluff = self._pixel_colors["akuma fluff"]


        if dim == 1:
            # resize image to 1/4 size and add 4 images to original image
            # NB I don't know why I have to create all instances and cant use just one instance
            portion = self.scale(0.5, 0.5)
            portion1 = self.scale(0.5, 0.5)
            portion2 = self.scale(0.5, 0.5)
            portion3 = self.scale(0.5, 0.5)


            # picking random colors
            colors = [pink_kimmy, purple_rain, mustard, techi_green, blue_waves, geraldine, sunburn, dreaming_of, akuma_fluff]

            all_colors = True
            while all_colors:
                color1 = colors[random.randint(0, 8)]
                color2 = colors[random.randint(0, 8)]
                color3 = colors[random.randint(0, 8)]
                color4 = colors[random.randint(0, 8)]
                if color1 != color2 != color3 != color4:
                    all_colors = False

            # paste first in top right corner
            portion.shift_color(color1)
            self.paste(portion, 0, 0)

            # paste second in top left corner
            portion1.shift_color(color2)
            self.paste(portion1, int(self.xmax / 2), 0)


            # paste third in down right corner
            portion2.shift_color(color3)
            self.paste(portion2, 0, int(self.ymax / 2))


            # paste fourth in down left corner
            portion3.shift_color(color4)
            self.paste(portion3, int(self.xmax / 2), int(self.ymax / 2))
            return Imager(image=self.image)

        if dim==2:

            # cut images 1/9th of original image
            portion1 = self.scale(1/3, 1/3)
            portion2 = self.scale(1/3, 1/3)
            portion3 = self.scale(1/3, 1/3)
            portion4 = self.scale(1/3, 1/3)
            portion5 = self.scale(1/3, 1/3)
            portion6 = self.scale(1/3, 1/3)
            portion7 = self.scale(1/3, 1/3)
            portion8 = self.scale(1/3, 1/3)
            portion9 = self.scale(1/3, 1/3)

            # First row

            # top right corner
            pink_kimmy = self._pixel_colors["pink kimmy"]
            shift_pk = portion1.shift_color(pink_kimmy)
            self.paste(shift_pk, 0, 0)


            # top middle
            purple_rain = self._pixel_colors["purple rain"]
            shift_pr = portion2.shift_color(purple_rain)
            self.paste(shift_pr, int(self.xmax / 3), 0)

            # top left corner
            mustard = self._pixel_colors["mustard"]
            shift_mustard = portion3.shift_color(mustard)
            self.paste(shift_mustard,int(self.xmax*2/3), 0)


            # Second row

            # middle right
            shift_techi = portion4.shift_color(self._pixel_colors["techi green"])
            self.paste(shift_techi, 0, int(self.ymax / 3))

            # center of image
            shift_waves = portion5.shift_color(self._pixel_colors["blue waves"])
            self.paste(shift_waves, int(self.xmax / 3), int(self.ymax / 3))

            # middle left
            shift_geraldine = portion6.shift_color(self._pixel_colors["geraldine"])
            self.paste(shift_geraldine, int(self.xmax * 2 / 3), int(self.ymax / 3))

            # third row

            # down right corner
            shift_sunburn = portion7.shift_color(self._pixel_colors["sunburn"])
            self.paste(shift_sunburn, 0, int(self.ymax * 2/3))

            # down center
            shift_dreaming = portion8.shift_color(self._pixel_colors["dreaming of"])
            self.paste(shift_dreaming, int(self.xmax / 3), int(self.ymax * 2 / 3))

            # down left
            shift_akuma = portion9.shift_color(self._pixel_colors["akuma fluff"])
            self.paste(shift_akuma, int(self.xmax*2/3), int(self.ymax * 2 / 3))

            randomized = self.puzzlize(4)

            return Imager(image=randomized.image)




        if dim == 3:
            # Andy Warhol type
            # first create a black and white image

            converter = ImageEnhance.Color(self.image)
            img = converter.enhance(0.0)
            img = Imager(image=img)

            # and turn down the brightness



            # cut images 1/9th of original image
            portion1 = img.scale(1 / 3, 1 / 3)
            portion2 = self.scale(1 / 3, 1 / 3)
            portion3 = self.scale(1 / 3, 1 / 3)
            portion4 = self.scale(1 / 3, 1 / 3)
            portion5 = self.scale(1 / 3, 1 / 3)
            portion6 = self.scale(1 / 3, 1 / 3)
            portion7 = self.scale(1 / 3, 1 / 3)
            portion8 = self.scale(1 / 3, 1 / 3)
            portion9 = self.scale(1 / 3, 1 / 3)

            # First row


            #### change background ###

            # top right corner

            portion1.change_background(pink_kimmy)

            # top middle

            portion2.change_background(purple_rain)

            # top left corner

            portion3.change_background(mustard)

            # Second row

            # middle right
            portion4.change_background(techi_green)

            # center of image
            portion5.change_background(blue_waves)

            # middle left
            portion6.change_background(geraldine)

            # third row

            # down right corner
            portion7.change_background(sunburn)

            # down center
            portion8.change_background(dreaming_of)

            # down left
            portion9.change_background(akuma_fluff)

            ### change profile color ##

            # First row

            # top right corner

            shift_pk = portion1.shift_color(blue_waves)
            self.paste(shift_pk, 0, 0)

            # top middle

            shift_pr = portion2.shift_color(geraldine)
            self.paste(shift_pr, int(self.xmax / 3), 0)

            # top left corner

            shift_mustard = portion3.shift_color(sunburn)
            self.paste(shift_mustard, int(self.xmax * 2 / 3), 0)

            # Second row

            # middle right
            shift_techi = portion4.shift_color(dreaming_of)
            self.paste(shift_techi, 0, int(self.ymax / 3))

            # center of image
            shift_waves = portion5.shift_color(akuma_fluff)
            self.paste(shift_waves, int(self.xmax / 3), int(self.ymax / 3))

            # middle left
            shift_geraldine = portion6.shift_color(pink_kimmy)
            self.paste(shift_geraldine, int(self.xmax * 2 / 3), int(self.ymax / 3))

            # third row

            # down right corner
            shift_sunburn = portion7.shift_color(techi_green)
            self.paste(shift_sunburn, 0, int(self.ymax * 2 / 3))

            # down center
            shift_dreaming = portion8.shift_color(mustard)
            self.paste(shift_dreaming, int(self.xmax / 3), int(self.ymax * 2 / 3))

            # down left
            shift_akuma = portion9.shift_color(purple_rain)
            self.paste(shift_akuma, int(self.xmax * 2 / 3), int(self.ymax * 2 / 3))

            return Imager(image=self.image)






    ######## sub methods ########

    # chaning background
    def change_background(self,color):
        for x_pixel in range(self.xmax):
            for y_pixel in range(self.ymax):
                im_R, im_G, im_B = self.get_pixel(x_pixel, y_pixel)
                # if pixel is almost completely white
                if im_R>254 and im_G > 254 and im_B > 254:
                    self.set_pixel(x_pixel,y_pixel,color)
        return Imager(image=self.image)


    # shift color
    def shift_color(self,RGB):
        R,G,B = RGB
        for x_pixel in range(self.xmax):
            for y_pixel in range(self.ymax):
                im_R,im_G,im_B = self.get_pixel(x_pixel,y_pixel)
                if im_R < 254 and im_G < 254 and im_B < 254:
                    im_R += R
                    im_G += G
                    im_B += B
                    if im_R == 255:
                        im_R -= 2
                    if im_G == 255:
                        im_G -= 2
                    if im_B == 255:
                        im_B -= 2
                    pixel_RGB = (im_R,im_G,im_B)
                    self.set_pixel(x_pixel,y_pixel,pixel_RGB)

        return Imager(image=self.image)


    def puzzlize(self, num_of_parts):
        parts = []
        startpoint = (0,0)
        startpoints = []
        for x in range(num_of_parts):
            for y in range(num_of_parts):
                img = self.image.crop((int(self.xmax * x / num_of_parts), int(self.ymax * y / num_of_parts), int(self.xmax * (x+1) / num_of_parts), int(self.ymax * (y+1) / num_of_parts)))


                parts.append(img)
                x_start, y_start = startpoint
                x_start = int(self.xmax*x / num_of_parts)
                y_start = int(self.ymax*y / num_of_parts)
                startpoint = (x_start, y_start)
                startpoints.append(startpoint)
        random.shuffle(parts)
        i = 0
        for part in parts:
            x, y = startpoints[i]
            image = Imager(image=part)
            self.paste(image, x, y)
            i += 1

        return Imager(image=self.image)

    def merge_images(self,image2=False):
        if self.xmax < image2.xmax :
            x_size = self.xmax
        else:
            x_size = image2.xmax
        if self.ymax < image2.ymax :
            y_size = self.ymax
        else:
            y_size = image2.ymax
        scaled_image1 = self.resize(x_size, y_size)
        scaled_image2 = image2.resize(x_size, y_size)
        morphed = scaled_image1.morph(scaled_image2)
        return Imager(image=morphed.image)


    ## combining methods
    def warhol_merge(self,):
        duplicate = Imager(image=self.image.copy())

        warhol1 = self.pop_art(3)
        merged = duplicate.merge_images(warhol1)
        return Imager(image=merged.image)

    def warhol_random(self):
        warhol = self.pop_art(3)
        warhol.puzzlize(4)

        return Imager(image=warhol.image)
def main():
    Einstein = "einstein_patentoffice.jpg"
    Obama = "obama.png"
    # initialize image object
    image = Image.open(Obama)
    image2 = Image.open(Einstein)

    # initialize imager object
    imager = Imager(Obama, image)
    imager2 = Imager(Einstein,image2)

    # try warhol art on obama picture
    #imager.pop_art(3)
    #imager.display()

    # try random pop art on einstein
    #imager2.pop_art(1)
    #imager2.display()

    # puzzlize on obama
    #imager.puzzlize(4)
    #imager.display()

    # random warhol
    imager.warhol_random()
    imager.display()

    # PS I used portrait images with white background
    # pop_art method works with dim 1, 2 and 3 for different results
