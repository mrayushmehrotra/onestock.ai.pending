"""
Model Downloader for AI Fine-Tuning Phase
Downloads and sets up SmolLM/Phi-3 models for fine-tuning
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig
from huggingface_hub import snapshot_download
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelDownloader:
    def __init__(self, model_cache_dir: str = "models"):
        self.model_cache_dir = model_cache_dir
        os.makedirs(model_cache_dir, exist_ok=True)
        
    def download_phi3_mini(self):
        """Download Phi-3-mini-4k-instruct model"""
        model_name = "microsoft/Phi-3-mini-4k-instruct"
        model_path = os.path.join(self.model_cache_dir, "phi3-mini")
        
        if os.path.exists(model_path):
            logger.info(f"Phi-3-mini model already exists at {model_path}")
            return model_path
            
        logger.info(f"Downloading {model_name}...")
        try:
            snapshot_download(
                repo_id=model_name,
                local_dir=model_path,
                local_dir_use_symlinks=False
            )
            logger.info(f"Successfully downloaded Phi-3-mini to {model_path}")
            return model_path
        except Exception as e:
            logger.error(f"Failed to download Phi-3-mini: {e}")
            raise
    
    def download_smollm(self):
        """Download SmolLM-135M model"""
        model_name = "HuggingFaceTB/SmolLM-135M"
        model_path = os.path.join(self.model_cache_dir, "smollm-135m")
        
        if os.path.exists(model_path):
            logger.info(f"SmolLM-135M model already exists at {model_path}")
            return model_path
            
        logger.info(f"Downloading {model_name}...")
        try:
            snapshot_download(
                repo_id=model_name,
                local_dir=model_path,
                local_dir_use_symlinks=False
            )
            logger.info(f"Successfully downloaded SmolLM-135M to {model_path}")
            return model_path
        except Exception as e:
            logger.error(f"Failed to download SmolLM-135M: {e}")
            raise
    
    def load_model(self, model_path: str, device: str = "auto"):
        """Load model and tokenizer"""
        if device == "auto":
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
        logger.info(f"Loading model from {model_path} on {device}")
        
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_path)
            model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                low_cpu_mem_usage=True
            )
            
            if device == "cpu":
                model = model.to(device)
                
            logger.info("Model loaded successfully")
            return model, tokenizer
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def test_model(self, model, tokenizer, prompt: str = "Hello, how are you?"):
        """Test model inference"""
        try:
            inputs = tokenizer(prompt, return_tensors="pt")
            if torch.cuda.is_available():
                inputs = {k: v.to(model.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=50,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id
                )
            
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
            logger.info(f"Model test successful. Response: {response}")
            return response
        except Exception as e:
            logger.error(f"Model test failed: {e}")
            raise

if __name__ == "__main__":
    downloader = ModelDownloader()
    
    # Download Phi-3-mini (recommended for better reasoning)
    phi3_path = downloader.download_phi3_mini()
    model, tokenizer = downloader.load_model(phi3_path)
    downloader.test_model(model, tokenizer)
    
    # Alternative: Download SmolLM-135M (smaller, faster)
    # smollm_path = downloader.download_smollm()
    # model, tokenizer = downloader.load_model(smollm_path)
    # downloader.test_model(model, tokenizer)
