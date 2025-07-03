# CozyReader: AI-Powered Bedtime Story Generator for Kids

Storytelling has been an integral part of human history, shaping cultures and connecting generations. For children, bedtime stories are not just a source of entertainment but also a vital tool for cognitive development, language acquisition, and emotional bonding with parents. In today’s digital age, CozyReader brings the magic of storytelling to life with an AI-powered platform that generates customized bedtime stories tailored to your child's imagination.

## Why CozyReader?

Parents often struggle to come up with unique and engaging bedtime stories every night. Children love hearing tales about their favorite characters, fantastical places, and adventurous themes. CozyReader addresses this need by offering:

-   **Personalized Storytelling:** Choose characters, themes, and settings to craft a story that resonates with your child.
-   **AI-Powered Story Generation:** Leveraging cutting-edge generative AI, CozyReader creates original narratives on demand.
-   **Text-to-Speech (TTS) Narration:** Transform stories into audio for a seamless listening experience.
-   **Voice Cloning (Beta):** Narrate stories in the voice of famous personalities, making bedtime even more exciting.
-   **Story Management:** Save, retrieve, and delete your favorite stories and their audio narrations.
-   **User Authentication & Data Security:** Secure access via Streamlit Authenticator with all stories stored in CouchDB.

## How CozyReader Works

CozyReader is designed to be user-friendly and interactive. Here’s how you can create a magical bedtime story in just a few steps:

1.  **Log in or Sign Up:** Secure authentication ensures your stories are saved and accessible only to you.
2.  **Customize Your Story:**
    -   Select a genre (Fantasy, Adventure, Sci-Fi, etc.).
    -   Choose characters and environments.
    -   Provide custom names to personalize the story.
3.  **Generate & Listen:**
    -   CozyReader’s AI will instantly craft a unique story.
    -   Convert the text into speech using the built-in TTS model.
    -   Enable voice cloning for an immersive experience.
4.  **Save & Access Anytime:**
    -   Store your favorite stories and audio files for future bedtime sessions.

## Behind the Scenes: The Technology

CozyReader integrates multiple AI technologies to enhance storytelling:

-   **Generative AI Models:** AI-driven natural language generation ensures fresh and engaging stories every time.
-   **Google Cloud API:** Used for AI processing and optimization.
-   **Coqui TTS:** Provides high-quality, natural-sounding narration.
-   **CouchDB:** A robust NoSQL database for storing user data and generated stories securely.
-   **Streamlit:** A lightweight and interactive web interface for effortless story creation.

## Setting Up CozyReader

Want to try it out? Follow these simple steps to get started:

1.  **Clone the Repository**

    ```bash
    git clone <repository-url>
    cd CozyReader
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**

    Create a `.env` file inside `.config/` with the following details:

    ```
    GOOGLE_API_KEY=<your-google-api-key>
    COUCHDB_USER=<your-couchdb-username>
    COUCHDB_PASSWORD=<your-couchdb-password>
    COUCHDB_URL=<your-couchdb-url>
    ```

4.  **Run the Application**

    ```bash
    streamlit run app.py
    ```

    Now, open your browser and start creating magical stories!

## The Future of CozyReader

I envision CozyReader evolving into a comprehensive storytelling platform with exciting features such as:

-   **Multi-Language Support:** Generate and narrate stories in different languages.
-   **Illustrated Storybooks:** AI-generated illustrations accompanying each story.
