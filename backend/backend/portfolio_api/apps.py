from django.apps import AppConfig


class PortfolioApiConfig(AppConfig):
    """
    Configuration for the Portfolio API application.
    
    This app provides a comprehensive API for managing portfolio information
    including personal details, skills, projects, experience, education,
    and contact form submissions.
    """
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio_api'
    verbose_name = 'Portfolio API'
    
    def ready(self):
        """
        Import signals when the app is ready.
        This method is called when Django starts.
        """
        try:
            import portfolio_api.signals  # noqa
        except ImportError:
            pass
