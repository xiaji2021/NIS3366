from flask import Flask, request, jsonify, send_from_directory
from diffusers import StableDiffusionPipeline
import torch
import os
from flask_cors import CORS
from uuid import uuid4
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='images')
CORS(app)  # 启用 CORS

model = StableDiffusionPipeline.from_pretrained(
    "/root/.cache/huggingface/stable-diffusion-v1-5",
    revision="fp16",
    torch_dtype=torch.float16
)
model.to("cuda")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('text')
    if prompt is None or prompt.strip() == '':
        return jsonify({'error': 'No prompt provided'}), 400

    image = model(prompt).images[0]
    # 使用 secure_filename 清洁文件名
    unique_filename = f"generated_image_{uuid4().hex}.png"
    output_filepath = os.path.join(app.static_folder, secure_filename(unique_filename))

    # 保存图片到静态文件夹
    image.save(output_filepath)

    # 构建图片的URL
    image_url = request.host_url + 'images/' + unique_filename

    # 返回包含图片URL的响应
    return jsonify({'image_path': image_url})


# 路由提供静态文件夹中的图片
@app.route('/images/<filename>')
def images(filename):
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
