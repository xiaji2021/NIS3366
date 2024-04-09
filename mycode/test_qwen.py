# 功能：测试微调后的Qwen-VL-Chat-lora
# 输入：/root/dataset/COCO/subval2014/coco_ground_truth_segementation_subval2014.json
#       /root/validation/diffusers
# 输出：/root/validation/Qwen-lora

from html import entities
from Qwen_VL import QWEN_VL
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import json
import os
from tqdm import tqdm
torch.manual_seed(1234)

# 读取数据
file_path = "/root/dataset/COCO/subval2014/coco_ground_truth_segementation_subval2014.json"
datas = []
with open(file_path,"r") as f:
    for line in f:
        datas.append(json.loads(line))

# 加载模型
model = QWEN_VL()

# 实体检测
image_dir = "/root/validation/diffusers"
output_dir = "/root/validation/Qwen-lora"
for data in tqdm(datas):
    image_id = "diffusers_"+str(data["image_id"])+".jpg"
    img_input_path = os.path.join(image_dir,image_id)
    img_output_path = os.path.join(output_dir,image_id)
    
    model.extract_entity(img_input_path,img_output_path)

        