# Django Chat App

## API Reference

#### User Registration

```https
  POST /api/register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | users username  (required)           |
| `password` | `string` | users username     (required)        |

#### User Login

```https
  POST /api/login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username` | `string` | users username  (required) |
| `password` | `string` | users password  (required) |

#### Get Access token

```https
  POST /api/token/refresh/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh` | `string` | refresh token  (required) |

"*Note: Requires user authentication.*"

#### Get Online users

```https
  GET /api/online-users/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| - | - | -  |

"*Note: Requires user authentication.*"

#### Logout

```https
  POST /api/logout/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh` | `string` | refresh token   (required)  |

"*Note: Requires user authentication.*"
#### Friends Recommendation

```https
  GET /api/suggested-friends/<int:user_id>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| - | - | -  |


#### Start a chat

```https
  POST /api/chat/start/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `receiver_id` | `string` | receivers username  (required) |

"*Note: Requires user authentication.*"

#### Send a message

```https
  WEBSOCKET /api/chat/send/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `message` | `string` | message for receiver  (required) |
| `receiver` | `string` |  receivers username  (required) |

"*Note: Requires user authentication.*"

## Installation 

To install, run the following command

```bash
  $ pip install -r requirements.txt
```

```bash
  $ python manage.py makemigrations
```

```bash
  $ python manage.py migrate
```

```bash
  $ python manage.py runserver
```


I have also attached postman collections file in postman_collections folder for reference
