# RAG-Based Chatbot for Syrian Universities' Informatics Engineering

A Retrieval-Augmented Generation (RAG) chatbot designed to assist with queries related to Informatics Engineering at Syrian universities. The system leverages a knowledge base of bilingual (English and Arabic) documents to provide accurate, context-aware responses. It supports both terminal-based interaction and a web-based user interface powered by Streamlit.

## Features

- **Bilingual Support**: Automatically detects and responds in English or Arabic based on user input.
- **RAG Architecture**: Combines retrieval from a pre-built vector store with generative AI for precise answers.
- **Evaluation System**: Provides confidence scores and reasoning for each response.
- **Web UI**: Interactive chat interface with a custom Syrian-inspired visual theme.
- **Terminal Interface**: Command-line interaction for quick queries.
- **Modular Design**: Core logic separated into agent and tool modules for easy extension.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd rag_agent_chatbot
   ```

2. **Create a Virtual Environment** (recommended):
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Note: Ensure `streamlit` is installed if not included in `requirements.txt`:
   ```bash
   pip install streamlit
   ```

4. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory.
   - Add your Hugging Face API key:
     ```
     HUGGINGFACE_API_KEY=your_api_key_here
     ```
   - Obtain an API key from [Hugging Face](https://huggingface.co/settings/tokens).

5. **Prepare the Knowledge Base**:
   - Ensure the data file `data/Syrian_Universities_IT_KB_Bilingual.txt` is present.
   - Run preprocessing if needed (refer to `rag/preprocess.py` for details).

## How to Run

### Web UI (Recommended)
Launch the interactive web interface using Streamlit:
```bash
streamlit run app.py
```
- Open the provided URL in your browser.
- Enter queries in English or Arabic; the chatbot will respond accordingly.
- Features include chat history, language toggle, and response evaluation.

### Terminal Interface
For command-line interaction:
```bash
python main.py
```
- Follow the prompts to enter questions.
- Type `exit` to quit.
- Responses include answers and evaluations in the detected language.

## Project Structure

- `app.py`: Main Streamlit application for the web-based chat interface.
- `main.py`: Entry point for terminal-based interaction.
- `agent/`: Core agent logic.
  - `agent.py`: Defines the `SimpleAgent` class and the `ask` method.
  - `tools.py`: Utility functions for retrieval, answering, and evaluation.
- `rag/`: Retrieval-Augmented Generation components.
  - `preprocess.py`: Handles data preprocessing and vector store creation.
  - `retriever.py`: Manages document retrieval from the vector store.
  - `vector_store.py`: Interfaces with FAISS for vector storage.
- `data/`: Knowledge base files.
  - `Syrian_Universities_IT_KB_Bilingual.txt`: Bilingual dataset for Informatics Engineering.
- `embeddings/`: Directory for storing generated embeddings.
- `utils.py`: Helper functions, including language detection.
- `requirements.txt`: Python dependencies.
- `README.md`: This file.

## Visual Identity

The application adopts a Syrian-inspired visual theme, drawing from national identity elements:
- **Color Palette**: Dark backgrounds (`#161616`) with gold accents (`#b9a779`) for headers and highlights, evoking traditional Syrian aesthetics.
- **Typography**: Uses the 'Cairo' font family for a modern, readable Arabic-friendly design.
- **UI Elements**: Rounded cards, subtle shadows, and progress bars for evaluations, maintaining a professional yet culturally resonant look.
- **Icons**: Emojis like 🎓 for educational context.

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch.
3. Make your changes and test thoroughly.
4. Submit a pull request with a clear description.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with [Hugging Face Transformers](https://huggingface.co/) for generative AI.
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss).
- Web UI via [Streamlit](https://streamlit.io/).