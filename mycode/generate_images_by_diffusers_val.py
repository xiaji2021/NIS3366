# 功能：使用diffusers的pipeline生成与COCO中采样的样本具有相同实体的图片
# 输入：/root/dataset/COCO/subval2014/coco_ground_truth_segementation_subval2014.json
# 输出：/root/validation/diffusers

from diffusers import DiffusionPipeline
import torch
import json
import os
from tqdm import tqdm

# 加载模型参数
pipeline = DiffusionPipeline.from_pretrained("/root/model/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipeline.to("cuda")

# 读取数据
file_path = "/root/dataset/COCO/subval2014/coco_ground_truth_segementation_subval2014.json"
datas = []
with open(file_path,"r") as f:
    for line in f:
        datas.append(json.loads(line))

# 生成图片
save_dir = "/root/validation/diffusers"
for data in tqdm(datas):
    print(data)
    entities = data["objects"]
    prompt  = "a " + " and a ".join(entities)
    print(entities,prompt)
    image = pipeline(prompt).images[0]
    save_path = os.path.join(save_dir,"diffusers_"+str(data["image_id"])+".jpg")
    image.save(save_path)