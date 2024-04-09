# 功能：从实体检测的输出文件中计算Recall
# 输入：/root/validation/Records_groungdingDINO_diffusers.json 或 /root/validation/Records_groungdingDINO_COCO.json
# 输出：终端直接显示

import json
import os

# 读取数据
# file_path = "/root/validation/Records_groungdingDINO_diffusers.json"
file_path = "/root/validation/Records_groungdingDINO_COCO.json"
with open(file_path,"r") as f:
    datas=json.loads(f.read())

# 统计正确检测的实体个数
TP=FN=0
for data in datas:
    entities_gen = data["entities_gen"]
    entities_found =data["entities_found"]

    TP = TP + len([_ for _ in entities_found if _ in entities_gen ])
    FN = FN + len([_ for _ in entities_gen if _ not in entities_found ])

# 计算Recall
print(f"data file:{file_path}")
print('TP\tFN\t')
print('{}\t{}'.format(TP, FN))
recall = float(TP) / float(TP + FN)
print('Recall: {}'.format(recall))