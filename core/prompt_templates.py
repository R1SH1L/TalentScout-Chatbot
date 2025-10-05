"""AI Prompt Templates for TalentScout Hiring Assistant

Contains carefully crafted prompt templates for AI-powered question
generation with consistent formatting and quality standards.
"""


class PromptTemplates:
    """Collection of prompt templates for different interview scenarios."""
    
    @staticmethod
    def generate_tech_questions_prompt(tech_stack: str) -> str:
        """Generate prompt for AI-powered technical question creation.
        
        Creates a structured prompt that instructs the AI to generate
        relevant, practical technical questions based on the candidate's
        technology stack.
        
        Args:
            tech_stack: Candidate's technology stack and skills
            
        Returns:
            Formatted prompt string for GPT API call
        """
        return f"""Generate exactly 5 technical interview questions for a candidate with the following tech stack: {tech_stack}

Requirements:
- Each question should be on a separate line
- Number each question (1., 2., 3., etc.)
- Focus on practical experience and problem-solving
- Mix of conceptual understanding and real-world application
- Difficulty level: intermediate
- Avoid questions requiring code implementation
- Make questions specific to the mentioned technologies
- Questions should be suitable for a 15-20 minute interview

Format example:
1. Question about technology A
2. Question about technology B
3. Question about problem-solving
4. Question about best practices
5. Question about experience/challenges

Generate the questions now:"""


def generate_tech_questions_prompt(tech_stack: str) -> str:
    """Legacy function for backward compatibility.
    
    Args:
        tech_stack: Candidate's technology stack
        
    Returns:
        Formatted prompt string for GPT API call
    """
    return PromptTemplates.generate_tech_questions_prompt(tech_stack)
