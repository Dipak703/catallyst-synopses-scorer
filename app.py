import os
import tempfile
from anonymizer import anonymize_text
from parser import parse_file
from scorer import evaluate_synopsis
from together import Together
import together
from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import shutil

load_dotenv()
together.api_key = os.getenv("TOGETHER_API_KEY")
app = FastAPI()
client = Together()

templates = Jinja2Templates(directory="templates")

def feed(inp):
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "user", "content": inp}],
        system='''You are a helpful assistant evaluating the quality of a synopsis compared to its corresponding article. You have already received anonymized versions of both texts. Your task is to provide short, constructive feedback (2–3 sentences) focusing on the following dimensions:
Content Coverage: Does the synopsis capture the main ideas of the article?
Clarity: Is the synopsis easy to understand and well-articulated?
Coherence: Do the sentences in the synopsis logically flow from one to the next?
Do not repeat the article or synopsis. Your feedback should be concise, professional, and encourage improvement if needed. Avoid generic praise. If the synopsis is excellent, note the strengths specifically. If it lacks certain qualities, mention them tactfully.
You must not include any sensitive, personal, or identifiable information in the feedback.'''
    )
    return response.choices[0].message.content


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def evaluate(request: Request, 
                   article: UploadFile = File(...), 
                   synopsis: UploadFile = File(...), 
                   password: str = Form(...)):
    result = None
    feedback = None
    error = None

    if password != "1234":
        error = "Wrong password. Please try again."
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": error
        })

    try:
        article_ext = os.path.splitext(article.filename)[1]
        synopsis_ext = os.path.splitext(synopsis.filename)[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=article_ext) as temp_article:
            shutil.copyfileobj(article.file, temp_article)
            article_path = temp_article.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=synopsis_ext) as temp_synopsis:
            shutil.copyfileobj(synopsis.file, temp_synopsis)
            synopsis_path = temp_synopsis.name

        txt1 = parse_file(article_path)
        txt2 = parse_file(synopsis_path)
        
        article_text = anonymize_text(txt1)
        synopsis_text = anonymize_text(txt2)

        result = evaluate_synopsis(article_text, synopsis_text)
        feedback = feed(f'''The following is an anonymized article and its corresponding synopsis. Based on the comparison between the two, generate a short, 2–3 sentence feedback focusing on content coverage, clarity, and coherence. Do not quote or repeat the original texts. Keep your feedback professional, specific, and constructive.
Anonymized Article:{article_text}
Anonymized Synopsis:{synopsis_text}
score:{result}   ''')# generating feed back from the llama 3.3 70 B model running on toegtherai plateform
        # feedback ='feedback'

    except Exception as e:
        error = str(e)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
        "feedback": feedback,
        "error": error
    })


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
