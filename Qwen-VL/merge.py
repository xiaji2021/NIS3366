
from peft import AutoPeftModelForCausalLM

model = AutoPeftModelForCausalLM.from_pretrained(
    "/root/model/Qwen-VL-Chat-lora", # path to the output directory
    device_map="auto",
    trust_remote_code=True,
    fp16=True,
).eval()

merged_model = model.merge_and_unload()
# max_shard_size and safe serialization are not necessary. 
# They respectively work for sharding checkpoint and save the model to safetensors
merged_model.save_pretrained("/root/model/Qwen-VL-Chat-new", max_shard_size="2048MB", safe_serialization=True)