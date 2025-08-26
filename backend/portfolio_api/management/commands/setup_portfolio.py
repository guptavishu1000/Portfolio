"""
Management command to set up initial portfolio data.

Usage:
    python manage.py setup_portfolio

This command creates sample data for the portfolio application
including personal info, skills, projects, experience, and education.
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portfolio_api.models import PersonalInfo, Skill, Project, Experience, Education
from portfolio_api.constants import SKILL_CATEGORIES


class Command(BaseCommand):
    help = 'Set up initial portfolio data with sample content'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if data already exists',
        )

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write(
            self.style.SUCCESS('Setting up portfolio data...')
        ) 
        # Get superuser details from environment variables
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        # Create superuser if none exists
        if not User.objects.filter(username=username).exists():
            self.stdout.write(f'Creating superuser: {username}')
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created.')
            )
        
        # Create personal info
        if not PersonalInfo.objects.exists() or force:
            self.stdout.write('Creating personal information...')
            personal_info = PersonalInfo.objects.create(
                name='John Doe',
                title='Full Stack Developer',
                bio='Passionate developer with expertise in modern web technologies.',
                email='john.doe@example.com',
                phone='+1-555-0123',
                location='San Francisco, CA',
                github='https://github.com/johndoe',
                linkedin='https://linkedin.com/in/johndoe',
                website='https://johndoe.dev'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Personal info created for {personal_info.name}')
            )
        
        # Create skills
        if not Skill.objects.exists() or force:
            self.stdout.write('Creating skills...')
            skills_data = [
                # Programming Languages
                ('Python', 'programming', 9, 'Primary programming language'),
                ('JavaScript', 'programming', 8, 'Frontend and Node.js development'),
                ('Java', 'programming', 7, 'Enterprise development experience'),
                
                # Frameworks
                ('Django', 'framework', 9, 'Python web framework'),
                ('React', 'framework', 8, 'Frontend library'),
                ('Node.js', 'framework', 7, 'JavaScript runtime'),
                
                # Databases
                ('PostgreSQL', 'database', 8, 'Primary database'),
                ('MongoDB', 'database', 7, 'NoSQL database'),
                ('Redis', 'database', 6, 'Caching and sessions'),
                
                # Tools
                ('Git', 'tool', 9, 'Version control'),
                ('Docker', 'tool', 7, 'Containerization'),
                ('AWS', 'tool', 6, 'Cloud services'),
                
                # Soft Skills
                ('Team Leadership', 'soft', 8, 'Leading development teams'),
                ('Problem Solving', 'soft', 9, 'Analytical thinking'),
                ('Communication', 'soft', 8, 'Technical and non-technical'),
            ]
            
            for name, category, proficiency, description in skills_data:
                Skill.objects.create(
                    name=name,
                    category=category,
                    proficiency=proficiency,
                    description=description,
                    order=proficiency
                )
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(skills_data)} skills')
            )
        
        # Create projects
        if not Project.objects.exists() or force:
            self.stdout.write('Creating projects...')
            projects_data = [
                {
                    'title': 'E-commerce Platform',
                    'description': 'Full-stack e-commerce solution with payment integration.',
                    'short_description': 'Modern e-commerce platform built with Django and React',
                    'featured': True,
                    'order': 1,
                    'github_url': 'https://github.com/johndoe/ecommerce',
                    'live_url': 'https://ecommerce-demo.johndoe.dev'
                },
                {
                    'title': 'Task Management App',
                    'description': 'Collaborative task management application with real-time updates.',
                    'short_description': 'Team collaboration tool with real-time features',
                    'featured': True,
                    'order': 2,
                    'github_url': 'https://github.com/johndoe/taskapp',
                    'live_url': 'https://tasks.johndoe.dev'
                },
                {
                    'title': 'Portfolio Website',
                    'description': 'Personal portfolio website showcasing projects and skills.',
                    'short_description': 'Personal portfolio built with Django and React',
                    'featured': False,
                    'order': 3,
                    'github_url': 'https://github.com/johndoe/portfolio',
                    'live_url': 'https://johndoe.dev'
                }
            ]
            
            for project_data in projects_data:
                project = Project.objects.create(**project_data)
                # Add some skills to projects
                skills = Skill.objects.filter(category__in=['programming', 'framework'])[:3]
                project.technologies.set(skills)
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(projects_data)} projects')
            )
        
        # Create experience
        if not Experience.objects.exists() or force:
            self.stdout.write('Creating work experience...')
            experience_data = [
                {
                    'company': 'Tech Corp',
                    'position': 'Senior Developer',
                    'location': 'San Francisco, CA',
                    'start_date': '2022-01-01',
                    'current': True,
                    'description': 'Leading development team and architecting solutions.',
                    'achievements': 'Improved system performance by 40%, led team of 5 developers'
                },
                {
                    'company': 'Startup Inc',
                    'position': 'Full Stack Developer',
                    'location': 'Remote',
                    'start_date': '2020-06-01',
                    'end_date': '2021-12-31',
                    'current': False,
                    'description': 'Developed and maintained web applications.',
                    'achievements': 'Built MVP in 3 months, increased user engagement by 60%'
                }
            ]
            
            for exp_data in experience_data:
                experience = Experience.objects.create(**exp_data)
                # Add some skills to experience
                skills = Skill.objects.filter(category__in=['programming', 'framework'])[:2]
                experience.technologies_used.set(skills)
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(experience_data)} experience entries')
            )
        
        # Create education
        if not Education.objects.exists() or force:
            self.stdout.write('Creating education...')
            education_data = [
                {
                    'institution': 'University of Technology',
                    'degree': 'Bachelor of Science',
                    'field_of_study': 'Computer Science',
                    'start_date': '2016-09-01',
                    'end_date': '2020-05-01',
                    'current': False,
                    'description': 'Focused on software engineering and algorithms.',
                    'gpa': 3.8,
                    'achievements': 'Dean\'s List, Computer Science Honor Society'
                }
            ]
            
            for edu_data in education_data:
                Education.objects.create(**edu_data)
            
            self.stdout.write(
                self.style.SUCCESS(f'Created {len(education_data)} education entries')
            )
        
        self.stdout.write(
            self.style.SUCCESS('Portfolio setup completed successfully!')
        )
        self.stdout.write(
            'You can now access the admin at /admin/ with username: admin, password: admin123'
        )

