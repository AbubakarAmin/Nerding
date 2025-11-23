# StudyEco - AI Powered Study Ecosystem

A comprehensive web application that combines AI-powered study tools with a beautiful dark theme interface. Built with Flask and Google Gemini AI.

## Features

### 🎯 Study Tools
- **AI Study Assistant**: Chat with AI for instant help on any subject
- **Quiz Generator**: Upload study materials and get AI-generated quizzes
- **Audiobook Creator**: Convert PDFs to audio using Gemini TTS

### 📚 Resources
- **Book Search**: Search books using Open Library API
- **Research Papers**: Find academic papers using Archive.org API
- **Music Player**: Local music files and online study music

### 📊 Planning & Tracking
- **Study Goals**: Set daily study time goals
- **Assignment Tracker**: Add assignments with due dates
- **Streak Counter**: Track your study streak
- **Progress Monitoring**: Visual progress tracking

### 🎨 Design
- **Dark Theme**: Beautiful dark color scheme
- **Responsive Design**: Works on all devices
- **Modern UI**: Clean, intuitive interface
- **Smooth Animations**: Engaging user experience

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd StudyEco
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key**
   - The Google Gemini API key is already configured in `app.py`
   - Make sure you have internet access for API calls

4. **Create necessary directories**
   ```bash
   mkdir static/music
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:5000`
   - Start studying!

## Usage

### Getting Started
1. **Select Subject**: Use the dropdown in the navbar to choose your current subject
2. **Set Goals**: Go to Goals section to set daily study time and add assignments
3. **Start Studying**: Use any of the study tools in the sidebar

### Study Tools
- **Study with AI**: Ask questions about any topic
- **Take Quiz**: Paste study material to generate quizzes
- **Create Audiobook**: Upload PDFs for audio conversion

### Resources
- **Books**: Search for books by title, author, or subject
- **Research Papers**: Find academic papers on any topic
- **Music**: Play local music files or online study music

## File Structure

```
StudyEco/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template with navbar/sidebar
│   ├── index.html        # Dashboard
│   ├── study_ai.html     # AI study assistant
│   ├── quiz.html         # Quiz generator
│   ├── audiobook.html    # Audiobook creator
│   ├── goals.html        # Goals and assignments
│   ├── music.html        # Music player
│   ├── books.html        # Book search
│   └── research.html     # Research papers
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── music/            # Local music files (add your own)
```

## API Integration

### Google Gemini AI
- Used for AI chat assistance
- Quiz generation from study materials
- Text-to-speech for audiobooks

### Open Library API
- Book search functionality
- Free access to book database

### Archive.org API
- Research paper search
- Academic content discovery

## Customization

### Adding Music Files
1. Add MP3, WAV, or M4A files to `static/music/` folder
2. Files will automatically appear in the Music section

### Modifying Subjects
- Edit the subject dropdown in `templates/base.html`
- Update the options in `app.py` if needed

### Styling
- Modify `static/css/style.css` for custom styling
- Color scheme uses CSS variables for easy theming

## Features Status

### ✅ Working Features
- AI Study Assistant (Gemini integration)
- Quiz Generator (Gemini integration)
- Book Search (Open Library API)
- Research Paper Search (Archive.org API)
- Music Player (local files)
- Responsive Design
- Dark Theme

### 🚧 Demo Features (Frontend Only)
- Audiobook Generation (UI ready, needs TTS implementation)
- Assignment Management (UI ready, needs backend)
- Streak Tracking (UI ready, needs backend)
- WhatsApp Reminders (UI ready, needs integration)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed description

---

**Happy Studying! 🎓**
