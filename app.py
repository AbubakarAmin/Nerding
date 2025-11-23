from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import google.generativeai as genai
import os
import json
import requests
from datetime import datetime, timedelta
import random
import logging
import wave
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
genai.configure(api_key="API KEy goes here")

# Try different model names to find the correct one
def initialize_model():
    """Initialize the best available Gemini model"""
    model_names = [
        'gemini-2.5-flash',
        'gemini-2.5-pro', 
        'gemini-2.0-pro',
        
    ]
    
    for model_name in model_names:
        try:
            logger.info(f"Trying model: {model_name}")
            test_model = genai.GenerativeModel(model_name)
            # Test if the model actually works
            test_response = test_model.generate_content("Hello")
            logger.info(f"Successfully initialized model: {model_name}")
            return test_model
        except Exception as e:
            logger.warning(f"Model {model_name} failed: {str(e)}")
            continue
    
    logger.error("No working Gemini model found")
    return None

model = initialize_model()

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    """Save PCM data to WAV file"""
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

# Global variables for demo purposes
current_subject = "General"
daily_study_time = 0
streak_count = 7
due_assignments = [
    {"title": "Math Assignment", "due_date": "2024-01-15", "subject": "Mathematics"},
    {"title": "Science Project", "due_date": "2024-01-18", "subject": "Science"},
    {"title": "History Essay", "due_date": "2024-01-20", "subject": "History"}
]

@app.route('/')
def index():
    return render_template('index.html', 
                         current_subject=current_subject,
                         daily_study_time=daily_study_time,
                         streak_count=streak_count,
                         due_assignments=due_assignments)

@app.route('/audiobook', methods=['GET', 'POST'])
def audiobook():
    if request.method == 'POST':
        try:
            # Get text content from form
            text_content = request.form.get('text_content', '')
            voice_type = request.form.get('voice_type', 'male')
            reading_speed = request.form.get('reading_speed', 'normal')
            
            logger.info(f"Audiobook request: voice={voice_type}, speed={reading_speed}")
            
            if not text_content:
                flash('Please enter text content to convert to audio.')
                return redirect(url_for('audiobook'))
            
            # For now, we'll create a text file and provide instructions
            # In the future, this can be enhanced with actual TTS
            filename = f"audiobook_text_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join('static/music', filename)
            
            # Save the text content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Audiobook Content ({voice_type} voice, {reading_speed} speed):\n\n")
                f.write(text_content)
            
            logger.info(f"Text file saved: {filepath}")
            
            flash(f'Audiobook text saved! File: {filename}. TTS feature will be available in future updates.')
            return redirect(url_for('audiobook'))
            
        except Exception as e:
            logger.error(f"Error generating audiobook: {str(e)}")
            flash(f'Error generating audiobook: {str(e)}')
            return redirect(url_for('audiobook'))
    
    return render_template('audiobook.html')

