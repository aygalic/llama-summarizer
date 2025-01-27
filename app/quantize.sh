#!/bin/sh
mkdir -p ./models

#Download model

huggingface-cli download "meta-llama/Llama-3.2-1B-Instruct" --local-dir "./models" --include "*"

#Convert to GGUF
python /Users/aygalic/github/llama.cpp/convert_hf_to_gguf.py ./models

#Quantize and save model
llama-quantize ./models/Models-1.2B-F16.gguf ./models/Q4_K_M.gguf Q4_K_M


