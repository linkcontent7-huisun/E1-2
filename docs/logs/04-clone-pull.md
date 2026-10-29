# 04. clone / pull 실습

퀴즈 게임 개발이 끝난 뒤 수행했다. (1) 별도 디렉터리에 clone → (2) 복제본에서 README 수정 후 commit·push → (3) 원래 작업 디렉터리에서 pull → (4) 반영 확인.

## 1. 별도 디렉터리에 clone

```
$ git clone git@github.com:linkcontent7-huisun/E1-2.git E1-2-clone
Cloning into 'E1-2-clone'...
$ cd E1-2-clone && git log --oneline -1
2bc3647 Docs: README 작성 (개요, 주제 선정 이유, 실행 방법, 기능, 구조, state.json, 트러블슈팅)과 환경·실행 로그 추가
```

## 2. 복제본에서 README에 한 줄 추가 → commit → push

```
$ git diff --stat
 README.md | 4 ++++
 1 file changed, 4 insertions(+)
$ git commit -m "Docs: 복제본에서 README에 clone 실습 안내 한 줄 추가"
c01a528 Docs: 복제본에서 README에 clone 실습 안내 한 줄 추가
$ git push
To github.com:linkcontent7-huisun/E1-2.git
   2bc3647..c01a528  main -> main
```

## 3. 원래 작업 디렉터리에서 pull

```
$ git log --oneline -1   (pull 전)
2bc3647 Docs: README 작성 (개요, 주제 선정 이유, 실행 방법, 기능, 구조, state.json, 트러블슈팅)과 환경·실행 로그 추가
$ git pull
From github.com:linkcontent7-huisun/E1-2
   2bc3647..c01a528  main       -> origin/main
Updating 2bc3647..c01a528
Fast-forward
 README.md | 4 ++++
 1 file changed, 4 insertions(+)
$ git log --oneline -2   (pull 후)
c01a528 Docs: 복제본에서 README에 clone 실습 안내 한 줄 추가
2bc3647 Docs: README 작성 (개요, 주제 선정 이유, 실행 방법, 기능, 구조, state.json, 트러블슈팅)과 환경·실행 로그 추가
```

## 4. 반영 확인

```
$ tail -3 README.md
---

> 복제본(clone) 실습: 별도 폴더 `E1-2-clone`에서 이 줄을 추가해 push했고, 원래 폴더에서 pull로 받아 확인했다.
$ git status -sb | head -1
## main...origin/main
```
