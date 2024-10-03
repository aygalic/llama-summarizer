import torch
from pathlib import Path


THIS_DIR = Path(__file__).parent.resolve()



model = torch.load('/Users/aygalic/github/llama-summarizer/Llama3.2-1B-Instruct/consolidated.00.pth', map_location=torch.device('mps') )

breakpoint()
model.eval()


breakpoint()