from blind_watermark import WaterMark
from blind_watermark import AttackFunctions

# bwm1 = WaterMark(password_img=1, password_wm=1)
# bwm1.read_img('/root/merlion.png')
# wm = 'NIS3366'
# bwm1.read_wm(wm, mode = "str")
# # wm="/root/astronaut_rides_horse.png"
# # bwm1.read_wm(wm, mode='img')
# bwm1.embed('merlion_watermark.png')
# len_wm = len(bwm1.wm_bit)
# print('Put down the length of wm_bit {len_wm}'.format(len_wm=len_wm))

# import string
# alphabet = list(string.ascii_letters) + list(string.punctuation) + list(string.digits)
# print(alphabet)

len_wm = 119
bwm1 = WaterMark(password_img=1, password_wm=1)
wm_extract = bwm1.extract('/root/NIS3366/src/static/watermark_gen/watermark_gen_c2dbc69d4b0f4a86b397f597c2c21cc6.png', wm_shape=len_wm, mode='str')
print(wm_extract)


# AttackFunctions.resize_att('merlion_watermark.png','merlion_watermark_resize.png')
# wm_extract = bwm1.extract('merlion_watermark_resize.png', wm_shape=len_wm, mode='str')
# print(wm_extract)

# AttackFunctions.salt_pepper_att('merlion_watermark.png','merlion_watermark_salt.png')
# wm_extract = bwm1.extract('merlion_watermark_salt.png', wm_shape=len_wm, mode='str')
# print(wm_extract)

# AttackFunctions.rot_att('merlion_watermark.png','merlion_watermark_rot.png')
# wm_extract = bwm1.extract('merlion_watermark_rot.png', wm_shape=len_wm, mode='str')
# print(wm_extract)

# AttackFunctions.rot_att('merlion_watermark_rot.png','merlion_watermark_rot_back.png',angle=-45)
# wm_extract = bwm1.extract('merlion_watermark_rot_back.png', wm_shape=len_wm, mode='str')
# print(wm_extract)


# AttackFunctions.shelter_att('merlion_watermark.png','merlion_watermark_shelter.png')
# wm_extract = bwm1.extract('merlion_watermark_shelter.png', wm_shape=len_wm, mode='str')
# print(wm_extract)

# AttackFunctions.bright_att('merlion_watermark.png','merlion_watermark_bright.png')
# wm_extract = bwm1.extract('merlion_watermark_bright.png', wm_shape=len_wm, mode='str')
# print(wm_extract)


