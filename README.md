# 🚀 Portfolio Website - Django + React

A modern, responsive portfolio website built with Django backend and React.js frontend, featuring dark mode, real-time data integration, and a beautiful UI.

## ✨ Features

### 🌟 Core Features
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Dark Mode**: Default dark theme with toggle functionality
- **Real-time Data**: Dynamic content from Django backend
- **Modern UI**: Beautiful animations with Framer Motion
- **Cross-platform**: Works seamlessly on all devices

### 🎨 Frontend Features
- **Profile Picture Display**: Shows user's profile picture on home page
- **Resume Management**: View and download resume functionality
- **Social Media Integration**: Dynamic social links from backend
- **Interactive Components**: Hover effects, smooth transitions
- **Error Handling**: User-friendly error messages and retry options
- **Loading States**: Smooth loading animations

### 🔧 Backend Features
- **RESTful API**: Django REST Framework with comprehensive endpoints
- **Admin Interface**: Customized Django admin with visual enhancements
- **File Management**: Profile pictures, resume uploads, project images
- **Data Validation**: Robust model validation and error handling
- **Caching System**: Intelligent caching for better performance
- **Management Commands**: Easy setup with `setup_portfolio` command

### 🛡️ Security & Performance
- **CORS Configuration**: Secure cross-origin requests
- **File Upload Security**: Type and size validation
- **Rate Limiting**: API protection against abuse
- **Logging**: Comprehensive logging for debugging
- **Database Optimization**: Efficient queries and indexing

## 🏗️ Project Structure

```
portfolio/
├── backend/                 # Django backend
│   ├── backend/            # Django project settings
│   │   ├── settings.py     # Main Django configuration
│   │   ├── urls.py         # Main URL routing
│   │   └── wsgi.py         # WSGI configuration
│   ├── portfolio_api/      # Main Django app
│   │   ├── models.py       # Database models
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API views and viewsets
│   │   ├── admin.py        # Admin interface customization
│   │   ├── constants.py    # Application constants
│   │   ├── utils.py        # Utility functions
│   │   ├── signals.py      # Django signals
│   │   └── management/     # Custom management commands
│   ├── static/             # Static files
│   ├── logs/               # Application logs
│   ├── manage.py           # Django management script
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   │   ├── Home.js     # Home page with profile & resume
│   │   │   ├── About.js    # About page with skills
│   │   │   ├── Projects.js # Projects showcase
│   │   │   ├── Experience.js # Work & education history
│   │   │   ├── Contact.js  # Contact form & info
│   │   │   ├── Navbar.js   # Navigation with theme toggle
│   │   │   ├── Footer.js   # Footer with real data
│   │   │   └── ThemeToggle.js # Dark/light mode toggle
│   │   ├── contexts/       # React contexts
│   │   │   └── ThemeContext.js # Theme management
│   │   ├── App.js          # Main app component
│   │   ├── index.js        # App entry point
│   │   ├── api.js          # API configuration
│   │   └── index.css       # Tailwind CSS imports
│   ├── tailwind.config.js  # Tailwind configuration
│   ├── postcss.config.js   # PostCSS configuration
│   └── package.json        # Node.js dependencies
└── README.md               # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend/backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser and populate data:**
   ```bash
   python manage.py setup_portfolio
   ```

6. **Start Django server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/

## 📱 Pages & Features

### 🏠 Home Page
- **Profile Picture**: Displays user's profile picture
- **Resume Actions**: View and download resume buttons
- **Social Links**: Dynamic GitHub, LinkedIn, Twitter links
- **Call-to-Action**: View work, contact, and feature highlights

### 👤 About Page
- **Personal Information**: Name, bio, title, location
- **Skills Display**: Categorized skills with proficiency bars
- **Professional Summary**: Comprehensive background information

### 💼 Projects Page
- **Project Showcase**: Featured and all projects
- **Technology Tags**: Skills used in each project
- **Filtering**: By technology and featured status
- **Responsive Grid**: Adapts to all screen sizes

### 🎓 Experience Page
- **Work History**: Professional experience timeline
- **Education**: Academic background
- **Technology Stack**: Skills used in each role
- **Chronological Order**: Most recent first

### 📞 Contact Page
- **Contact Form**: Name, email, subject, message
- **Real Information**: Email, phone, location from backend
- **Social Links**: GitHub, LinkedIn, Twitter integration
- **Response Time**: Clear communication expectations

### 🌙 Dark Mode
- **Default Theme**: Dark mode enabled by default
- **Theme Toggle**: Sun/moon icon in navigation
- **Persistence**: Remembers user preference
- **Smooth Transitions**: Animated theme switching

## 🔧 API Endpoints

### Core Endpoints
- `GET /api/personal-info/current/` - Current personal information
- `GET /api/skills/` - All skills with categories
- `GET /api/projects/` - All projects (with filtering)
- `GET /api/experience/` - Work experience
- `GET /api/education/` - Educational background
- `POST /api/contact/` - Submit contact form

### API Features
- **Filtering**: Query parameters for projects and skills
- **Pagination**: Configurable page sizes
- **Rate Limiting**: Protection against abuse
- **Error Handling**: Comprehensive error responses
- **Caching**: Intelligent response caching

## ✏️ Editing Portfolio Data

### Accessing Admin Interface
1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. Navigate to "Portfolio API" section

### Managing Content

#### Personal Information
- **Profile Picture**: Upload new image (recommended: 400x400px)
- **Resume**: Upload PDF or document file
- **Social Links**: Add GitHub, LinkedIn, Twitter URLs
- **Contact Details**: Update email, phone, location

#### Skills
- **Categories**: Frontend, Backend, Database, DevOps, Tools
- **Proficiency**: 1-10 scale with visual bars
- **Order**: Control display sequence
- **Icons**: Visual representation in admin

#### Projects
- **Images**: Upload project screenshots
- **Technologies**: Link to existing skills
- **Links**: Live demo and source code URLs
- **Featured**: Mark important projects

#### Experience & Education   
- **Dates**: Start/end dates with validation
- **Current Position**: Mark ongoing roles
- **Technologies**: Skills used in each role
- **Descriptions**: Rich text descriptions

### File Upload Guidelines
- **Images**: JPG, PNG, WebP (max 5MB)
- **Documents**: PDF, DOC, DOCX (max 10MB)
- **Profile Pictures**: Square aspect ratio recommended
- **Project Images**: 16:9 or 4:3 aspect ratios

### Best Practices
- **Regular Updates**: Keep content current
- **Image Optimization**: Compress images before upload
- **Content Validation**: Review all text content
- **Backup**: Export data periodically

### Bulk Operations
- **Import/Export**: Use Django admin actions
- **Batch Updates**: Modify multiple items at once
- **Data Migration**: Use management commands

## 🛠️ Development

### Code Quality Tools
```bash
# Backend
black backend/backend/portfolio_api/
flake8 backend/backend/portfolio_api/
isort backend/backend/portfolio_api/

