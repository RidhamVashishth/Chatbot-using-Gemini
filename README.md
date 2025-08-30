# **Gemini AI Multi-Modal Chatbot**

An interactive and intelligent chatbot built with Streamlit and powered by Google's Gemini 1.5 Flash model. This application can understand and respond to user queries, maintain conversation history, and analyze various uploaded file types for context-aware answers.

## **Overview**

This project is a versatile AI assistant designed to provide a seamless conversational experience. Users can engage in a natural chat dialogue, and the chatbot will remember the context of the conversation. Its key feature is the ability to ingest various file formats including images, PDFs, Word documents, PowerPoint presentations, and Excel spreadsheets, and answer specific questions based on the content of the uploaded file. This makes it a powerful tool for quickly summarizing, analyzing, and extracting information from documents without manual effort.

### **Core Features**

* **Conversational Memory**: The chatbot maintains a session-based chat history, allowing for follow-up questions and a natural flow of conversation.  
* **Multi-Modal Input**: Users can upload various file types to provide context for their questions:  
  * Images (.png, .jpg, .jpeg)  
  * Documents (.pdf, .docx)  
  * Presentations (.pptx)  
  * Spreadsheets (.xlsx)  
* **Dynamic Prompting**: The AI's behavior changes based on whether a file is provided.  
  * **With a file**: It acts as an expert assistant, answering questions strictly based on the document's content to prevent hallucination.  
  * **Without a file**: It functions as a general-purpose, friendly AI assistant using its broad knowledge base.  
* **Interactive UI**: A clean and user-friendly interface built with Streamlit, featuring a real-time chat display and a sidebar for file management.

## **Technology Stack**

* **Language**: Python  
* **Framework**: Streamlit  
* **AI Model**: Google Gemini (gemini-1.5-flash)  
* **Core Libraries**:  
  * google-generativeai for interacting with the Gemini API.  
  * Pillow for image processing.  
  * pypdf, python-docx, python-pptx, openpyxl for parsing various document formats.  
  * python-dotenv for managing environment variables.

## **Local Setup and Installation**

To run this project on your local machine, please follow these steps.

### **Prerequisites**

* Python 3.8 or higher.  
* A Google API Key with the Generative Language API enabled. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### **1\. Clone the Repository**

git clone \<your-repository-url\>  
cd \<repository-directory\>

### **2\. Create a Virtual Environment**

It is highly recommended to use a virtual environment to manage project dependencies.

\# For Windows  
python \-m venv venv  
venv\\Scripts\\activate

\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

### **3\. Install Dependencies**

Create a requirements.txt file in the root of your project with the following content, and then run the installation command.

**requirements.txt**:

streamlit  
google-generativeai  
python-dotenv  
Pillow  
pypdf  
python-docx  
python-pptx  
openpyxl

**Installation Command**:

pip install \-r requirements.txt

### **4\. Configure Environment Variables**

Create a file named .env in the root directory of your project and add your Google API key.

GOOGLE\_API\_KEY='YOUR\_API\_KEY\_HERE'

### **5\. Run the Application**

Launch the Streamlit app from your terminal.

streamlit run app.py

The application should now be running and accessible in your web browser.

## **How to Use the App**

1. **General Chat**: Simply type your question into the chat input at the bottom of the screen and press Enter.  
2. **Chat with a Document**:  
   * Use the sidebar to upload a supported file (Image, PDF, DOCX, etc.).  
   * Wait for the "File processed\!" success message to appear.  
   * Ask a question specifically about the content of the uploaded file in the chat input. The AI will use the document as the primary context for its answer.  
   * The file context is used for the next single question and then cleared, allowing you to continue a general conversation or upload a new file.