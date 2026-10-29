# 03. Git 작업 기록

## 기초 명령 7종 사용 증거

| 명령 | 사용 증거 |
|---|---|
| init | 첫 커밋 `f0c73fc` 전에 `git init -b main` 실행 |
| add / commit | 아래 커밋 목록 전체 (`git add -A` 후 `git commit`) |
| push | `git push -u origin main` 이후 모든 커밋과 브랜치를 origin에 반영 |
| checkout | 아래 reflog의 `checkout: moving from …` 기록 |
| clone | [04-clone-pull.md](04-clone-pull.md) 1절 |
| pull | [04-clone-pull.md](04-clone-pull.md) 3절 (Fast-forward) |

### checkout 기록 (git reflog)

```
$ git reflog | grep checkout
cb1d4fe HEAD@{3}: checkout: moving from fix/utf8-stdin to main
cb1d4fe HEAD@{5}: checkout: moving from main to fix/utf8-stdin
68fd7c8 HEAD@{7}: checkout: moving from feature/bonus to main
68fd7c8 HEAD@{12}: checkout: moving from main to feature/bonus
cfe8fba HEAD@{20}: checkout: moving from feature/play-quiz to main
cfe8fba HEAD@{23}: checkout: moving from main to feature/play-quiz
```

## 브랜치 생성과 병합

```
$ git branch -a
  feature/bonus
  feature/play-quiz
  fix/utf8-stdin
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature/bonus
  remotes/origin/feature/play-quiz
  remotes/origin/fix/utf8-stdin
  remotes/origin/main

$ git log --merges --oneline
a6873ba Merge: fix/utf8-stdin UTF-8 입력 처리 수정을 main에 병합
cb1d4fe Merge: feature/bonus 보너스 5종(랜덤·문제 수·힌트·삭제·기록)을 main에 병합
29cbd58 Merge: feature/play-quiz 퀴즈 풀기 기능을 main에 병합
```

## 커밋 그래프

```
$ git log --oneline --graph --decorate
* c01a528 (HEAD -> main, origin/main, origin/HEAD) Docs: 복제본에서 README에 clone 실습 안내 한 줄 추가
* 2bc3647 Docs: README 작성 (개요, 주제 선정 이유, 실행 방법, 기능, 구조, state.json, 트러블슈팅)과 환경·실행 로그 추가
*   a6873ba Merge: fix/utf8-stdin UTF-8 입력 처리 수정을 main에 병합
|\  
| * 64abb38 (origin/fix/utf8-stdin, fix/utf8-stdin) Fix: UTF-8 파이프 입력의 한글이 저장 단계에서 UnicodeEncodeError를 내던 문제 수정
|/  
*   cb1d4fe Merge: feature/bonus 보너스 5종(랜덤·문제 수·힌트·삭제·기록)을 main에 병합
|\  
| * 7d0a36b (origin/feature/bonus, feature/bonus) Feat: 보너스 - 점수 기록 히스토리 (날짜/시간, 푼 문제 수, 점수)
| * f6539e5 Feat: 보너스 - 퀴즈 삭제 기능 (확인 절차와 파일 반영)
| * 9ce0d40 Feat: 보너스 - 힌트 기능 (힌트 사용 시 정답 0.5점 인정)
| * 1119bcc Feat: 보너스 - 랜덤 출제와 문제 수 선택
|/  
* 68fd7c8 Feat: 퀴즈 주제를 한국 가톨릭 성지순례 상식으로 변경 (VisitHolyKorea 연계, 10문항)
* dda8d33 Refactor: QuizGame 메뉴 분기를 기능 표(dict)로 정리
* ad1f62d Feat: state.json 저장·불러오기와 파일 손상 복구 구현
* 015997e Feat: 점수 확인과 최고 점수 갱신 구현 (미플레이 처리 포함)
* 4287905 Feat: 퀴즈 목록 기능 구현 (퀴즈 없음 처리 포함)
* 68a3756 Feat: 퀴즈 추가 기능 구현 (입력 검증 포함)
*   29cbd58 Merge: feature/play-quiz 퀴즈 풀기 기능을 main에 병합
|\  
| * e968225 (origin/feature/play-quiz, feature/play-quiz) Fix: 퀴즈 풀기 안내 문구의 줄바꿈이 깨져 SyntaxError가 나던 문제 수정
| * a6ee93a Feat: 퀴즈 풀기 구현 (출제, 정오답 안내, 결과 표시, 퀴즈 없음 처리)
|/  
* cfe8fba Feat: AI·개발 상식 기본 퀴즈 7개 작성 (Quiz 인스턴스)
* 1463d7e Feat: Quiz 클래스 구현 (출력, 정답 확인, dict 변환)
* ca0e37a Fix: cp949 콘솔에서 이모지 출력 시 UnicodeEncodeError 수정
* b95e343 Feat: 메뉴 출력과 입력 예외 처리 기반 구현
* f0c73fc Chore: 저장소 초기 설정 (.gitignore, README 뼈대)
```

## 커밋 수

```
$ git rev-list --count HEAD
23
$ git rev-list --count --no-merges HEAD   (병합 커밋 제외)
20
```
