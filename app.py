import streamlit as st
import pandas as pd

# utf-8
def load_questions(file_path,encodings='latin1'):
    questions_data = pd.read_csv(file_path,encoding=encodings)
    return questions_data

def display_question(question_data,question_number):
    unique_identifier = f"question_{question_number}" 
    st.subheader(f"{question_number + 1}: {question_data['Question']}")
    options = question_data['Options'].split(',')
    selected_option = st.radio("Options", options, index=None, key=unique_identifier)
    return selected_option

def main():
    st.title("Quiz Application By Muneeb Wali Khan 🧠")

    # Upload CSV file
    uploaded_file = st.file_uploader("Upload CSV file with questions and answers", type=["csv"])

    
    # Initialize variables
    wrongAns = 0
    correctAns = 0
    result = 0
    
    
    # Instructions accordion
    with st.expander("ℹ️ Instructions About Application"):
        st.write(
            """
            Welcome to the Quiz Application By Muneeb Wali Khan! 🌟
            
            Follow these steps:
            
            1. Upload a CSV file containing questions and answers by clicking on 'Upload CSV file.'
            1. Upload a CSV file Must Contains These Columns: [Question , Options , CorrectAnswer].'
            2. Answer each question and click 'Submit' to see your results.
            
            Enjoy the quiz By Muneeb Wali Khan! 🧠
            """
        )

    if uploaded_file is not None:
        # Load questions from CSV
        questions_data = load_questions(uploaded_file)
        total_questions = len(questions_data)
        user_answers = []

        if 'Question' not in questions_data.columns or 'Options' not in questions_data.columns or 'CorrectAnswer' not in questions_data.columns:
            st.error("Invalid CSV file format. Please ensure that the file contains columns: Question, Options, CorrectAnswer")
            return

        # Display questions
        for index, question_row in questions_data.iterrows():
            st.write(f"\n\nQuestion {index + 1} of {total_questions}")
            selected_option = display_question(question_row,index)
            user_answers.append(selected_option)

        # Submit button at the end
        if st.button("Submit"):
            st.write("\n\n**Results:**")
            # Display correct or wrong responses
            for index, question_row in questions_data.iterrows():
                st.write(f"\nQuestion {index + 1}: {question_row['Question']}")
                correct_answer = question_row['CorrectAnswer']
                user_answer = user_answers[index]
                if user_answer is not None:
                    # Strip leading/trailing whitespaces
                    user_answer = str(user_answer).strip()
                    correct_answer = str(correct_answer).strip()
                    
                    if user_answer == correct_answer:
                        st.success(f"Your answer is correct! 🎉 [{ user_answer }]")
                        correctAns += 1
                    else:
                        st.error(f"Your answer is wrong ( {user_answer} ). Correct answer is [ {correct_answer} ].")
                        wrongAns += 1

            # Calculate result
            result = (correctAns / total_questions) * 100
            st.write(f"\n\n**Final Result:**")
            st.write(f"Total Questions: {total_questions}")
            st.write(f"Correct Answers: {correctAns}")
            st.write(f"Wrong Answers: {wrongAns}")
            st.write(f"Your Result: {round(result)}%")

if __name__ == "__main__":
    main()

