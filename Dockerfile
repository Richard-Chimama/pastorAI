FROM ubuntu:22.04

# Install dependencies
RUN apt update && apt install -y curl

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Expose the default Ollama API port
EXPOSE 11434

# Start Ollama when the container runs
CMD ["ollama", "serve"]
