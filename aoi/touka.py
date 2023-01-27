from PIL import Image
im1 = Image.open('aoi/waku5-50.png')
im1.putalpha(128)
im2 = Image.open('aoi/ira5.png')

bg = Image.new("RGBA", (1920, 1080), (255, 255, 255, 0))


bg.paste(im2,(0,0),im2)
bg.paste(im1,(0,0),im1)

bg.save("aoi/join5-50.png")