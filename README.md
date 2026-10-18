# ListingWriter

AI listing writer for Nigerian real estate agents. Type the property details once and get:

- a full property listing
- a short WhatsApp broadcast message
- an Instagram caption with hashtags

Languages: English, Nigerian Pidgin, and Hausa (beta).

Built for the Hacktoberfest Open-Source AI Challenge (Side Hustle theme).

## Why open-source AI

- **No per-use cost.** It runs on the agent's own computer with Ollama and Gemma, so there is no API bill that grows with every listing.
- **Private.** Property and client details never leave the device.
- **Works with weak internet.** After setup, writing needs no connection.

## Run it

1. Install Ollama: https://ollama.com/download
2. Start Ollama and download the model:

        ollama serve
        ollama pull gemma4:e2b-it-qat

3. In a second terminal, install and start the app:

        python3 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        python app.py

4. Open http://127.0.0.1:7860

A computer with 8 GB RAM is enough for gemma4:e2b-it-qat. For better writing, change `MODEL` in `app.py` to `gemma3:4b` if your computer has more memory.

## Pricing idea

- Free: 5 listings per month
- Agent: 5,000 naira per month, unlimited listings
- Agency: 15,000 naira per month for up to 5 agents

## Known limits

- Pidgin and Hausa come from a small model and can contain mistakes. Always read a post before sharing it.
- Writing is slow on computers without a GPU.

## Roadmap

- Better Hausa and Yoruba
- Listing history
- Export posts as images

## License

MIT
