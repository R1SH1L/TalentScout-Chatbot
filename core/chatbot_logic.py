import streamlit as st
import pandas as pd
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from datetime import datetime

from config import Config
from utils import (
    validate_email, validate_phone, validate_experience, validate_name,
    parse_tech_questions, get_fallback_tech_questions, sanitize_input
)
from core.prompt_templates import PromptTemplates
from core.data_handler import DataHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class InterviewPhases:
    BASIC_INFO = "basic_info"
    TECHNICAL = "technical"
    COMPLETED = "completed"


class TalentScoutChatbot:
    """
    Main chatbot class handling the interview process.
    """
    
    def __init__(self):
        """Initialize the chatbot with configuration and clients."""
        self.config = Config()
        self.data_handler = DataHandler(
            data_dir=self.config.DATA_DIR,
            csv_filename=self.config.CSV_FILENAME
        )
        
        # Initialize OpenAI client
        try:
            self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            st.error("Failed to initialize AI service. Please check your API key.")
            st.stop()
        
        self.basic_questions = [
            "What is your full name?",
            "What is your email address?",
            "What is your phone number?",
            "How many years of experience do you have?",
            "Which position are you applying for?",
            "Where are you currently located?",
            "Please list your tech stack (languages, frameworks, and tools you know)."
        ]
    
    def initialize_session_state(self) -> None:
        """Initialize all session state variables."""
        session_defaults = {
            "step": 0,
            "candidate": {},
            "messages": [],
            "completed": False,
            "tech_questions": [],
            "tech_step": 0,
            "tech_answers": {},
            "interview_phase": InterviewPhases.BASIC_INFO
        }
        
        for key, default_value in session_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value
    
    def show_initial_greeting(self) -> None:
        """Display the initial greeting message."""
        if st.session_state.step == 0 and not st.session_state.messages:
            greeting = (
                f"👋 Hi! I'm **{self.config.APP_TITLE.split()[0]}**, your AI Hiring Assistant.\n\n"
                "I'll collect some quick details and then ask a few technical questions "
                "based on your skills. Type **'exit'** anytime to end the chat.\n\n"
                f"📊 *We've helped {self.data_handler.get_candidate_count()} candidates so far!*"
            )
            st.chat_message("assistant").write(greeting)
            st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    def display_chat_history(self) -> None:
        """Display the chat message history."""
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
    
    def validate_user_input(self, user_input: str, question_index: int) -> Optional[str]:
        """
        Validate user input based on the current question.
        
        Args:
            user_input (str): User's input
            question_index (int): Index of current question
            
        Returns:
            Optional[str]: Error message if validation fails, None if valid
        """
        current_question = self.basic_questions[question_index].lower()
        
        if "email" in current_question:
            if not validate_email(user_input):
                return "⚠️ Please enter a valid email address (e.g., john@example.com)"
        
        elif "phone" in current_question:
            if not validate_phone(user_input):
                return "⚠️ Please enter a valid phone number (at least 10 digits)"
        
        elif "experience" in current_question:
            if not validate_experience(user_input, self.config.MAX_EXPERIENCE_YEARS):
                return f"⚠️ Please enter a valid number of years (0-{self.config.MAX_EXPERIENCE_YEARS})"
        
        elif "name" in current_question:
            if not validate_name(user_input):
                return "⚠️ Please enter your full name (at least 2 characters)"
        
        elif "tech stack" in current_question:
            if len(user_input.strip()) < 3:
                return "⚠️ Please provide more details about your technology stack"
        
        return None
    
    def generate_technical_questions(self, tech_stack: str) -> List[str]:
        """
        Generate technical questions using AI.
        
        Args:
            tech_stack (str): Candidate's technology stack
            
        Returns:
            List[str]: List of technical questions
        """
        try:
            prompt = PromptTemplates.generate_tech_questions_prompt(tech_stack)
            
            response = self.client.chat.completions.create(
                model=self.config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a professional technical interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            tech_response = response.choices[0].message.content
            questions = parse_tech_questions(tech_response, self.config.MAX_TECH_QUESTIONS)
            
            if len(questions) < 3:
                logger.warning("AI question generation failed, using fallback questions")
                questions = get_fallback_tech_questions(tech_stack)
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating technical questions: {e}")
            return get_fallback_tech_questions(tech_stack)
    
    def create_interview_csv(self) -> str:
        """Create CSV data from current interview session."""
        try:
            structured_data = {
                "interview_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **st.session_state.candidate
            }
            
            if st.session_state.tech_questions and st.session_state.tech_answers:
                for i, question in enumerate(st.session_state.tech_questions, 1):
                    answer_key = f"Tech Question {i}"
                    answer = st.session_state.tech_answers.get(answer_key, "No answer provided")
                    structured_data[f"Technical_Q{i}"] = question.replace('"', '').replace(',', ';')
                    structured_data[f"Technical_A{i}"] = answer.replace('"', '').replace(',', ';')
            
            for i in range(1, 6):
                if f"Technical_Q{i}" not in structured_data:
                    structured_data[f"Technical_Q{i}"] = ""
                if f"Technical_A{i}" not in structured_data:
                    structured_data[f"Technical_A{i}"] = ""
            
            df = pd.DataFrame([structured_data])
            return df.to_csv(index=False)
            
        except Exception as e:
            logger.error(f"Error creating CSV: {e}")
            return ""
    
    def handle_basic_info_phase(self) -> None:
        """Handle the basic information collection phase."""
        if st.session_state.step < len(self.basic_questions):
            # Show progress
            progress = (st.session_state.step + 1) / len(self.basic_questions)
            st.progress(progress, f"Basic Information: {st.session_state.step + 1}/{len(self.basic_questions)}")
            
            current_question = self.basic_questions[st.session_state.step]
            st.chat_message("assistant").write(
                f"**Question {st.session_state.step + 1} of {len(self.basic_questions)}:**\n{current_question}"
            )

        user_input = st.chat_input("Type your answer here...")
        
        if user_input:
            # Handle exit commands
            if user_input.lower() in ["exit", "quit", "bye", "end"]:
                st.chat_message("assistant").write(
                    "👋 Thanks for chatting with TalentScout! We'll review your details and get back to you soon."
                )
                st.stop()

            # Sanitize and validate input
            user_input = sanitize_input(user_input)
            
            if len(user_input.strip()) == 0:
                st.chat_message("assistant").write("⚠️ Sorry, I didn't catch that. Could you please rephrase?")
                st.stop()

            # Validate based on question type
            validation_error = self.validate_user_input(user_input, st.session_state.step)
            if validation_error:
                st.chat_message("assistant").write(validation_error)
                st.stop()

            # Save valid response
            st.chat_message("user").write(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            if st.session_state.step < len(self.basic_questions):
                question_key = self.basic_questions[st.session_state.step]
                st.session_state.candidate[question_key] = user_input
                st.session_state.step += 1

            # Transition to technical phase after last question
            if st.session_state.step == len(self.basic_questions):
                tech_stack = st.session_state.candidate[self.basic_questions[-1]]
                
                with st.spinner("🤖 Generating personalized technical questions..."):
                    tech_questions = self.generate_technical_questions(tech_stack)
                
                st.session_state.tech_questions = tech_questions
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "✅ Thanks for the basic details! Now let's move to the technical interview section."
                })
                
                st.session_state.interview_phase = InterviewPhases.TECHNICAL
                st.session_state.tech_step = 0
                st.rerun()
            
            elif st.session_state.step < len(self.basic_questions):
                st.rerun()
    
    def handle_technical_phase(self) -> None:
        """Handle the technical interview phase."""
        if st.session_state.tech_step < len(st.session_state.tech_questions):
            # Show progress
            progress = (st.session_state.tech_step + 1) / len(st.session_state.tech_questions)
            st.progress(progress, f"Technical Interview: {st.session_state.tech_step + 1}/{len(st.session_state.tech_questions)}")
            
            current_question = st.session_state.tech_questions[st.session_state.tech_step]
            st.chat_message("assistant").write(
                f"**Technical Question {st.session_state.tech_step + 1} of {len(st.session_state.tech_questions)}:**\n{current_question}"
            )

        user_input = st.chat_input("Type your technical answer here...")

        if user_input:
            # Handle exit commands
            if user_input.lower() in ["exit", "quit", "bye", "end"]:
                st.chat_message("assistant").write(
                    "👋 Thanks for participating in the technical interview! We'll review your responses and get back to you soon."
                )
                st.stop()

            # Sanitize input
            user_input = sanitize_input(user_input)
            
            # Validate answer length
            if len(user_input.strip()) < self.config.MIN_ANSWER_LENGTH:
                st.chat_message("assistant").write(
                    f"⚠️ Please provide a more detailed answer (at least {self.config.MIN_ANSWER_LENGTH} characters). Technical questions require thoughtful responses."
                )
                st.stop()

            # Save response
            st.chat_message("user").write(user_input)
            st.session_state.messages.append({"role": "user", "content": user_input})

            if st.session_state.tech_step < len(st.session_state.tech_questions):
                question_key = f"Tech Question {st.session_state.tech_step + 1}"
                st.session_state.tech_answers[question_key] = user_input
                st.session_state.tech_step += 1

            # Check if technical interview is complete
            if st.session_state.tech_step >= len(st.session_state.tech_questions):
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "🎉 Excellent! You've completed both the basic information and technical interview sections."
                })
                st.session_state.interview_phase = InterviewPhases.COMPLETED
                st.session_state.completed = True
                st.rerun()
            else:
                st.rerun()
    
    def display_completion_summary(self) -> None:
        """Display the completion summary and save options."""
        st.subheader("📝 Interview Summary")
        
        # Basic Information
        with st.expander("**📋 Basic Information**", expanded=True):
            basic_df = pd.DataFrame.from_dict(
                st.session_state.candidate, 
                orient='index', 
                columns=['Response']
            )
            st.table(basic_df)
        
        # Technical Questions and Answers
        if st.session_state.tech_answers and st.session_state.tech_questions:
            with st.expander("**🔧 Technical Interview Q&A**", expanded=True):
                # Create a structured display of questions and answers
                qa_data = []
                for i, question in enumerate(st.session_state.tech_questions, 1):
                    answer_key = f"Tech Question {i}"
                    answer = st.session_state.tech_answers.get(answer_key, "No answer provided")
                    qa_data.append({
                        "Question": question,
                        "Answer": answer
                    })
                
                # Display Q&A pairs
                for i, qa in enumerate(qa_data, 1):
                    st.write(f"**Q{i}:** {qa['Question']}")
                    st.write(f"**A{i}:** {qa['Answer']}")
                    st.write("---")

        # Save options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save Interview Data", type="primary"):
                success = self.data_handler.save_candidate_data(
                    candidate_dict=st.session_state.candidate,
                    tech_questions=st.session_state.tech_questions,
                    tech_answers=st.session_state.tech_answers
                )
                
                if success:
                    st.success("✅ Interview data saved successfully!")
                else:
                    st.error("❌ Failed to save data. Please try again.")
        
        with col2:
            if st.button("� Download CSV"):
                csv_data = self.create_interview_csv()
                if csv_data:
                    st.download_button(
                        label="📄 Download Interview Data",
                        data=csv_data,
                        file_name=f"interview_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                    st.success("✅ CSV ready for download!")
        
        with col3:
            if st.button("🔄 Start New Interview"):
                for key in st.session_state.keys():
                    del st.session_state[key]
                st.rerun()

        st.info("💡 **For Deployed Apps:** Use the download button to get your interview data as CSV file since cloud storage is temporary.")
    
    def run(self) -> None:
        """Main chatbot execution method."""
        # Initialize session state
        self.initialize_session_state()
        
        # Show initial greeting
        self.show_initial_greeting()
        
        # Display chat history
        self.display_chat_history()
        
        # Handle different interview phases
        if not st.session_state.completed:
            if st.session_state.interview_phase == InterviewPhases.BASIC_INFO:
                self.handle_basic_info_phase()
            elif st.session_state.interview_phase == InterviewPhases.TECHNICAL:
                self.handle_technical_phase()
        else:
            self.display_completion_summary()


def run_chatbot() -> None:
    """
    Entry point for the chatbot - maintains backward compatibility.
    """
    try:
        chatbot = TalentScoutChatbot()
        chatbot.run()
    except Exception as e:
        logger.error(f"Chatbot execution error: {e}")
        st.error("An unexpected error occurred. Please refresh the page and try again.")
        if st.button("🔄 Refresh Page"):
            st.rerun()