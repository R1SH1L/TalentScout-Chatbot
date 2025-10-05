import os
import pandas as pd
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataHandler:
    
    def __init__(self, data_dir: str = "data", csv_filename: str = "candidate_data.csv"):
        self.data_dir = data_dir
        self.csv_filename = csv_filename
        self.file_path = os.path.join(data_dir, csv_filename)
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def save_candidate_data(self, candidate_dict: Dict[str, Any], tech_questions: List[str] = None, tech_answers: Dict[str, str] = None) -> bool:
        try:
            structured_data = {
                "interview_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **candidate_dict
            }
            
            if tech_questions and tech_answers:
                for i, question in enumerate(tech_questions, 1):
                    answer_key = f"Tech Question {i}"
                    answer = tech_answers.get(answer_key, "No answer provided")
                    
                    structured_data[f"Technical_Q{i}"] = question.replace('"', '').replace(',', ';')
                    structured_data[f"Technical_A{i}"] = answer.replace('"', '').replace(',', ';')
            
            for i in range(1, 6):
                if f"Technical_Q{i}" not in structured_data:
                    structured_data[f"Technical_Q{i}"] = ""
                if f"Technical_A{i}" not in structured_data:
                    structured_data[f"Technical_A{i}"] = ""
            
            column_order = [
                "interview_date",
                "What is your full name?",
                "What is your email address?",
                "What is your phone number?",
                "How many years of experience do you have?",
                "Which position are you applying for?",
                "Where are you currently located?",
                "Please list your tech stack (languages, frameworks, and tools you know).",
                "Technical_Q1", "Technical_A1",
                "Technical_Q2", "Technical_A2",
                "Technical_Q3", "Technical_A3",
                "Technical_Q4", "Technical_A4",
                "Technical_Q5", "Technical_A5"
            ]
            
            for col in column_order:
                if col not in structured_data:
                    structured_data[col] = ""
            
            df = pd.DataFrame([structured_data], columns=column_order)
            if os.path.exists(self.file_path):
                df.to_csv(self.file_path, mode='a', index=False, header=False, encoding='utf-8')
            else:
                df.to_csv(self.file_path, index=False, encoding='utf-8')
            
            logger.info(f"Successfully saved candidate data to {self.file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving candidate data: {e}")
            return False
    
    def load_candidate_data(self) -> Optional[pd.DataFrame]:
        try:
            if os.path.exists(self.file_path):
                df = pd.read_csv(self.file_path, encoding='utf-8')
                logger.info(f"Loaded {len(df)} candidate records from {self.file_path}")
                return df
            else:
                logger.info(f"No data file found at {self.file_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error loading candidate data: {e}")
            return None
    
    def get_candidate_count(self) -> int:
        try:
            df = self.load_candidate_data()
            return len(df) if df is not None else 0
        except Exception:
            return 0


# Backward compatibility function
def save_candidate_data(candidate_dict: Dict[str, Any], tech_questions: List[str] = None, tech_answers: Dict[str, str] = None) -> bool:
    handler = DataHandler()
    return handler.save_candidate_data(candidate_dict, tech_questions, tech_answers)
