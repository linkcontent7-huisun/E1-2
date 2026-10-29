"""실행 진입점: python main.py"""
import sys

from game import QuizGame


def use_utf8_io():
    """한글 Windows(cp949 기본값)에서도 입출력이 깨지지 않도록 UTF-8로 맞춘다.

    출력: 이모지를 cp949로 인코딩하지 못해 죽는 문제를 막는다.
    입력: 잘못 해석된 글자가 저장 단계에서 UnicodeEncodeError를 일으키는 문제를 막는다.
    """
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")


if __name__ == "__main__":
    use_utf8_io()
    QuizGame().run()
