from flask import Flask, request, jsonify, send_from_directory
from diffusers import StableDiffusionPipeline
import torch
import os
from flask_cors import CORS
from uuid import uuid4
from werkzeug.utils import secure_filename
import sys
sys.path.append('/root/mycode')
from Stable_Diffusion import STABLE_DIFFUSION

app = Flask(__name__, static_folder='images')
CORS(app)  # 启用 CORS

# model = StableDiffusionPipeline.from_pretrained(
#     "/root/model/stable-diffusion-v1-5",
#     revision="fp16",
#     torch_dtype=torch.float16
# )
# model.to("cuda")

model = STABLE_DIFFUSION()


@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('text')
    if prompt is None or prompt.strip() == '':
        return jsonify({'error': 'No prompt provided'}), 400

    # image = model.generate_image(prompt).images[0]
    # 使用 secure_filename 清洁文件名
    unique_filename = f"generated_image_{uuid4().hex}.png"
    output_filepath = os.path.join(app.static_folder, secure_filename(unique_filename))

    model.generate_image(prompt,output_filepath)
    # # 保存图片到静态文件夹
    # image.save(output_filepath)

    # 构建图片的URL
    image_url = request.host_url + 'images/' + unique_filename

    # 返回包含图片URL的响应
    return jsonify({'image_path': image_url})


# 路由提供静态文件夹中的图片
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
