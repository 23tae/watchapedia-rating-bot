# WatchaPedia Rating Bot

## Overview

이 프로그램은 Selenium을 사용하여 WatchaPedia 웹사이트에서 별점을 조정하는 봇입니다. 이 봇은 특정 유형의 콘텐츠(영화, TV 프로그램, 책, 웹툰)에 대한 별점을 자동으로 변경하는 프로세스를 자동화합니다.

## Prerequisites

사용하기 전에 필요한 의존성이 설치되어 있는지 확인하세요. 다음 명령어로 설치할 수 있습니다.

1. 가상환경 생성

- macOS

  ```shell
  python3 -m venv .venv
  ```

- Windows

  ```shell
  python -m venv .venv
  ```

2. 가상환경 활성화

- macOS

  ```shell
  source ./.venv/bin/activate
  ```

- Windows

  ```shell
  .\venv\Scripts\activate.bat
  ```

3. 패키지 설치

  ```shell
  pip install -r requirements.txt
  ```

## Usage

### `main.py`

메인 스크립트(main.py)는 프로그램의 진입점입니다. 명령줄 인수를 사용하여 콘텐츠의 유형과 원하는 별점을 지정합니다.

```bash
python main.py <type> <rating> [limit]
```

- type: 콘텐츠 유형 (m: 영화, t: TV 프로그램, b: 책, w: 웹툰)
- rating: 변경하려는 별점으로, 0.5에서 5.0까지 0.5 간격으로 지정합니다.
- limit (optional): 변경하려는 콘텐츠의 개수로, 1 이상의 값을 지정합니다. 값을 지정하지 않으면 모든 콘텐츠를 변경합니다.

### `adjust_rating.py`

이 모듈은 Selenium을 사용한 웹 스크래핑 및 별점 조정과 관련된 함수를 포함합니다.

### `check_validity.py`

이 모듈은 명령줄 인수를 확인하고 사용자 입력을 처리하며 콘텐츠 URL을 저장하는 출력 파일을 관리합니다.

## Configuration

`.env` 파일에서 WatchaPedia 계정 정보를 불러옵니다. 이 파일에 올바른 사용자 이름 및 비밀번호를 설정하십시오. (`env.example`에 맞게 입력)

## Execution

1. 명령줄에서 적절한 명령줄 인수와 함께 메인 스크립트를 실행하여 별점 조정 프로세스를 시작합니다.

  ```bash
  python main.py <type> <rating>
  ```

2. 봇은 자동으로 WatchaPedia에 로그인하고 지정된 콘텐츠 유형으로 이동하여 별점을 조정합니다.

3. 콘텐츠 URL을 저장하는 출력 파일을 다시 생성할지 여부를 확인하라는 프롬프트가 표시됩니다. 이 파일은 참조용으로 사용되며 향후 조정에 유용할 수 있습니다.

4. 프로세스가 완료되면 프로그램은 별점 조정이 완료되었음을 나타내는 메시지를 표시합니다.

## Disclaimer

본 소프트웨어 사용에 따른 모든 결과에 대한 책임은 사용자에게 있습니다. 개발자는 이에 대해 책임지지 않습니다.
