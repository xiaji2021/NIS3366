# 功能：使用GroungdingDINO对COCO数据集中的图片和diffusers生成的具有相同实体的图片进行实体检测，后续计算回归率，用于验证diffusers模型生成的图片质量
# 输入：/root/dataset/COCO/subval2014/coco_ground_truth_segementation_subval2014.json
#       /root/validation/diffusers 或 /root/dataset/COCO/subval2014
# 输出：/root/validation/Records_groungdingDINO_COCO.json

from errno import ENOTBLK
from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2
import os
import json

# 加载模型
model = load_model("/root/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", "/root/model/groundingdino_swint_ogc.pth")

BOX_TRESHOLD = 0.35
TEXT_TRESHOLD = 0.25

# 读取数据
file_path = "/root/dataset/COCO/subval2014/coco_ground_truth_segementation_subval2014.json"
datas = []
with open(file_path,"r") as f:
    for line in f:
        datas.append(json.loads(line))

# 检测实体
Records = []
# image_dir = "/root/validation/diffusers"
image_dir = "/root/dataset/COCO/subval2014"
for data in datas:
    # image_id = "diffusers_"+str(data["image_id"])+".jpg"
    image_id = str(data["image_id"])
    entities = data["objects"]
    IMAGE_PATH = os.path.join(image_dir,data["image"])
    TEXT_PROMPT = " . ".join(entities)
    print(image_id,TEXT_PROMPT)

    # 加载图片
    image_source, image = load_image(IMAGE_PATH)

    # 检测实体
    boxes, logits, phrases = predict(
        model=model,
        image=image,
        caption=TEXT_PROMPT,
        box_threshold=BOX_TRESHOLD,
        text_threshold=TEXT_TRESHOLD
    )
    Records.append({"image_id":image_id,"entities_gen":entities,"entities_found":list(set(phrases))})
    
    # 将检测到的实体标注在图片中
    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    output_dir = "/root/validation/groungdingDINO"
    cv2.imwrite(os.path.join(output_dir,image_id), annotated_frame)


# 保存数据至json文件
Records_path = "/root/validation/Records_groungdingDINO_COCO.json"
with open(Records_path,"w") as f:
    json.dump(Records,f,indent=4)
    