---
title: Rails & Rake
date: "2023-12-26"
template: "post"
draft: false
slug: "/posts/rails-and-rake"
category: "Rails"
tags:
  - "Rails"
  - "Rake"
  - "Ruby on Rails"
description: "rails, tasks, rake 관련 포스트"
socialImage: ""
---

## Rake

먼저 rake가 뭔지 체크하고 넘어가자.

rake는 작업 정의 및 실행을 위한 DSL(도메인별 언어)을 제공하는 Ruby의 명령줄 유틸리티다.

rake는 확장자로 `*.rake`을 이용한다.

- `.rake`와 `.rb` 두 확장자 모두 ruby로 로드 된다. 다만 rb 확장자일 경우, rake 프로그램 실행 시 파일을 읽을 수 없다.

쉘에 아래 커맨드를 치면 이용 가능한 taske들을 확인할 수 있다.

```
rake -T
# or
rake --task
```

## Rakefile

ruby script이며 ruby 문법을 그대로 사용할 수 있다.

Rails 프로젝트를 보면 프로젝트의 루트 디렉토리에 Rakefile이 존재한다.

쉘에 rake 명령어를 입력하면, 자동으로 Rakefile script를 실행하고, `Rails.application.load_tasks`를 통해 `lib/tasks` 경로에 있는 `*.rake` 파일을 읽어온다.

```
# Add your own tasks in files placed in lib/tasks ending in .rake,
# for example lib/tasks/capistrano.rake, and they will automatically be available to Rake.

require_relative "config/application"

Rails.application.load_tasks
```

## 사용 방법

### 기본

사실 lib/tasks 파일을 이용할 필요는 없다.

그냥 Rakefile 안에 모든 task들을 넣어도 된다.

```
require_relative "config/application"

Rails.application.load_tasks

task :say_hi do
  p "hi"
end

task :say_hello do
  p "hello"
end
```

가능은 하지만 안티패턴이다.

lib/tasks 폴더 하위에 기능별로 파일을 만들어서 구분을 해주자.

그렇다면 `lib/tasks` 하위에 say.rake를 넣어보기로 하자.

```
task :hello do
  p "hello"
end
```

```
rake hello
#=> "hello"
```

주의할 점은 파일명이 “say”라고 해서 `rake say`라고 치면 안 된다는 점이다. rake 파일 내에 생성한 task를 쳐야한다.

내가 주로 사용하는 방식은 파일명과 동일한 namespace를 적용해주는 것이다.

```
namespace :say do
  task :hello do
    p "hello"
  end
end
```

```
rake say:hello
#=> "hello"
```

또한 rake 파일에는 처음 말했다시피 ruby 문법을 그대로 사용 가능하다.

```
class SaySomething
  def self.hello
    p "hello"
  end

  def self.introduce(name)
    p "Hi. My name is #{name}"
  end
end

namespace :say do
  task :hello do
    SaySomething.hello
  end

  task :introduce do
    SaySomething.introduce("jehoon")
  end
end
```

```
rake say:introduce
#=> "Hi. My name is jehoon"
```

### 환경별

우리가 만든 모델 중 User가 있다고 하자. 매달 타겟 유저의 포인트를 0으로 초기화해줘야 한다.

environment를 설정할 경우, 환경별 DB에서 데이터를 가져올 수 있다.

```
namespace :monthly_update do
    namespace :target_users_point_to_zero do
        task point_zero: :environment do
            User.specific_target.update(point: 0)
        end
    end
end
```

### desc

task를 만들고 `rake —-task` 를 치면 내가 만든 task가 보이지 않는다.

task 윗줄에 desc를 작성하면 `rake —task`에서 확인할 수 있다.

```
namespace :monthly_update do
	namespace :target_users_point_to_zero do
		desc "update user monthly"
		task point_zero: :environment do
			User.specific_target.update(point: 0)
	  end
	end
end
```

## 그 외

### rake와 rails 명령어

```
rake say_hi
#=> "hi"

rails say_hi
#=> "hi"
```

rake도 task를 실행하고, rails도 task를 실행한다.

그럼 뭘 쓰는게 좋냐?

rails의 경우 전체 rails 어플리케이션을 로드하기 때문에 rake에 비해 무겁다.

다만 경우에 따라 rails application의 종속성이 있을 수 있어 시간이 오래 걸릴 수 있다.

지금까지 설명한 내용은 task와 관련된 내용으로, 다른 명령어일 경우 `bundle exec rails generate` 와 같이 rake로는 실행 불가능한 명령어가 있을 수 있다. `bundle exec rails --help`로 확인해보자.

---

### 참고

*https://stackoverflow.com/questions/66311919/what-is-the-difference-between-rails-and-rake*
