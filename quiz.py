"""개별 퀴즈 한 문제를 표현하는 Quiz 클래스."""

CHOICE_COUNT = 4


class Quiz:
    def __init__(self, question, choices, answer):
        if len(choices) != CHOICE_COUNT:
            raise ValueError(f"선택지는 {CHOICE_COUNT}개여야 합니다.")
        if not 1 <= answer <= CHOICE_COUNT:
            raise ValueError(f"정답은 1~{CHOICE_COUNT} 사이여야 합니다.")
        self.question = question
        self.choices = list(choices)
        self.answer = answer  # 1~4 번호로 관리한다.

    def display(self):
        """문제와 선택지를 출력한다."""
        print(self.question)
        print()
        for number, choice in enumerate(self.choices, start=1):
            print(f"{number}. {choice}")

    def is_correct(self, choice):
        """사용자가 고른 번호가 정답인지 확인한다."""
        return choice == self.answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices, "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        return cls(data["question"], data["choices"], data["answer"])
