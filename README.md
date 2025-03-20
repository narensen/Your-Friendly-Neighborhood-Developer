![Screenshot from 2025-03-21 00-15-45](https://github.com/user-attachments/assets/703f612b-a2ff-48dc-8714-1c618181f8eb)

A powerful tool to generate robust FastAPI backend code (and optional frontend) with ease. Built with Python, FastAPI, and AI-driven code generation, this project streamlines development by creating efficient, debugged, and production-ready code based on natural language prompts.

## Features
- **Backend Generation**: Creates optimized FastAPI backend code tailored to your prompt.
- **Full-Stack Option**: Optionally generates a single-file HTML/CSS frontend to complement the backend.
- **AI-Powered**: Leverages advanced language models for code generation, planning, and debugging.
- **Fast & Flexible**: Built with FastAPI for high performance and easy customization.
- **Downloadable Output**: Saves generated code to `downloads/` for immediate use.

## How It Works
1. Send a prompt to the `/generate` endpoint describing your desired backend functionality.
2. The system generates a plan, writes the code, debugs it, and returns the result.
3. Optionally request full-stack generation to get a matching frontend.
4. Access the polished code via the API response or download it from the `downloads/` directory.

![Screenshot from 2025-03-21 00-35-56](https://github.com/user-attachments/assets/51b0fb7c-41f2-41d6-b593-192cb861d3c8)


## Installation

### Using Git Bash
Follow these steps to set up the project locally using Git Bash:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/narensen/your-friendly-neighborhood-developer.git
   cd your-friendly-neighborhood-developer

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Set up your environment:**
   ```bash
   GROQ_API_KEY=your-api-key-here

![Screenshot from 2025-03-21 00-36-04](https://github.com/user-attachments/assets/d1543126-5421-476b-a546-88b0fe456bec)

