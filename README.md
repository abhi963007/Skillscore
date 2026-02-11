# SkillScore - Academic & Placement Readiness Analyzer

A comprehensive full-stack web application designed to assess and analyze students' academic performance and placement readiness through automated evaluation and skill scoring.

## 🚀 Features

### **Multi-Role System**
- **Admin**: User management, system settings, audit logs
- **Teacher**: Exam creation, note uploads, result analysis
- **Student**: Exam taking, profile management, learning resources

### **Core Functionality**
- **Automated MCQ Generation**: Generate questions from uploaded text files using NLP
- **Skill Assessment**: Weighted scoring across aptitude, technical, and verbal skills
- **Placement Readiness**: Automated placement status recommendations
- **Secure Authentication**: Role-based access control with password protection
- **Result Analytics**: Comprehensive performance tracking and reporting

## 🛠️ Tech Stack

### **Backend**
- **Python Flask**: Primary web framework
- **Node.js/Express**: Evaluation and result processing
- **SQLite**: User data storage
- **MySQL**: Exam and results database
- **NLTK**: Natural Language Processing for MCQ generation

### **Frontend**
- **Bootstrap 4**: Responsive UI framework
- **jQuery**: JavaScript interactions
- **Jinja2**: Template engine
- **AOS**: Scroll animations
- **Owl Carousel**: Image sliders

## 📋 Prerequisites

- Python 3.7+
- Node.js 14+
- MySQL Server
- Git

## 🚀 Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/abhi963007/Skillscore.git
cd SkillScore
```

### **2. Python Backend Setup**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### **3. Node.js Backend Setup**
```bash
cd backend
npm install
cd ..
```

### **4. Database Setup**
```bash
# MySQL Setup
mysql -u root -p
CREATE DATABASE skillscore;
```

### **5. Environment Configuration**
- Update MySQL credentials in `backend/db.js`
- Configure Flask secret key in `app.py`

## 🏃‍♂️ Running the Application

### **Start Flask Backend**
```bash
python app.py
```
*Runs on: http://localhost:5000*

### **Start Node.js Evaluation Server**
```bash
cd backend
node server.js
```
*Runs on: http://localhost:3000*

## 📊 Project Structure

```
SkillScore/
├── app.py                 # Flask main application
├── mcq.py                 # MCQ generation module
├── requirements.txt       # Python dependencies
├── backend/               # Node.js evaluation backend
│   ├── server.js          # Express server
│   ├── db.js              # MySQL connection
│   ├── evaluation.js      # Scoring algorithm
│   └── route/             # API routes
├── templates/             # HTML templates (28 files)
├── static/                # CSS, JS, images, fonts
├── skillscore.db          # SQLite database
└── README.md              # This file
```

## 🎯 Skill Scoring Algorithm

The application uses a weighted scoring system:

- **Aptitude Skills**: 30%
- **Technical Skills**: 40%
- **Verbal Skills**: 30%

### **Placement Status**
- **Placement Ready**: ≥75% score
- **Almost Ready**: 50-74% score
- **Needs Training**: <50% score

## 🔐 Authentication & Security

- **Role-Based Access Control**: Admin, Teacher, Student roles
- **Password Hashing**: Secure password storage
- **Session Management**: Secure user sessions
- **Input Validation**: Form data sanitization

## 📝 Key Features Explained

### **MCQ Generation**
Uses NLTK to:
- Extract keywords from uploaded text
- Generate fill-in-the-blank questions
- Provide automated answers with explanations
- Support multiple question formats

### **Evaluation System**
- Automated answer checking
- Category-wise scoring
- Skill gap analysis
- Placement readiness assessment

### **User Management**
- Admin can add/remove users
- Role-based dashboard access
- Profile management
- Password recovery system

## 🎨 UI/UX Features

- **Responsive Design**: Works on all devices
- **Modern Interface**: Clean, professional design
- **Interactive Elements**: Smooth animations and transitions
- **Accessibility**: WCAG compliant design patterns

## 🔄 API Endpoints

### **Flask Routes**
- `/` - Home page
- `/login` - User authentication
- `/register` - User registration
- `/admin/*` - Admin functions
- `/teacher/*` - Teacher functions
- `/student/*` - Student functions

### **Node.js API**
- `POST /exam/submit` - Submit exam answers
- `GET /result/:studentId` - Get student results

## 🐛 Troubleshooting

### **Common Issues**

1. **Database Connection Error**
   - Check MySQL server status
   - Verify credentials in `backend/db.js`

2. **NLTK Download Error**
   - Run: `python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`

3. **Port Conflicts**
   - Ensure ports 5000 and 3000 are available
   - Modify ports in `app.py` and `backend/server.js`

4. **Missing Dependencies**
   - Run `pip install -r requirements.txt`
   - Run `npm install` in backend directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project uses the Learner template by Untree.co, licensed under Creative Commons BY 3.0.

## 👥 Authors

- **Abhi** - *Initial Development* - [abhi963007](https://github.com/abhi963007)

## 📞 Support

For support and queries:
- Create an issue on GitHub
- Email: [your-email@example.com]

## 🌟 Acknowledgments

- **Untree.co** - For the amazing Learner template
- **Bootstrap** - UI framework
- **NLTK** - Natural Language Processing
- **Flask & Node.js** - Backend frameworks

---

**SkillScore** - Empowering students with data-driven placement readiness assessment! 🎓🚀
