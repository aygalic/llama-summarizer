const submitBtn = document.getElementById('submit-btn');
const inputArea = document.getElementById('input-area');
const outputArea = document.getElementById('output-area');

submitBtn.addEventListener('click', async function() {
    const input = inputArea.value;
    outputArea.textContent = 'Generating response...';

    try {
        const response = await fetch('/llm_on_cpu_stream', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ item: input }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        outputArea.textContent = '';

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const decodedChunk = decoder.decode(value, { stream: true });
            const lines = decodedChunk.split('\n\n');
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const token = line.slice(6);
                    outputArea.textContent += token;
                }
            }
        }
    } catch (error) {
        console.error('Error:', error);
        outputArea.textContent = 'An error occurred while fetching the response.';
    }
});