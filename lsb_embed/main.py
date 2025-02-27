from PIL import Image
import getopt, sys
from tqdm import tqdm


options = {}
options["lsb"] = 3
argumentList = sys.argv[1:]
try:
    arguments, values = getopt.getopt(argumentList, "hu:l:o:b:", ["help", "upper", "lower", "output", "lsb"])
    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--help"):
            print("#todo")
        elif currentArgument in ("-u", "--upper"):
            options["upper"] = currentValue
        elif currentArgument in ("-l", "--lower"):
            options["lower"] = currentValue
        elif currentArgument in ("-o", "--output"):
            options["output"] = currentValue
        elif currentArgument in ("-b", "--lsb"):
            options["lsb"] = int(currentValue)
except getopt.error as err:
    print(str(err))


def bitstopix(img, coord, bits, lsblen=1):
    pixel = img.getpixel(coord)
    bpx = list(map(lambda x: bin(x)[2:].zfill(8), pixel))
    for ch in range(3):
        bpx[ch] = bpx[ch][:-lsblen]
        bpx[ch] += bits[lsblen*ch:lsblen*(ch+1)]
    px = tuple([int(c, 2) for c in bpx])
    img.putpixel(coord, px)


if __name__ == "__main__":
    upper = Image.open(options["upper"])
    lower = Image.open(options["lower"])
    u = upper.size
    l = lower.size
    assert (u[0] >= l[0] or u[1] >= l[0]), "embedable is smaller than the canvas"
    for x in tqdm(range(l[0])):
        for y in range(l[1]):
            pl = lower.getpixel((x, y))
            pl = "".join([str(bin(a >> (8 - options["lsb"])))[2:].zfill(options["lsb"]) for a in pl])
            bitstopix(upper, (x, y), pl, options["lsb"])
    upper.save(options["output"], quality='keep')