"""게임 전체를 관리하는 QuizGame 클래스."""
from data import default_quizzes
from io_utils import ExitRequested, read_int, read_nonempty
from quiz import CHOICE_COUNT, Quiz

LINE = "=" * 40


class QuizGame:
    def __init__(self):
        self.quizzes = default_quizzes()
        self.best_score = None  # 아직 풀지 않았으면 None

    def show_menu(self):
        print(LINE)
        print("🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print(LINE)

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return None
        total = len(self.quizzes)
        correct = 0
        print()
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
        for number, quiz in enumerate(self.quizzes, start=1):
            print("-" * 40)
            print(f"[문제 {number}]")
            quiz.display()
            print()
            choice = read_int("정답 입력: ", 1, len(quiz.choices))
            if quiz.is_correct(choice):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        score = round(correct / total * 100)
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE)
        return score

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 등록한다."""
        print()
        print("📌 새로운 퀴즈를 추가합니다.")
        print()
        question = read_nonempty("문제를 입력하세요: ")
        choices = [read_nonempty(f"선택지 {number}: ") for number in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        self.quizzes.append(Quiz(question, choices, answer))
        print("✅ 퀴즈가 추가되었습니다!")

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
                if choice == 5:
                    break
                if choice == 1:
                    self.play_quiz()
                elif choice == 2:
                    self.add_quiz()
                else:
                    print("(준비 중인 기능입니다)")
        except ExitRequested:
            print("⚠️ 입력이 중단되어 안전하게 종료합니다.")
        print("👋 게임을 종료합니다.")
