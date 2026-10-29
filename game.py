"""게임 전체를 관리하는 QuizGame 클래스."""
import json
import random
from pathlib import Path

from data import default_quizzes
from io_utils import ExitRequested, read_int, read_nonempty, read_text
from quiz import CHOICE_COUNT, Quiz

LINE = "=" * 40
MENU_TITLES = ["퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "퀴즈 삭제", "종료"]
EXIT_CHOICE = len(MENU_TITLES)  # 마지막 항목이 항상 종료
HINT_CREDIT = 0.5  # 힌트를 쓰고 맞히면 인정되는 점수 비율
STATE_PATH =Path(__file__).resolve().parent / "state.json"  # 프로젝트 루트


class QuizGame:
    def __init__(self, state_path=STATE_PATH):
        self.state_path = Path(state_path)
        self.quizzes = default_quizzes()
        self.best_score = None  # 아직 풀지 않았으면 None
        self.best_correct = 0
        self.best_total = 0
        self.load_state()

    def reset_to_default(self):
        self.quizzes = default_quizzes()
        self.best_score = None
        self.best_correct = 0
        self.best_total = 0

    def load_state(self):
        """state.json을 읽는다. 없으면 기본 데이터, 손상되었으면 안내 후 기본 데이터로 복구한다."""
        if not self.state_path.exists():
            print("🆕 저장된 데이터가 없어 기본 퀴즈로 시작합니다.")
            return
        try:
            with open(self.state_path, encoding="utf-8") as file:
                data = json.load(file)
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            best_score = data["best_score"]
            if best_score is not None and not isinstance(best_score, int):
                raise ValueError("best_score는 정수 또는 null이어야 합니다.")
            self.quizzes = quizzes
            self.best_score = best_score
            self.best_correct = data.get("best_correct", 0)
            self.best_total = data.get("best_total", 0)
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
            print(f"⚠️ 데이터 파일을 읽을 수 없습니다 ({type(error).__name__}). 기본 퀴즈로 복구합니다.")
            self.backup_broken_file()
            self.reset_to_default()
            self.save_state()
            return
        score_text = "없음" if self.best_score is None else f"{self.best_score}점"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {score_text})")

    def backup_broken_file(self):
        """손상된 파일을 .bak으로 옮겨 둔다. 실패해도 게임은 계속한다."""
        try:
            self.state_path.replace(self.state_path.with_suffix(".json.bak"))
        except OSError:
            pass

    def save_state(self):
        """퀴즈와 최고 점수를 UTF-8 JSON으로 저장한다."""
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total,
        }
        try:
            with open(self.state_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            print(f"⚠️ 저장하지 못했습니다: {error}")

    def show_menu(self):
        print(LINE)
        print("🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, title in enumerate(MENU_TITLES, start=1):
            print(f"{number}. {title}")
        print(LINE)

    def play_quiz(self):
        """저장된 퀴즈를 순서대로 출제하고 결과를 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다. 먼저 퀴즈를 추가하세요.")
            return None
        count = read_int(f"몇 문제를 풀까요? (1-{len(self.quizzes)}): ", 1, len(self.quizzes))
        selected = random.sample(self.quizzes, count)  # 순서를 섞어 count개를 뽑는다
        total = len(selected)
        correct = 0
        points = 0.0  # 힌트 없이 맞히면 1점, 힌트를 쓰고 맞히면 HINT_CREDIT점
        hints_used = 0
        print()
        print(f"📝 퀴즈를 시작합니다! (총 {total}문제)")
        for number, quiz in enumerate(selected, start=1):
            print("-" * 40)
            print(f"[문제 {number}]")
            quiz.display()
            print()
            is_correct, used_hint = self.ask_question(quiz)
            hints_used += used_hint
            if is_correct:
                correct += 1
                points += HINT_CREDIT if used_hint else 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
        score = round(points / total * 100)
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if hints_used:
            print(f"💡 힌트 {hints_used}회 사용: 힌트를 쓴 정답은 {HINT_CREDIT}점만 인정됩니다.")
        if self.update_best(score, correct, total):
            self.save_state()
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)
        return score

    def ask_question(self, quiz):
        """한 문제의 답을 받는다. 0을 입력하면 힌트를 볼 수 있다(문제당 1회).

        (정답 여부, 힌트 사용 여부)를 돌려준다.
        """
        used_hint = False
        while True:
            choice = read_int("정답 입력 (힌트 보기: 0): ", 0, len(quiz.choices))
            if choice != 0:
                return quiz.is_correct(choice), used_hint
            if used_hint:
                print("⚠️ 이 문제의 힌트는 이미 확인했습니다.")
            elif quiz.show_hint():
                used_hint = True
            else:
                print("⚠️ 이 문제에는 힌트가 없습니다.")

    def update_best(self, score, correct, total):
        """최고 점수보다 높으면 갱신하고 True를 돌려준다."""
        if self.best_score is not None and score <= self.best_score:
            return False
        self.best_score = score
        self.best_correct = correct
        self.best_total = total
        return True

    def show_score(self):
        """최고 점수를 보여준다. 아직 풀지 않았으면 안내한다."""
        if self.best_score is None:
            print("⚠️ 아직 퀴즈를 풀지 않았습니다. 퀴즈를 풀면 점수가 기록됩니다.")
            return
        print(f"🏆 최고 점수: {self.best_score}점 ({self.best_total}문제 중 {self.best_correct}문제 정답)")

    def add_quiz(self):
        """문제, 선택지 4개, 정답 번호를 입력받아 퀴즈를 등록한다."""
        print()
        print("📌 새로운 퀴즈를 추가합니다.")
        print()
        question = read_nonempty("문제를 입력하세요: ")
        choices = [read_nonempty(f"선택지 {number}: ") for number in range(1, CHOICE_COUNT + 1)]
        answer = read_int(f"정답 번호 (1-{CHOICE_COUNT}): ", 1, CHOICE_COUNT)
        hint = read_text("힌트 (없으면 Enter): ")
        self.quizzes.append(Quiz(question, choices, answer, hint))
        self.save_state()
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈의 문제만 번호와 함께 보여준다."""
        if not self.quizzes:
            print("⚠️ 등록된 퀴즈가 없습니다.")
            return
        print()
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 40)
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"[{number}] {quiz.question}")
        print("-" * 40)

    def delete_quiz(self):
        """목록에서 번호를 골라 퀴즈를 삭제하고 파일에 반영한다."""
        if not self.quizzes:
            print("⚠️ 삭제할 퀴즈가 없습니다.")
            return
        self.list_quizzes()
        number = read_int("삭제할 퀴즈 번호 (취소: 0): ", 0, len(self.quizzes))
        if number == 0:
            print("삭제를 취소했습니다.")
            return
        target = self.quizzes[number - 1]
        print(f"삭제 대상: {target.question}")
        if read_int("정말 삭제할까요? (1. 예 / 2. 아니오): ", 1, 2) != 1:
            print("삭제를 취소했습니다.")
            return
        del self.quizzes[number - 1]
        self.save_state()
        print("🗑️ 퀴즈를 삭제했습니다.")

    def run(self):
        """메뉴 번호와 기능을 한 곳에 묶어 두고 종료(5)를 고를 때까지 반복한다."""
        actions = {
            1: self.play_quiz,
            2: self.add_quiz,
            3: self.list_quizzes,
            4: self.show_score,
            5: self.delete_quiz,
        }
        try:
            while True:
                self.show_menu()
                choice = read_int("선택: ", 1, EXIT_CHOICE)
                if choice == EXIT_CHOICE:
                    break
                actions[choice]()
        except ExitRequested:
            print("⚠️ 입력이 중단되어 안전하게 종료합니다.")
        self.save_state()
        print("👋 게임을 종료합니다.")
