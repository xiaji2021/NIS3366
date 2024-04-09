# 功能：定义了STABLE_DIFFUSION类
# generate_image 函数用于文生图任务，同时支持调整 height, width, num_inference_steps, guidance_scale, seed 等参数

from PIL import Image
import torch
from transformers import CLIPTextModel, CLIPTokenizer
from diffusers import AutoencoderKL, UNet2DConditionModel, PNDMScheduler

class STABLE_DIFFUSION:
    def __init__(self):
        # 初始化模型
        self.vae = AutoencoderKL.from_pretrained("/root/model/stable-diffusion-v1-5", subfolder="vae", use_safetensors=True)
        self.tokenizer = CLIPTokenizer.from_pretrained("/root/model/stable-diffusion-v1-5", subfolder="tokenizer")
        self.text_encoder = CLIPTextModel.from_pretrained(
            "/root/model/stable-diffusion-v1-5", subfolder="text_encoder", use_safetensors=True
        )
        self.unet = UNet2DConditionModel.from_pretrained(
            "/root/model/stable-diffusion-v1-5", subfolder="unet", use_safetensors=True
        )
        from diffusers import UniPCMultistepScheduler
        self.scheduler = UniPCMultistepScheduler.from_pretrained("/root/model/stable-diffusion-v1-5", subfolder="scheduler")

        # 模型转移到cuda中
        self.torch_device = "cuda:0"
        self.vae.to(self.torch_device)
        self.text_encoder.to(self.torch_device)
        self.unet.to(self.torch_device)

    def generate_image(
        self,
        prompt, # 对图片的文字描述
        save_path, # 生成的图片的路径
        height = 512,  # default height of Stable Diffusion
        width = 512,  # default width of Stable Diffusion
        num_inference_steps = 25,  # Number of denoising steps
        guidance_scale = 7.5,  # Scale for classifier-free guidance
        seed = 0, # default random seed
    ):
    
        # 生成文本embeddings
        prompt = [prompt]

        self.generator = torch._C.Generator(device = self.torch_device)
        self.generator.manual_seed(seed)  # Seed generator to create the initial latent noise
        batch_size = len(prompt)

        text_input = self.tokenizer(
            prompt, padding="max_length", max_length=self.tokenizer.model_max_length, truncation=True, return_tensors="pt"
        )

        with torch.no_grad():
            text_embeddings = self.text_encoder(text_input.input_ids.to(self.torch_device))[0]

        max_length = text_input.input_ids.shape[-1]
        uncond_input = self.tokenizer([""] * batch_size, padding="max_length", max_length=max_length, return_tensors="pt")
        uncond_embeddings = self.text_encoder(uncond_input.input_ids.to(self.torch_device))[0]

        text_embeddings = torch.cat([uncond_embeddings, text_embeddings])

        # 生成随机噪声
        latents = torch.randn(
            (batch_size, self.unet.config.in_channels, height // 8, width // 8),
            generator=self.generator,
            device=self.torch_device,
        )

        # 给图片去噪
        latents = latents * self.scheduler.init_noise_sigma

        from tqdm.auto import tqdm

        self.scheduler.set_timesteps(num_inference_steps)

        for t in tqdm(self.scheduler.timesteps):
            # expand the latents if we are doing classifier-free guidance to avoid doing two forward passes.
            latent_model_input = torch.cat([latents] * 2)

            latent_model_input = self.scheduler.scale_model_input(latent_model_input, timestep=t)

            # predict the noise residual
            with torch.no_grad():
                noise_pred = self.unet(latent_model_input, t, encoder_hidden_states=text_embeddings).sample

            # perform guidance
            noise_pred_uncond, noise_pred_text = noise_pred.chunk(2)
            noise_pred = noise_pred_uncond + guidance_scale * (noise_pred_text - noise_pred_uncond)

            # compute the previous noisy sample x_t -> x_t-1
            latents = self.scheduler.step(noise_pred, t, latents).prev_sample


        # 图片译码
        # scale and decode the image latents with vae
        latents = 1 / 0.18215 * latents
        with torch.no_grad():
            image = self.vae.decode(latents).sample

        image = (image / 2 + 0.5).clamp(0, 1).squeeze()
        image = (image.permute(1, 2, 0) * 255).to(torch.uint8).cpu().numpy()
        image = Image.fromarray(image)
        image.save(save_path)


if __name__ == "__main__":
    model = STABLE_DIFFUSION()
    model.generate_image("a photograph of an astronaut riding a pig","a photograph of an astronaut riding a pig.jpg",seed=1)