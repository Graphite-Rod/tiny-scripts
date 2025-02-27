import getopt, sys
from PIL import Image
import itertools
from tqdm import tqdm

options = {}
options["lsb"] = 1
argumentList = sys.argv[1:]
try:
    arguments, values = getopt.getopt(argumentList, "i:l:", ["input", "lsb"])
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("#todo")
        elif currentArgument in ("-i", "--input"):
            options["input"] = currentValue
        elif currentArgument in ("-l", "--lsb"):
            options["lsb"] = int(currentValue)
except getopt.error as err:
    print(str(err))

if __name__ == "__main__":
    im = Image.open(options["input"])
    imsize = im.size
    
    r, g, b = Image.new("RGB", im.size), Image.new("RGB", im.size), Image.new("RGB", im.size)
    z = Image.new("RGB", im.size)
    for coord in tqdm(itertools.product(list(range(imsize[0])), list(range(imsize[1])))):
        subj = im.getpixel(coord)
        cr, cg, cb = ((subj[0] << (8 - options["lsb"]))%256)*2, ((subj[1] << (8 - options["lsb"]))%256)*2, ((subj[2] << (8 - options["lsb"]))%256)*2
        r.putpixel(coord, (cr, cr, cr))
        g.putpixel(coord, (cg, cg, cg))
        b.putpixel(coord, (cb, cb, cb))
        z.putpixel(coord, (cr, cg, cb))
    r.save("output/r_"+options["input"]+str(options["lsb"])+".png", quality='keep')
    g.save("output/g_"+options["input"]+str(options["lsb"])+".png", quality='keep')
    b.save("output/b_"+options["input"]+str(options["lsb"])+".png", quality='keep')
    z.save("output/z_"+options["input"]+str(options["lsb"])+".png", quality='keep')