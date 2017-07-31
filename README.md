# Bibinet-parser
Test task for bibinet.ru

Тестовое задание для вакансии “Программист-разработчик” в компанию bibinet.ru

Формулировка задания от работодателя:

Требуется написать скрипт на Perl (или Python), выполняющий сканирование страниц сайта и загрузку разобранных данных в таблицу базы данных Postgresql. 
Основная цель задания - продемонстрировать навыки работы с регулярными выражениями. 
 
Есть страница  https://bibinet.ru/part/all/honda/
 
необходимо собрать информацию для двух моделей из списка, но только если у модели есть запчасти. Страниц запчастей надо сканировать первые 3, если всего страниц меньше, то все что есть.
 
Например, должны быть просканированы следующие страницы:
 
https://bibinet.ru/part/all/honda/accord/
https://bibinet.ru/search/parts/all/honda/accord/?page=2
https://bibinet.ru/search/parts/all/honda/accord/?page=3
 
С каждой страницы необходимо вытащить следующие данные для запчасти:
 - Наименование запчасти (например, ДВИГАТЕЛЬ)
 - Марку
 - Цена
 - Название компании
 - Фото (если есть)
 
Разобрать с помощью регулярных выражений третий столбик "АВТОМОБИЛЬ" и получить данные:
- модель
- кузов
- двигатель
- год
 
Таблица БД для хранения:
CREATE TABLE parts (
  id serial PRIMARY KEY,
  part_type character varying(100),
  mark character varying(100),
  model character varying(100),
  frame character varying(50),
  engine character varying(50),
  year character varying(4),
  price double precision,
  company character varying(100),
  photo  character varying(100)
);
 
Фотографии сохранять на диске, а в базе писать путь до нее.
