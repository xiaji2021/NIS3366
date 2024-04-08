from flask import Flask, request, jsonify, send_from_directory
from diffusers import StableDiffusionPipeline
import torch
import os
from flask_cors import CORS
from uuid import uuid4
from werkzeug.utils import secure_filename
import sys
sys.path.append('/root/mycode')
sys.path.append('/root/blind_watermark')
from Stable_Diffusion import STABLE_DIFFUSION
from Qwen_VL import QWEN_VL
from blind_watermark import WaterMark
from blind_watermark import AttackFunctions

len_wm = 0;

MAX_PROMPT_LEN = 128
DEFAULT_SEED = 1234
MIN_SEED = 0
MAX_SEED = 2**32 -1

app = Flask(__name__, static_folder='static')
CORS(app)  # 启用 CORS

# model = None

# 如何释放？
# @app.route('/load-model/t2i',methods=['GET'])
# def load_t2i():
#     global model
#     if model is not None:
#         del model
#         model = None
#     import gc
#     gc.collect()
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
#     model = STABLE_DIFFUSION()

# @app.route('/load-model/entity',methods=['GET'])
# def load_entity():
#     global model
#     if model is not None:
#         model = None
#     import gc
#     gc.collect()
#     if torch.cuda.is_available():
#         torch.cuda.empty_cache()
#     model = QWEN_VL()


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
        os.mkdir(os.path.join(app.static_folder, 'txt2images'))
    
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
    return send_from_directory(os.path.join(app.static_folder,'txt2images'), filename)


@app.route('/entity-gen', methods=['POST'])
def entity():
    model = QWEN_VL()
    dic_path = os.path.join(app.static_folder, 'entity_origin')
    # 存储原始图片的目录
    if not os.path.exists(dic_path):
        os.mkdir(dic_path)
    #如果不存在，创建目录
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    #未找到的错误处理
    file = request.files['image']
    # text = request.form.get('text')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(f"entity_origin_{uuid4().hex}.png")
        file_path = os.path.join(dic_path,filename)
        file.save(file_path)
        print('testttttttttttt')
        #将文件重命名并存储在定义的原始图片目录下
    else:
        return jsonify({'error': 'No such file'}), 400

    output_filepath = os.path.join(app.static_folder, 'entity_gen',filename)
    # 定义实体抽取后的生成图片目录
    if not os.path.exists(os.path.join(app.static_folder, 'entity_gen')):
        os.mkdir(os.path.join(app.static_folder, 'entity_gen'))
    model.extract_entity(file_path,output_filepath)
    # 模型运行
    image_url = request.host_url + 'entity-gen/' + filename
    return jsonify({'image_path': image_url})



@app.route('/entity-gen/<filename>')
def entityGen(filename):
    return send_from_directory(os.path.join(app.static_folder,'entity_gen'), filename)




@app.route('/watermark-gen', methods=['POST'])
def watermarkGen():
    global len_wm;
    dic_path = os.path.join(app.static_folder, 'watermark_origin')
    # 存储原始图片的目录
    if not os.path.exists(dic_path):
        os.mkdir(dic_path)
    #如果不存在，创建目录
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
    #未找到的错误处理
    file = request.files['image']
    text = request.form.get('text')
    print(text)
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(f"watermark_origin_{uuid4().hex}.png")
        file_path = os.path.join(dic_path,filename)
        file.save(file_path)
        #将文件重命名并存储在定义的原始图片目录下
    else:
        return jsonify({'error': 'No such file'}), 400
    output_filename = secure_filename(f"watermark_gen_{uuid4().hex}.png")

    output_filepath = os.path.join(app.static_folder, 'watermark_gen',output_filename)

    if not os.path.exists(os.path.join(app.static_folder, 'watermark_gen')):
        os.mkdir(os.path.join(app.static_folder, 'watermark_gen'))
    
    bwm1 = WaterMark(password_img=1, password_wm=1)
    bwm1.read_img(file_path)
    wm = text
    bwm1.read_wm(wm, mode='str')
    bwm1.embed(output_filepath)
    len_wm = len(bwm1.wm_bit)
    print(len_wm)
    # 模型运行


    image_url = request.host_url + 'watermark-gen/' + output_filename
    return jsonify({'image_path': image_url})




@app.route('/watermark-gen/<filename>')
def returnwatermarkGen(filename):
    return send_from_directory(os.path.join(app.static_folder,'watermark_gen'), filename)



@app.route('/watermark-attack', methods=['POST'])
def watermarkAttack():
    global len_wm;
    dic_path = os.path.join(app.static_folder, 'attack_origin')
    # 存储原始图片的目录
    if not os.path.exists(dic_path):
        os.mkdir(dic_path)
    #如果不存在，创建目录
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    #未找到的错误处理
    file = request.files['image']
    method = request.form.get('method')
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        filename = secure_filename(f"attack_origin_{uuid4().hex}.png")
        file_path = os.path.join(dic_path,filename)
        file.save(file_path)
        file.stream.seek(0)
        #将文件重命名并存储在定义的原始图片目录下
    else:
        return jsonify({'error': 'No such file'}), 400
    
    output_filename = secure_filename(f"watermark_attack_{uuid4().hex}.png")
    output_filepath = os.path.join(app.static_folder, 'watermark_attack',output_filename)

    if not os.path.exists(os.path.join(app.static_folder, 'watermark_attack')):
        os.mkdir(os.path.join(app.static_folder, 'watermark_attack'))
    
    print(method)

    if method == 'bright':
        AttackFunctions.bright_att(file_path,output_filepath)
        bwm1 = WaterMark(password_img=1, password_wm=1)
        wm_extract = bwm1.extract(output_filepath, wm_shape=len_wm, mode='str')
    elif method == 'shelter':
        AttackFunctions.shelter_att(file_path,output_filepath)
        bwm1 = WaterMark(password_img=1, password_wm=1)
        wm_extract = bwm1.extract(output_filepath, wm_shape=len_wm, mode='str')
    elif method == 'salt':
        AttackFunctions.salt_pepper_att(file_path,output_filepath)
        bwm1 = WaterMark(password_img=1, password_wm=1)
        wm_extract = bwm1.extract(output_filepath, wm_shape=len_wm, mode='str')
    elif method == 'rot':
        AttackFunctions.rot_att(file_path,output_filepath)
        bwm1 = WaterMark(password_img=1, password_wm=1)
        AttackFunctions.rot_att(output_filepath,output_filepath,angle=-45)
        wm_extract = bwm1.extract(output_filepath, wm_shape=len_wm, mode='str')
    else:
        bwm1 = WaterMark(password_img=1, password_wm=1)
        file.save(output_filepath)
        wm_extract = bwm1.extract(output_filepath, wm_shape=len_wm, mode='str')


    print(wm_extract)


    # 模型运行
    image_url = request.host_url + 'watermark-attack/' + output_filename
    return jsonify({'image_path': image_url,'text_detected': wm_extract})



@app.route('/watermark-attack/<filename>')
def returnAttack(filename):
    return send_from_directory(os.path.join(app.static_folder,'watermark_attack'), filename)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)






