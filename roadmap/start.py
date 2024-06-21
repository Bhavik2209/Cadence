from app import generate_course_roadmap
from quiz import generate_course_quiz

def main():
    # Example course input
    course = "Python Programming"

    # Generate roadmap for the specified course
    generated_roadmap = generate_course_roadmap(course)
    generate_quiz = generate_course_quiz(course)

    # Print or use the generated roadmap as needed
    print("Generated Roadmap:")
    print(generated_roadmap)
    print("------------------------------------------------------")
    print("-------------------------------------------------------")
    print("Quiz")
    print(generate_quiz)
if __name__ == "__main__":
    main()