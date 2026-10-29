"""입력 처리 공통 함수. 공백 제거, 숫자 변환, 범위 검사, 중단(Ctrl+C/EOF) 처리를 맡는다."""


class ExitRequested(Exception):
    """Ctrl+C 또는 입력 스트림 종료(EOF)가 발생했을 때 올리는 예외."""


def read_text(prompt):
    """한 줄을 읽어 앞뒤 공백을 제거해 돌려준다. 중단 입력은 ExitRequested로 바꾼다."""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print()
        raise ExitRequested


def read_nonempty(prompt):
    """빈 입력이면 안내하고 다시 받는다."""
    while True:
        text = read_text(prompt)
        if text:
            return text
        print("⚠️ 빈 입력입니다. 내용을 입력하세요.")


def read_int(prompt, low, high):
    """low~high 범위의 정수를 받을 때까지 반복한다."""
    while True:
        text = read_text(prompt)
        if not text:
            print("⚠️ 빈 입력입니다. 숫자를 입력하세요.")
            continue
        try:
            number = int(text)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= number <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return number
