"""실행 진입점: python main.py"""
import sys

from game import QuizGame


def use_utf8_output():
    """한글 Windows 콘솔(cp949)에서 이모지 출력 시 죽지 않도록 출력 인코딩을 UTF-8로 맞춘다."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")


if __name__ == "__main__":
    use_utf8_output()
    QuizGame().run()
