from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.generation import GenerationConfig
import torch
torch.manual_seed(1234)

tokenizer = AutoTokenizer.from_pretrained("/root/model/Qwen-VL-Chat", trust_remote_code=True)

# model = AutoModelForCausalLM.from_pretrained("/root/model/Qwen-VL-Chat", device_map="cuda", trust_remote_code=True).eval()

from peft import AutoPeftModelForCausalLM
model = AutoPeftModelForCausalLM.from_pretrained(
    # pretrained_model_name_or_path = "/root/model/Qwen-VL-Chat",
    # adapter_name = "/root/model/Qwen-VL-Chat-lora", # path to the output directory
    pretrained_model_name_or_path = "/root/model/Qwen-VL-Chat-lora",
    adapter_name = "/root/model/Qwen-VL-Chat", 
    fp16=True,
    device_map="cuda:0",
    trust_remote_code=True,
).eval()

query = tokenizer.from_list_format([
    {'image': '/root/results/diffusers/traffic light.jpg'}, # Either a local path or an url
    {'text': 'Generate the caption in English with grounding:'},
])
inputs = tokenizer(query, return_tensors='pt')
inputs = inputs.to(model.device)
pred = model.generate(**inputs)
response = tokenizer.decode(pred.cpu()[0], skip_special_tokens=False)
print(response)
# <img>https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen-VL/assets/demo.jpeg</img>Generate the caption in English with grounding:<ref> Woman</ref><box>(451,379),(731,806)</box> and<ref> her dog</ref><box>(219,424),(576,896)</box> playing on the beach<|endoftext|>
image = tokenizer.draw_bbox_on_latest_picture(response)
if image:
  image.save('2.jpg')
else:
  print("no box")