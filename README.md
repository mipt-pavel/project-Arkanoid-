# "Арканоид"

# "В планах на этот проект"
1. Сделать несложный арканоид.
2. Добавить несколько уровней.
3. Разные типы "врагов".
4. Счётчик очков.
5. Разные способности для платформы.
6. Поэкспериментировать с отскоками от платформы.
7. Добавить музыку на фон.

Авторы:
- Андрей Клочан
- Степан Глушак
- Павел Недобежкин

Необходимые библиотеки:
- pygame 2.5.2

# Описание игры Арканоид
![Шарик из игры](/sprites/game_screenshot.png)

Игрок контролирует небольшую платформу-ракетку, которую можно передвигать горизонтально от одной стенки до другой, подставляя её под шарик, предотвращая его падение вниз. Для перехода на новый уровень необходимо уничтожить всех врагов.
## Управление
- Движение платформы осуществляется с помощью стрелок на клавиатуре
- Для активации способности необходимо нажать левой кнопкой мыши на её иконку
- Чтобы поставить игру на паузу, необходимо нажать соответствуюущую кнопку в игровом интерфейсе
(Подсказка об управлении реализована в игровом интерфейсе, под соответствующей кнопкой помощи - "?")

![Подсказка из игры](/sprites/buttons/help.png)

## Типы врагов
Для увеличения сложности игры и интереса к прохождению созданы три типа врагов:
### Чушпан

![Обычный враг из игры](/sprites/enemies/enemy.png)

Обычный враг, имеет одну жизнь. 
При смерти дает игроку 10 очков.
### Бронированный

![Бронированный враг из игры](/sprites/enemies/armored_enemy.png)

В отличии от предыдущего типа имеет три жизни
При смерти дает игроку 30 очков.
### Стрелок

![Стрелок из игры](/sprites/enemies/shooter_enemy.png)

Имеет две жизни, при этом сам стреляет по игроку с периодичностью в две секунды
При смерти дает игроку 40 очков.
## Способности
В правом меню отображаются иконки способностей (учитывается их доступность - "яркие", когда активны и "тусклые" в ином случае). при их активации у игрока снимаются n очков, где n - цена способности.
### Пушка

![Иконка пушки](/sprites/buttons/gun_button01.png)

Стреляет пулей из середины платфомы, отнимает одну жизнь у врагов.
Цена - 10 очков
### Щит

![Иконка щита](/sprites/buttons/shield_button01.png)

Защищает платформу от двух попаданий в нее.
Цена - 15 очков
### Восстановление жизни

![Иконка восстановления жизни](/sprites/buttons/heal_button01.png)

Прибавляет платформе одну жизнь.
Цена - 20 очков
