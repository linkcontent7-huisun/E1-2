"""게임 전체를 관리하는 QuizGame 클래스."""
from data import default_quizzes
from io_utils import ExitRequested, read_int

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

    def run(self):
        try:
            while True:
                self.show_menu()
                choice = read_int("선택: ", 1, 5)
                if choice == 5:
                    break
                print("(준비 중인 기능입니다)")
        except ExitRequested:
            print("⚠️ 입력이 중단되어 안전하게 종료합니다.")
        print("👋 게임을 종료합니다.")
