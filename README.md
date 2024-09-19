# The Origins
Project

## Development setup


Clone this repository:

```
git clone https://github.com/ArduPilot/WebTools.git
```

Start project:

```
make up
```




## Instructions

For start project use  

```
make up
```

Variables:
```
{{base_url}}=0.0.0.0:8000

```
### Auth
Add user:
```
POST {{base_url}}/users/
BODY:
{"username": "username",
"role": "Admin",
"email": "username@gmail.com",
"password": "password"}
```
Get token:
```
POST {{base_url}}/token
BODY:
{
    "password": "password",
    "username": "username"
}
```

### Tasks

Create task 
```
POST {{base_url}}/tasks/
BODY:
{
    "title": "title",
    "responsible_person": 1,
    "executors": [1],
    "status": "TODO",
    "priority": 1
}
```
Get task
```
GET {{base_url}}/tasks/
BODY:
{
    "title": "title",
    "responsible_person": 1,
    "executors": [1],
    "status": "TODO",
    "priority": 1
}
```
Patch task
```
PATCH {{base_url}}/tasks/{{nn}}
BODY:
{
    "status": "IN_PROGRESS",
}
```
Delete task
```
DELETE {{base_url}}/tasks/{{nn}}
```
