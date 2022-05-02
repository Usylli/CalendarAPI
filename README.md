# CalendarAPI

Бек-энд (REST API) для простого приложения “Календарь” с поддержкой
авторизации, оповещения о приближающихся событиях и возможностью добавления пользовательских событий.
____

Already deployed on [Heroku](http://calendar-usylli.herokuapp.com/events/)

____

### Registration

To register template, follow the link:
> /auth/register/

To register API, send request auth/api/register_user/. Example:

Request (POST-method):
```
{
    "email_address" : "test@gmail.com",
    "username" : "test",
    "password" : "1234",
    "name" : "test"
}
```
Response:
```
redirect to login
```

### Login

To login template, follow the link: 
> /auth/login

To login API, send request to /api-auth/login_user/. Example: 
Request (POST-method):
```
{
    "email_address": "test@gmail.com",
    "password": "1234"
}
```

Response:
```
redirect to Events, access_token saved to cookie
```


**Note:**
*For all of the following requests insert the token into the request header, for example:*
*headers = {"Authorization": "Token 0f9ccdafdd2d356d5215ae08ecf12ac9903bd307"}*


### Create an event

> /events/add Event add template

>To create event by API, send request to /events/api/create_event. Example:

Request (POST-method):
```
{
    "name": "test_event",
    "start_date": "2022-04-15T15:30:00+06:00",
    "end_date": "2022-04-15T16:30:00+06:00",
    "ReminderTime": "2022-04-15T14:30:00+06:00"
}
```

- "start_date" - enter start datetime of event (required field)  
- "end_date" - enter datetime end of event (default = "23:59:59")  
- "ReminderTime" - enter reminder datetime for email notification.

Response:
```
{
  "user":4,
  "message":"event created successfully",
  "name":"test_event",
  "start_date":"2022-07-15T15:30:00+06:00",
  "end_date":"2022-07-15T16:30:00+06:00",
  "ReminderTime":"2022-05-02T23:30:00+06:00"
}
```

### Getting a list of events 

> /events/ for list events template

Request (GET-method) to /events/api/list/ 

Response:
```
[
    {
        "user": 4,
        "name": "test_event",
        "start_date": "2021-07-15T18:30:00+06:00",
        "end_date": "2021-07-15T19:30:00+06:00",
        "ReminderTime": "2021-07-15T17:30:00+06:00"
    },
    {
        ...
    }
]
```

### Getting the general aggregation of events by month

> /events?month=4

Request (GET-method with params) to /events/api/list/ 

Response:
```
{
    [
        {
          "user": 4,
          "name": "test_event",
          "start_date": "2021-04-15T18:30:00+06:00",
          "end_date": "2021-04-15T19:30:00+06:00",
          "ReminderTime": "2021-04-15T17:30:00+06:00"
        },
        {
            ...
        }
    ],
    ...
}
```
