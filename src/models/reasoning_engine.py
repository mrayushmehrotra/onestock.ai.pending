from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ReasoningModel:
    """
    Handles model selection and local inference for stock reasoning.
    Target: SmolLM-135M-Instruct or Phi-3-mini
    """
    
    def __init__(self, model_id: str = "HuggingFaceTB/SmolLM-135M-Instruct"):
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = None
        self.model = None

    def load(self):
        print(f"Loading model {self.model_id} on {self.device}...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

    def generate_reasoning(self, prompt: str) -> str:
        if not self.model:
            # Fallback mock for development
            return "THOUGHT: Analyzing context. PREDICTION: Neutral."

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(**inputs, max_new_tokens=200)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

if __name__ == "__main__":
    reasoning = ReasoningModel()
    # reasoning.load()
    print(reasoning.generate_reasoning("News: Nifty hits high. Season: Summer."))
