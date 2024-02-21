#ChatPilot
##Description

This Django project utilizes LangChain and VectorDB for text processing and searching functionalities. It includes APIs for processing PDF documents and searching for relevant documents based on user queries.
##Installation

    Clone the repository.
    Install dependencies using pip install -r requirements.txt.
    Set up environment variables for OPENAI_API_KEY and QDRANT_API_KEY.
    

##Usage

    Run the Django development server using python manage.py runserver.
    Use the /process-pdf endpoint to upload PDF documents. Example: POST /process-pdf with JSON payload {"file_url": "https://example.com/document.pdf"}.
    Use the /search endpoint to search query in documents. Example: GET /search?query=search_query_here.

##Technologies Used

    Django
    LangChain
    VectorDB (Qdrant)
    OpenAI
