
## API Reference

#### User Registration

```http
  POST /api/register/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | users username  (required)           |
| `password` | `string` | users username     (required)        |

#### User Login

```http
  POST /api/login/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `username` | `string` | users username  (required) |
| `password` | `string` | users password  (required) |

#### Get Access token

```http
  POST /api/token/refresh/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh` | `string` | refresh token  (required) |

#### Get Online users

```http
  GET /api/online-users/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| - | - | -  |


#### Logout

```http
  POST /api/logout/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `refresh` | `string` | refresh token   (required)  |

#### Friends Recommendation

```http
  GET /api/suggested-friends/<int:user_id>
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| - | - | -  |

#### Start a chat

```http
  POST /api/chat/start/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `receiver_id` | `string` | receivers username  (required) |

#### Send a message

```http
  WEBSOCKET /api/chat/send/
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `message` | `string` | message for receiver  (required) |
| `receiver` | `string` |  receivers username  (required) |


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
