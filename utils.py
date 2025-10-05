"""Utility Functions for TalentScout Hiring Assistant

Collection of validation, parsing, and data processing utilities
used throughout the application.
"""

import re
from typing import List


def validate_email(email: str) -> bool:
    """Validate email address format using regex.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if email format is valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone(phone: str) -> bool:
    """Validate phone number by checking digit count.
    
    Args:
        phone: Phone number string to validate
        
    Returns:
        bool: True if phone has at least 10 digits, False otherwise
    """
    # Extract only digits from phone number
    digits_only = re.sub(r'\D', '', phone)
    return len(digits_only) >= 10


def validate_experience(exp: str, max_years: int = 50) -> bool:
    """Validate years of experience input.
    
    Args:
        exp: Experience years as string
        max_years: Maximum allowed years of experience
        
    Returns:
        bool: True if experience is valid number within range
    """
    try:
        years = float(exp)
        return 0 <= years <= max_years
    except ValueError:
        return False


def validate_name(name: str, min_length: int = 2) -> bool:
    """Validate name input for minimum length.
    
    Args:
        name: Name string to validate
        min_length: Minimum required length
        
    Returns:
        bool: True if name meets minimum length requirement
    """
    return len(name.strip()) >= min_length


def parse_tech_questions(tech_response: str, max_questions: int = 5) -> List[str]:
    """Parse technical questions from GPT response text.
    
    Uses multiple parsing strategies to extract individual questions
    from AI-generated response text.
    
    Args:
        tech_response: Raw response text from GPT containing questions
        max_questions: Maximum number of questions to return
        
    Returns:
        List of parsed question strings, limited to max_questions
    """
    lines = tech_response.split('\n')
    questions = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Remove numbering patterns (1., 2), etc.)
        clean_line = re.sub(r'^\d+[.)\-]\s*', '', line)
        
        # Check if line contains question indicators
        if ('?' in clean_line or 
            any(word in clean_line.lower() for word in 
                ['what', 'how', 'why', 'when', 'where', 'explain', 'describe', 'discuss'])):
            questions.append(clean_line)
    
    # Fallback parsing strategy if primary method fails
    if len(questions) < 3:
        questions = [q.strip() for q in re.split(r'\d+[.)\-]', tech_response) if q.strip()]
    
    return questions[:max_questions]


def get_fallback_tech_questions(tech_stack: str) -> List[str]:
    """Generate fallback technical questions when AI generation fails.
    
    Provides a reliable set of technical questions based on the
    candidate's primary technology stack.
    
    Args:
        tech_stack: Candidate's technology stack (comma-separated)
        
    Returns:
        List of 5 fallback technical questions
    """
    primary_tech = tech_stack.split(',')[0].strip() if tech_stack else "your technology stack"
    
    return [
        f"What are the key features and benefits of {primary_tech}?",
        f"Explain a challenging project you worked on using {primary_tech}.",
        "How do you stay updated with the latest technology trends?",
        "Describe your approach to debugging and troubleshooting.",
        "What's your experience with version control systems like Git?"
    ]


def sanitize_input(user_input: str) -> str:
    """Sanitize user input by removing excessive whitespace and harmful characters.
    
    Provides basic input sanitization for security and data quality.
    
    Args:
        user_input: Raw user input string
        
    Returns:
        Sanitized input string with cleaned formatting
    """
    # Remove excessive whitespace and normalize spacing
    sanitized = ' '.join(user_input.split())
    # Remove potentially harmful characters (basic sanitization)
    sanitized = re.sub(r'[<>"\'%;()&+]', '', sanitized)
    return sanitized.strip()