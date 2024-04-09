# 功能：使用GroungdingDINO对diffusers生成的训练图片进行标注
# 输入：/root/train/diffusers
# 输出：/root/train/train_data.json

from groundingdino.util.inference import load_model, load_image, predict, annotate
import cv2
import os
import json 

# 加载模型
model = load_model("/root/GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py", "/root/model/groundingdino_swint_ogc.pth")

BOX_TRESHOLD = 0.35
TEXT_TRESHOLD = 0.25

# 读取图片数据
image_dir = "/root/train/diffusers"
image_ids = os.listdir(image_dir)

# 标注数据
Records = []
train_datas=[]
for image_id in image_ids:
    entity = image_id.split(".")[0]
    IMAGE_PATH = os.path.join(image_dir,image_id)
    TEXT_PROMPT = entity
    # print(TEXT_PROMPT)

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
    Records.append({"image_id":image_id,"entity_found":TEXT_PROMPT in phrases})
    
    # 将检测到的实体标注在图片中
    annotated_frame = annotate(image_source=image_source, boxes=boxes, logits=logits, phrases=phrases)
    output_dir = "/root/train/groundingDINO"
    cv2.imwrite(os.path.join(output_dir,image_id), annotated_frame)

    # 生成Qwen-VL对应格式的训练数据
    if TEXT_PROMPT in phrases:
        train_data = {}
        train_data["id"] = entity
        train_data["conversations"]=[]
        train_data["conversations"].append({"from":"user","value":f"Picture 1: <img>{os.path.join(image_dir,image_id)}</img>\n Generate the caption in English with grounding:"})
        train_data["conversations"].append({"from":"assistant","value":f"<ref>{entity}</ref><box>({boxes[0][0]*1000},{boxes[0][1]*1000}),({boxes[0][2]*1000}{boxes[0][3]*1000})</box>"})
        train_datas.append(train_data)


# Records_path = "/root/train/groundingDINO/Records.json"
# with open(Records_path,"w") as f:
#     json.dump(Records,f,indent=4)
    
# 保存训练数据至json文件
train_data_path = "/root/train/train_data.json"
with open(train_data_path,"w") as f:
    json.dump(train_datas,f,indent=4)