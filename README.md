# Meowy - The Cat Chatbot

## Overview

Meowy is a cat chatbot designed to boost motivation by providing users with adorable cat images on demand. The chatbot integrates the OpenAI Assistant API and CatAPI to respond to user requests for different cat breeds and allows a customizable number of images. This project includes both backend and frontend components, leveraging modern web development tools to provide a smooth user experience.

## Features

1. **Cat Image Requests**: Users can ask the chatbot to show images of cats. Requests can specify a certain breed or just show random cats.
2. **Multiple Image Support**: Users can request more than one cat image in a single query. The chatbot can display up to 100 images at a time.
3. **Engaging Conversations**: The chatbot maintains a friendly and engaging tone while fetching and displaying cat images.
4. **Fallback for Invalid Breeds**: If a breed is not recognized, the chatbot will still respond with random cat images.
5. **Bonus Feature**: The chatbot can fetch images based on a specific breed and the number of images requested by the user.

### Not Implemented

- **Real-time Streaming Output**: Streaming responses to the UI are not yet implemented.

## Tech Stack

- **Backend**:

  - FastAPI
  - OpenAI Assistant API
  - CatAPI

- **Frontend**:
  - Next.js
  - TypeScript
  - React
  - `ui.shadcn.com` for UI components
  - `llm-ui-kit` for additional UI elements

## How It Works

### Backend

1. **API Integration**: The FastAPI backend handles requests to the OpenAI Assistant API. It processes user inputs and forwards them to the Assistant for conversational responses.
2. **CatAPI Integration**: When the user asks for cat images, the backend calls CatAPI to fetch the requested images (with options for breed and number).

### Frontend

1. **User Input**: Users can type in requests for cat images via a text input field.
2. **Displaying Conversations**: Conversations between the user and the chatbot are displayed in a scrollable UI, mimicking typical chatbot interactions.
3. **Image Display**: Cat images fetched from CatAPI are displayed dynamically in the conversation flow based on user requests.

## Installation and Setup

### Prerequisites

1. **OpenAI API Key**: Create an account at [OpenAI](https://beta.openai.com/signup/), and get your API key.
2. **CatAPI Key**: Register for an API key at [CatAPI](https://thecatapi.com/signup).
3. **Node.js**: Install Node.js from [here](https://nodejs.org/).
4. **Python**: Install Python 3.8+ from [here](https://www.python.org/).

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/meowy.git
   cd meowy
   ```

2. Create a `.env` file with your obtained **OpenAI API Key** and **CatAPI Key**, and place it in the `backend` directory.
3. Run the following lines in the root directory to start the app:

   ```bash
   docker compose build
   docker compose up
   ```

4. To stop the app, run the following line of code:

   ```bash
   docker compose down
   ```

### API Endpoints

- **POST /api/chat**: Sends a user input to the OpenAI Assistant API and returns a response, possibly with cat images.
- **GET /api/chat-history/**: Obtains the chat history of the user's current session, which is linked to the user's cookie.
