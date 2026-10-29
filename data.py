"""기본 퀴즈 데이터: 주제는 'AI·개발 상식'."""
from quiz import Quiz


def default_quizzes():
    return [
        Quiz("Python을 만든 사람은?",
             ["Guido van Rossum", "Linus Torvalds", "Bjarne Stroustrup", "James Gosling"], 1),
        Quiz("분산 버전 관리 도구 Git을 만든 사람은?",
             ["Dennis Ritchie", "Linus Torvalds", "Ken Thompson", "Guido van Rossum"], 2),
        Quiz("HTTP 상태 코드 404가 뜻하는 것은?",
             ["서버 내부 오류", "접근 권한 없음", "요청한 페이지를 찾을 수 없음", "요청 성공"], 3),
        Quiz("Docker 이미지를 실제로 실행한 인스턴스를 무엇이라 부를까?",
             ["볼륨", "레지스트리", "네트워크", "컨테이너"], 4),
        Quiz("ChatGPT 같은 모델을 가리키는 LLM의 뜻은?",
             ["Large Language Model", "Linear Logic Machine", "Low Latency Module", "Local Learning Memory"], 1),
        Quiz("JSON은 무엇의 약자일까?",
             ["Java Standard Object Network", "JavaScript Object Notation",
              "Joint Syntax Operation Node", "Java Source Open Name"], 2),
        Quiz("원격 저장소를 내 컴퓨터로 통째로 복제하는 Git 명령은?",
             ["git push", "git merge", "git clone", "git init"], 3),
    ]