# Frontend
npm run lint
npm run format
```

### Testing
```bash
# Backend
cd backend/backend
python manage.py test

# Frontend
cd frontend
npm test
```

### Environment Variables
Create `.env` files for configuration:

**Backend (.env)**
```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

**Frontend (.env)**
```env
REACT_APP_API_BASE_URL=http://localhost:8000/api
REACT_APP_MEDIA_BASE_URL=http://localhost:8000/media
```

## 🚀 Deployment

### Backend Deployment
1. Set `DEBUG=False` in production
2. Configure production database
3. Set up static file serving
4. Configure environment variables
5. Use production WSGI server (Gunicorn)

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Serve static files from web server
3. Configure API base URLs
4. Set up CDN for media files

## 🐛 Troubleshooting

### Common Issues

#### Backend Issues
- **Database Errors**: Run `python manage.py migrate`
- **Static Files**: Check `STATIC_ROOT` and `STATICFILES_DIRS`
- **Media Files**: Verify `MEDIA_URL` and `MEDIA_ROOT`
- **CORS Errors**: Check `CORS_ALLOWED_ORIGINS`

#### Frontend Issues
- **API Connection**: Verify backend server is running
- **Build Errors**: Clear `node_modules` and reinstall
- **Styling Issues**: Check Tailwind CSS configuration
- **Theme Issues**: Clear localStorage and refresh

#### Data Issues
- **Empty Pages**: Run `python manage.py setup_portfolio`
- **Missing Images**: Check file upload permissions
- **API Errors**: Review Django logs in `logs/` directory

### Logs Location
- **Django Logs**: `backend/backend/logs/`
- **Console Logs**: Check terminal output
- **Browser Logs**: Developer tools console

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes with proper formatting
4. Test thoroughly
5. Submit pull request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint for JavaScript
- Write meaningful commit messages
- Test on multiple devices
- Document new features

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django and Django REST Framework
- React.js and Framer Motion
- Tailwind CSS for styling
- Create React App for frontend setup

---

**Happy Coding! 🎉**

For support or questions, please open an issue in the repository.