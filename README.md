# DDD Layerd 를 적용한 리펙토링 레포지토리 입니다.

기본 구조는 아래와 같습니다.

```
/
app/
  di/container.py
  domain1/
    application/
      service/
      dto/
    infrastructure/
      entities/
      repositories/
  domain2/
    application/
      service/
      dto/
    infrastructure/
      entities/
      repositories/
  main.py
core/
  applications/
    dtos/base_dto.py
    services/base_service.py
  infrastructure/
     database/database.py
     redis/client.py
     di/core_container.py
     entities/base_entity.py
     setting/settings.py
     middleware/
       (하위 설정 middleware).py
     models/
       model1.py
       model2.py
router/
  domain1.py
  domain2.py
run_server.py
```


초기엔 다소 복잡하고 어렵게 느껴지실 수 있습니다.
하지만 예제 코드를 보면 이해가 간단해집니다.

![image](https://github.com/user-attachments/assets/5a0fc04b-2f02-4eca-9a65-f93c46cf3a36)
상기 코드를 보면, client와의 통신만을 담당합니다.
통신을 위한 데이터의 송수신은 DTO(Data Transfer Object)로 하는것을 원칙으로 합니다.
Service와 repository는 container단에서 의존성 주입을 통해 관리해줍니다.

![image](https://github.com/user-attachments/assets/8d1f380c-5078-465b-afe3-fe10a8f78238)
repository 계층은 database와의 입출력을 담당하는 계층으로서 사용됩니다.
담당하는 rdb라면 session과 redis라면 client는 CoreContainer에서 정의하며 이를 DI container가 생성자 매개변수에 맞게 값을 넣어줍니다.
repository 는 singleton으로 선언을 원칙으로 합니다. 이는 자원의 효율성을 위한 행위이며, 
session을 DI로 매번 다른 인스턴스를 주입하면서 사용하는 것이 맞습니다.
(repository 생성 시, session=CoreConatiner.database.provided.session 부분을 삭제하고, 함수마다 session을 입력받아 처리하게 하는 것이 원칙적으로 맞음.
다만, 개발 편의성을 생각하여 우선적으로 제외시켜 둔 항목이며 추후 개선 항목 1순위임.)

service 계층에선, 해당 repository를 인자로 받아 사용하며, 실질적인 비즈니스 로직과 유스케이스를 구현하게 됩니다. 
(use_case 계층을 따로 분할하여도 무관하며, 분리하여 처리하려다 아키텍쳐에 대한 이해가 어려울 것 같아 service 계층으로 통일함.)



