from PIL import Image, ImageFilter
import random

# Crops sourceImage to its transparency bounds
def cropImageToBounds(sourceImage):
    imageBoundsSize = sourceImage.convert("RGBa").getbbox()  # premultiplied
    croppedImage = sourceImage.crop(imageBoundsSize)
    return croppedImage


try:
    bg = Image.open("./bg.jpg")
    shirt = Image.open("./shirt/shirt-1.png")
    pants = Image.open("./pants/pants-2.png")
    shoes = Image.open("./shoes/shoes-2.png")
    separationDistance = 100

    shirt = cropImageToBounds(shirt)
    pants = cropImageToBounds(pants)
    shoes = cropImageToBounds(shoes)

    shoes = shoes.rotate(45, 0, 1, None, None)

    size = separationDistance * 3 + shirt.size[0] + pants.size[0]

    outfitGridArtboard = Image.new("RGBA", (size, size), (255, 0, 0, 255))
    clothesLayer = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    clothesLayer.paste(shirt, (separationDistance, separationDistance), shirt)
    clothesLayer.paste(
        pants,
        (shirt.size[0] + separationDistance * 2, int(size / 2 - pants.size[1] / 2)),
        pants,
    )
    clothesLayer.paste(
        shoes, (separationDistance, shirt.size[1] - separationDistance * 2), shoes
    )
    clothesLayerAlpha = clothesLayer.split()[-1]
    shadowLayer = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    clothesLayerAlpha = clothesLayerAlpha.filter(ImageFilter.GaussianBlur(radius=20))
    shadowLayer.putalpha(clothesLayerAlpha)

    outfitGridArtboard.paste(bg, (0, 0))
    outfitGridArtboard.paste(shadowLayer, (2, 2), shadowLayer)
    outfitGridArtboard.paste(clothesLayer, (0, 0), clothesLayer)

    outfitGridArtboard.show()
    outfitGridArtboard.save("./outfitGridArtboard.png")
except IOError:
    print("e")

