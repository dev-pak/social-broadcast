# social-broadcast

Бот для рассылки в ВК, Дискорд, Телеграм
На данный момент ссылки в дискорде не работают

Также в Вк при переписке с ботом действуют команды:
```
/sub                                        //для подписки
/unsub                                      //для отписки
/help                                       //для списка команд
```
Дважды подписаться или отписаться нельзя

Формат запроса:
```
{"message":"text",                          //обязательный аргумент
 "link":"vk.com",                           //необязательный аргумент, однако должен быть строго ссылкой на пост в вк
 "dispatchers":["vk","telegram","discord"]  //обязательный аргумент. может быть пустым
 "sign":"signature"}                        //no comments
 ```
 
При отказе доступа возвращает Forbidden. После выполнения запроса без ошибок возвращает список dispatchers и ok
