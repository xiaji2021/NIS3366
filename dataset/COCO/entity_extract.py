# 功能：从COCO_train2014中抽取出COCO的全部标注实体
# 输入：/root/dataset/COCO/coco_ground_truth_segementation_train2014.json
# 输出：/root/dataset/COCO/coco_entity.json

import os
import json

# 读取数据
file_path = "/root/dataset/COCO/coco_ground_truth_segementation_train2014.json"
infos = []
with open(file_path,"r") as f:
    for line in f:
        infos.append(json.loads(line))

# 抽取实体
entity = []
for info in infos:
    entity.extend(info["objects"])

# 去重
entity = list(set(entity))
print(entity)

# 输出到文件
output_path = "/root/dataset/COCO/coco_entity.json"
with open(output_path,"w") as f:
    json.dump(entity,f)