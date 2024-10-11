---
title: Tiny Llama
emoji: 🌖
colorFrom: purple
colorTo: purple
sdk: docker
pinned: false
license: llama3.2
short_description: Llama 3.2 Instruct quantized
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference


# llama-summarizer
Summarization tool built with Llama


### Run the app locally:

~~~bash
docker build -t tiny-llama .

docker run -p 7860:7860 tiny-llama
~~~

### Making a request

~~~bash

curl -X POST "http://localhost:7860/llm_on_cpu" -H "Content-Type: application/json" -d '{"item": "hi"}'
~~~

Built with Llama.