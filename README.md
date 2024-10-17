---
title: Tiny Llama
emoji: 🌖
colorFrom: purple
colorTo: purple
sdk: docker
pinned: false
license: llama3.2
short_description: Llama 3.2 1B Instruct quantized
---

# llama-superlight

Summarization and chatbot tool built with Llama

### Model detail:

- Model Llama 3.2 1B Instruct
- Quantized with [llama.cpp](https://github.com/ggerganov/llama.cpp)

### Run the app locally:

~~~bash
docker build -t tiny-llama .

docker run -p 7860:7860 tiny-llama
~~~

### Making a summary request

~~~bash

curl -X POST "http://localhost:7860/llm_on_cpu" -H "Content-Type: application/json" -d '{"item": "hi"}'
~~~

### Chat Bot web interface: 

Available at http://0.0.0.0:7860 when running locally with docker.

Or live on [Hugging Face Spaces](https://huggingface.co/spaces/aygalic/tiny-llama)

##### TODO 
- Add fine tuning pipeline using LoRA

Built with Llama.