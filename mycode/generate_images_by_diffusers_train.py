# 功能：使用diffusers的pipeline生成COCO中单个实体对应的训练图片
# 输入：/root/dataset/COCO/coco_entity.json
# 输出：/root/train/diffusers

from diffusers import DiffusionPipeline
import torch
import json
import os
from tqdm import tqdm

# 加载模型参数
pipeline = DiffusionPipeline.from_pretrained("/root/model/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipeline.to("cuda")

# 读取数据
file_path = "/root/dataset/COCO/coco_entity.json"
entities = []
with open(file_path,"r") as f:
    entities = json.loads(f.read())


# 生成图片
save_dir = "/root/train/diffusers"
for entity in tqdm(entities):
    print(entity)
    image = pipeline(entity).images[0]
    save_path = os.path.join(save_dir,entity+".jpg")
    image.save(save_path)