from agent.agent import SimpleAgent
from utils import detect_language

def main():
    agent = SimpleAgent()

    print("🎓  Chatbot Agent for Informatics Engineering")
    print("أدخل سؤالك (اكتب exit للخروج):")

    while True:
        q = input("\n> ")
        lang = detect_language(q)
        if q.lower() == "exit":
            break

        answer, eval_text = agent.ask(q, lang)

        if lang == "ar":
            print("\n📌 الإجابة:")
        else: print("\n📌 Answer:")
        print(answer)

        if lang == "ar":
            print("\n📝 التقييم:")
        else: print("\n📝 Evaluation:")
        print(eval_text)


if __name__ == "__main__":
    main()