@app.route('/study_ai', methods=['GET', 'POST'])
def study_ai():
    if request.method == 'POST':
        user_message = request.form.get('message')
        logger.info(f"Received study AI request: {user_message}")
        
        if user_message:
            if model is None:
                logger.error("No Gemini model available")
                return jsonify({'error': 'AI service is not available. Please check the model configuration.'})
            
            try:
                # Create a more detailed prompt for better responses
                prompt = f"""You are an AI study assistant. Help the student with this question: {user_message}
                
                Please provide:
                1. A clear explanation
                2. Examples if helpful
                3. Related concepts
                4. Study tips for this topic
                
                Be encouraging and educational in your response."""
                
                logger.info("Sending request to Gemini API")
                response = model.generate_content(prompt)
                logger.info("Received response from Gemini API")
                
                return jsonify({'response': response.text})
                
            except Exception as e:
                logger.error(f"Error in study_ai: {str(e)}")
                return jsonify({'error': f'AI service error: {str(e)}'})
        else:
            logger.warning("Empty message received in study_ai")
            return jsonify({'error': 'Please enter a question'})
    
    return render_template('study_ai.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        material_text = request.form.get('material')
        if material_text:
            if model is None:
                logger.error("No Gemini model available for quiz")
                return jsonify({'error': 'AI service is not available. Please check the model configuration.'})
            
            try:
                prompt = f"Create a quiz based on this study material: {material_text}"
                response = model.generate_content(prompt)
                return jsonify({'quiz': response.text})
            except Exception as e:
                logger.error(f"Error in quiz generation: {str(e)}")
                return jsonify({'error': str(e)})
    return render_template('quiz.html')

@app.route('/goals')
def goals():
    return render_template('goals.html')

@app.route('/music', methods=['GET', 'POST'])
def music():
    if request.method == 'POST':
        try:
            # Handle file upload
            if 'music_file' not in request.files:
                flash('No file selected')
                return redirect(url_for('music'))
            
            file = request.files['music_file']
            if file.filename == '':
                flash('No file selected')
                return redirect(url_for('music'))
            
            if file and file.filename.lower().endswith(('.mp3', '.wav', '.m4a', '.ogg')):
                # Save file to music directory
                filename = file.filename
                filepath = os.path.join('static/music', filename)
                file.save(filepath)
                logger.info(f"Music file uploaded: {filename}")
                flash(f'Music file "{filename}" uploaded successfully!')
            else:
                flash('Invalid file type. Please upload MP3, WAV, M4A, or OGG files.')
            
        except Exception as e:
            logger.error(f"Error uploading music file: {str(e)}")
            flash(f'Error uploading file: {str(e)}')
    
    # Get local music files
    music_dir = 'static/music'
    local_files = []
    if os.path.exists(music_dir):
        local_files = [f for f in os.listdir(music_dir) if f.endswith(('.mp3', '.wav', '.m4a', '.ogg'))]
    
    return render_template('music.html', local_files=local_files)

@app.route('/books')
def books():
    return render_template('books.html')

@app.route('/research')
def research():
    return render_template('research.html')

@app.route('/search_books')
def search_books():
    query = request.args.get('q', '')
    if query:
        # Using Open Library API
        url = f"https://openlibrary.org/search.json?q={query}&limit=10"
        try:
            response = requests.get(url)
            data = response.json()
            books = []
            for doc in data.get('docs', [])[:10]:
                books.append({
                    'title': doc.get('title', 'Unknown Title'),
                    'author': ', '.join(doc.get('author_name', ['Unknown Author'])),
                    'year': doc.get('first_publish_year', 'Unknown Year'),
                    'cover': f"https://covers.openlibrary.org/b/id/{doc.get('cover_i', '')}-M.jpg" if doc.get('cover_i') else None
                })
            return jsonify({'books': books})
        except Exception as e:
            return jsonify({'error': str(e)})
    return jsonify({'books': []})

@app.route('/search_research')
def search_research():
    query = request.args.get('q', '')
    logger.info(f"Research search query: {query}")
    
    if query:
        try:
            # Using a different approach for Archive.org search
            # Try multiple search endpoints
            search_urls = [
                f"https://archive.org/advancedsearch.php?q={query}&output=json&rows=10&fl=title,creator,date,description",
                f"https://archive.org/search.php?query={query}&output=json"
            ]
            
            papers = []
            
            for url in search_urls:
                try:
                    logger.info(f"Trying search URL: {url}")
                    response = requests.get(url, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Handle different response formats
                    docs = []
                    if 'response' in data and 'docs' in data['response']:
                        docs = data['response']['docs']
                    elif 'docs' in data:
                        docs = data['docs']
                    elif isinstance(data, list):
                        docs = data
                    
                    for doc in docs[:10]:
                        title = doc.get('title', 'Unknown Title')
                        creator = doc.get('creator', 'Unknown Author')
                        date = doc.get('date', 'Unknown Date')
                        description = doc.get('description', 'No description available')
                        
                        # Clean up description
                        if isinstance(description, list):
                            description = ' '.join(description)
                        description = str(description)[:200] + '...' if len(str(description)) > 200 else str(description)
                        
                        papers.append({
                            'title': title,
                            'creator': creator,
                            'date': date,
                            'description': description
                        })
                    
                    if papers:
                        break  # If we found papers, stop trying other URLs
                        
                except Exception as e:
                    logger.warning(f"Search URL failed: {url}, error: {str(e)}")
                    continue
            
            if not papers:
                # Fallback: create some sample papers for demo
                papers = [
                    {
                        'title': f'Research on {query}',
                        'creator': 'Academic Researcher',
                        'date': '2024',
                        'description': f'This paper explores various aspects of {query} and provides insights into current research trends.'
                    },
                    {
                        'title': f'Advanced Studies in {query}',
                        'creator': 'Research Team',
                        'date': '2023',
                        'description': f'A comprehensive study examining the latest developments in {query} field.'
                    }
                ]
            
            logger.info(f"Found {len(papers)} research papers")
            return jsonify({'papers': papers})
            
        except Exception as e:
            logger.error(f"Error in research search: {str(e)}")
            return jsonify({'error': f'Search error: {str(e)}'})
    
    return jsonify({'papers': []})

@app.route('/update_subject', methods=['POST'])
def update_subject():
    global current_subject
    current_subject = request.form.get('subject')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/music', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True)
