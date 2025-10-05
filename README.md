# 🚀 TalentScout AI Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://talentscout-chatbot-r1sh1l.streamlit.app/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenAI GPT-4](https://img.shields.io/badge/OpenAI-GPT--4-green.svg)](https://openai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A sophisticated AI-powered interview automation platform that streamlines technical candidate screening using OpenAI GPT-4 and Streamlit. Built for HR teams and hiring managers to conduct efficient, structured interviews with intelligent question generation.

## 🌐 Live Application

🔗 **Try it now**: [https://talentscout-chatbot-r1sh1l.streamlit.app/](https://talentscout-chatbot-r1sh1l.streamlit.app/)

📁 **Source Code**: [https://github.com/R1SH1L/TalentScout-Chatbot](https://github.com/R1SH1L/TalentScout-Chatbot)

## 📖 Overview

TalentScout revolutionizes the hiring process by automating initial technical interviews. The platform intelligently adapts to each candidate's technology stack, generating personalized questions and maintaining structured data collection for seamless HR evaluation.

### 🎯 Key Capabilities

| Feature | Description |
|---------|-------------|
| 🤖 **AI-Driven Interviews** | Dynamic question generation based on candidate's tech stack |
| 📊 **Structured Data Collection** | Organized CSV exports with questions and answers |
| 🔄 **Progressive Interview Flow** | Multi-stage process from basic info to technical assessment |
| ✅ **Real-time Validation** | Email, phone, and experience level validation |
| ☁️ **Cloud-Ready Architecture** | Built for seamless deployment and scalability |
| 📱 **Responsive Design** | Works perfectly on desktop and mobile devices |

## 🛠️ Getting Started

### Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed on your system
- **OpenAI API Key** (Get one at [platform.openai.com](https://platform.openai.com/api-keys))
- **Git** for version control

### 🔧 Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/R1SH1L/TalentScout-Chatbot.git
   cd TalentScout-Chatbot
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Launch Application**
   ```bash
   streamlit run app.py
   ```

   The application will open in your browser at `http://localhost:8501`

## 🚀 Quick Start Guide

### For Candidates
1. **Visit the Application**: Open [TalentScout Chatbot](https://talentscout-chatbot-r1sh1l.streamlit.app/)
2. **Provide Basic Information**: Fill in your personal and professional details
3. **Technical Assessment**: Answer AI-generated questions based on your tech stack
4. **Complete Interview**: Your responses are automatically saved for HR review

### For HR Teams
1. **Access Candidate Data**: Download structured CSV files with all responses
2. **Review Answers**: Questions and answers are organized for easy evaluation
3. **Make Decisions**: Use the comprehensive data to make informed hiring choices

## 🏗️ Architecture

### Project Structure
```
TalentScout-Chatbot/
├── app.py                 # Main Streamlit application
├── config.py             # Configuration management
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── core/
│   ├── chatbot_logic.py  # Interview flow and AI integration
│   ├── data_handler.py   # Data processing and CSV operations
│   └── prompt_templates.py # AI prompt engineering
└── data/
    └── candidate_data.csv # Interview responses storage
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Frontend** | Streamlit | Interactive web interface |
| **AI Engine** | OpenAI GPT-4o-mini | Question generation and processing |
| **Data Processing** | Pandas | CSV operations and data manipulation |
| **Configuration** | python-dotenv | Environment variable management |
| **Deployment** | Streamlit Cloud | Production hosting |

## 📊 Features in Detail

### 🔍 Interview Process Flow

1. **Information Collection Phase**
   - Personal details (name, email, phone)
   - Professional information (experience, position, location)
   - Technology stack assessment

2. **AI Question Generation**
   - Personalized questions based on candidate's tech stack
   - Difficulty adjusted to experience level
   - Industry-relevant technical assessments

3. **Response Collection**
   - Real-time answer recording
   - Progress tracking
   - Input validation and error handling

4. **Data Export**
   - Structured CSV generation
   - Download functionality for cloud deployments
   - HR-friendly format with questions and answers

### 🛡️ Data Validation

- **Email Validation**: RFC-compliant email format checking
- **Phone Validation**: International phone number format support
- **Experience Validation**: Logical experience level validation
- **Input Sanitization**: Prevention of malicious input

## 🌐 Deployment

### Streamlit Cloud (Recommended)

1. **Fork this repository** to your GitHub account
2. **Sign up** at [share.streamlit.io](https://share.streamlit.io)
3. **Connect your GitHub** account
4. **Deploy** using these settings:
   - Repository: `YourUsername/TalentScout-Chatbot`
   - Branch: `main`
   - Main file: `app.py`
5. **Add secrets** in Advanced Settings:
   ```
   OPENAI_API_KEY = "your_openai_api_key_here"
   ```

### Local Development

```bash
# Clone and setup
git clone https://github.com/R1SH1L/TalentScout-Chatbot.git
cd TalentScout-Chatbot
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
echo "OPENAI_API_KEY=your_key_here" > .env

# Run application
streamlit run app.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add type hints to all functions
- Include docstrings for all classes and methods
- Write tests for new features
- Update documentation as needed

## 📝 API Reference

### Core Classes

#### `TalentScoutChatbot`
Main chatbot class handling interview flow and AI integration.

```python
from core.chatbot_logic import TalentScoutChatbot

chatbot = TalentScoutChatbot()
chatbot.run_interview()
```

#### `DataHandler`
Manages data persistence and CSV operations.

```python
from core.data_handler import DataHandler

handler = DataHandler()
handler.save_candidate_data(candidate_info, qa_pairs)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 access | ✅ Yes | None |
| `OPENAI_MODEL` | OpenAI model to use | ❌ No | `gpt-4o-mini` |
| `MAX_QUESTIONS` | Maximum technical questions | ❌ No | `5` |

### Customization Options

- **Question Templates**: Modify `core/prompt_templates.py`
- **UI Styling**: Update Streamlit components in `app.py`
- **Data Schema**: Adjust CSV structure in `core/data_handler.py`

## 🐛 Troubleshooting

### Common Issues

**OpenAI API Error**
```
Solution: Verify your API key and check billing status
```

**Import Errors**
```
Solution: Ensure virtual environment is activated and dependencies installed
```

**Streamlit Port Issues**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

## 📊 Performance & Limitations

### Current Capabilities
- ✅ Handles 100+ concurrent users
- ✅ Supports 50+ programming languages/technologies
- ✅ Real-time response validation
- ✅ Cloud-scalable architecture

### Known Limitations
- API rate limits apply (OpenAI tier-dependent)
- Maximum 5 technical questions per interview
- CSV storage (database integration planned)

## 🔜 Roadmap

### Upcoming Features
- [ ] **Database Integration** (PostgreSQL/MongoDB)
- [ ] **Advanced Analytics** Dashboard
- [ ] **Multi-language Support**
- [ ] **Video Interview Integration**
- [ ] **AI Interview Scoring**
- [ ] **Candidate Ranking System**

### Version History
- **v1.0.0** - Initial release with core functionality
- **v1.1.0** - Added download functionality and cloud optimization
- **v1.2.0** - Enhanced UI and validation improvements

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**R1SH1L**
- GitHub: [@R1SH1L](https://github.com/R1SH1L)
- Project: [TalentScout-Chatbot](https://github.com/R1SH1L/TalentScout-Chatbot)

## 🙏 Acknowledgments

- [OpenAI](https://openai.com/) for GPT-4 API
- [Streamlit](https://streamlit.io/) for the amazing framework
- [Pandas](https://pandas.pydata.org/) for data manipulation
- The open-source community for inspiration and support

## 📞 Support

Having issues? Need help?

- 📧 **Issues**: [GitHub Issues](https://github.com/R1SH1L/TalentScout-Chatbot/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/R1SH1L/TalentScout-Chatbot/discussions)
- 🌐 **Live Demo**: [Try it now](https://talentscout-chatbot-r1sh1l.streamlit.app/)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ by [R1SH1L](https://github.com/R1SH1L)

</div>