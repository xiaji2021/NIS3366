from diffusers import DiffusionPipeline
import torch
import json
import os
from tqdm import tqdm

pipeline = DiffusionPipeline.from_pretrained("/root/model/stable-diffusion-v1-5", torch_dtype=torch.float16)
pipeline.to("cuda")

file_path = "/root/dataset/COCO/coco_entity.json"
entities = []
with open(file_path,"r") as f:
    for line in f:
        entities = json.loads(line)

print(entities)
save_dir = "/root/results/diffusers"
for entity in tqdm(entities):
    print(entity)
    image = pipeline(entity).images[0]
    save_path = os.path.join(save_dir,entity+".jpg")
    image.save(save_path)