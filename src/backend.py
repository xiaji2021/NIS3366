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

MAX_PROMPT_LEN = 128
DEFAULT_SEED = 1234
MIN_SEED = 0
MAX_SEED = 2**32 -1

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
    height = data.get('height')
    width = data.get('width')
    step = data.get('step')
    scale = data.get('scale')
    seed = data.get('seed')

    height = int(height)
    width = int(width)
    step = int(step)
    scale = float(scale)

    if seed is None:
        seed = DEFAULT_SEED
    else:
        try:
            seed = int(seed)
            if seed > MAX_SEED or seed <MIN_SEED:
                return jsonify({'error': 'seed is beyond range'}), 400
        except ValueError:
            return jsonify({'error': 'Seed must be a number'}), 400



    if prompt is None or prompt.strip() == '':
        return jsonify({'error': 'No prompt provided'}), 400

    if len(prompt) > MAX_PROMPT_LEN:
        return jsonify({'error': 'prompt len limited'}), 400


    # image = model.generate_image(prompt).images[0]
    # 使用 secure_filename 清洁文件名
    unique_filename = f"generated_image_{uuid4().hex}.png"
    output_filepath = os.path.join(app.static_folder, secure_filename(unique_filename))

    model.generate_image(prompt,output_filepath,height, width, step, scale, seed)
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
