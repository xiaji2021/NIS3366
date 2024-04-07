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

app = Flask(__name__, static_folder='static')
CORS(app)  # 启用 CORS

# model = StableDiffusionPipeline.from_pretrained(
#     "/root/model/stable-diffusion-v1-5",
#     revision="fp16",
#     torch_dtype=torch.float16
# )
# model.to("cuda")




@app.route('/generate-image', methods=['POST'])

def generate_image():
    model = STABLE_DIFFUSION()

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
    unique_filename = secure_filename(f"generated_image_{uuid4().hex}.png")
    output_filepath = os.path.join(app.static_folder, 'txt2images', unique_filename)
    if not os.path.exists(os.path.join(app.static_folder, 'txt2images')):
        os.mkdirs(os.path.join(app.static_folder, 'txt2images'))

    model.generate_image(prompt,output_filepath,height, width, step, scale, seed)
    # # 保存图片到静态文件夹
    # image.save(output_filepath)

    # 构建图片的URL
    image_url = request.host_url + 'txt2images/' + unique_filename

    # 返回包含图片URL的响应
    return jsonify({'image_path': image_url})


# 路由提供静态文件夹中的图片
@app.route('/txt2images/<filename>')
def images(filename):
    return send_from_directory(app.static_folder, filename)

// app.static_folder可能需要进行区分

@app.route('/entity-gen', methods=['POST'])
def entity():
    model = QWEN_VL()

    dic_path = os.path.join(app.static_folder, 'entity_origin')
    if not os.path.exists(dic_path):
        os.mkdirs(dic_path)
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    file = request.files['image']
    text = request.form.get('text')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(f"entity_origin_{uuid4().hex}.png")
        file_path = os.path.join(dic_path,filename)
        file.save(file_path)
    else:
        return jsonify({'error': 'No such file'}), 400

    output_filepath = os.path.join(app.static_folder, 'entity_gen')
    if not os.exists(output_filepath):
        os.mkdirs(output_filepath)
    model.extract_entity(file_path,output_filepath)
    image_url = request.host_url + 'entity-gen/' + unique_filename



@app.route('/entity-gen/<filename>')
def entityGen(filename):
    return send_from_directory(os.path.join(app.static_folder,entity_gen), filename)











if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)






