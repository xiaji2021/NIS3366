# 功能：定义了QWEN_VL类，用于调用Qwen-VL模型进行实体检测
 

from html import entities
import sys
sys.path.append("/root/Qwen-VL")
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
import json
import os
from tqdm import tqdm
torch.manual_seed(1234)

class QWEN_VL:
    def __init__(self, type = "lora"):
        # 加载tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("/root/model/Qwen-VL-Chat", trust_remote_code=True)


        if type == "lora":
            # 使用peft加载微调后的模型
            from peft import AutoPeftModelForCausalLM
            self.model = AutoPeftModelForCausalLM.from_pretrained(
                pretrained_model_name_or_path = "/root/model/Qwen-VL-Chat-lora",
                adapter_name = "/root/model/Qwen-VL-Chat", 
                fp16=True,
                device_map="cuda:0",
                trust_remote_code=True,
            ).eval()
        elif type == "baseline":
            # 加载原始的Qwen-VL-Chat
            self.model = AutoModelForCausalLM.from_pretrained("/root/model/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()

    def extract_entity(
        self,
        img_input_path, # 要检测实体的图片的路径
        img_output_path, # 输出图片路径
        prompt = 'Generate the caption in English with grounding:', # 检测实体的prompt
    ):
        print(img_input_path, img_output_path)
        # 使用prompt和img_input_path构造输入
        query = self.tokenizer.from_list_format([
            {'image': img_input_path}, # Either a local path or an url
            {'text': prompt},
        ])
        inputs = self.tokenizer(query, return_tensors='pt')
        inputs = inputs.to(self.model.device)
        
        # 生成输出
        pred = self.model.generate(**inputs)
        response = self.tokenizer.decode(pred.cpu()[0], skip_special_tokens=False)
        # print(response)
        
        # 将检测到的实体标注在图片中
        try:
            image = self.tokenizer.draw_bbox_on_latest_picture(response)
            if image:
                image.save(img_output_path)
            else:
                print("no box")
        except:
            print("ValueError: Unclosed image token")

if __name__ == "__main__":
    model = QWEN_VL()
    model.extract_entity("/root/merlion.png","/root/merlion_entity.png")