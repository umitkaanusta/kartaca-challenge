# Kartaca Hiring Challenge

Umit Kaan Usta - u.kaanusta@gmail.com

Key: `gAAAAABgUNOg5Rgr5DcgAujfKVukSq8yyWxrJLNOrwivY6EHHs4yUyJsf23-MwvrgkBdBrPu7MfDAcT67_nsYOAMKvD1_hwT11UiNdeksgrXqauNySfxUV3eCfP_8tdI4wGCkZ-Hwq1lds3QFLp2I3Emflom4YxTkuPorlal_Lj5lIHdMW4DOBtoYGBHS9tb_NWxtc6mdeik`


## What does the program do?
- REST API with GET, POST, PUT, DELETE endpoints
- Each request has random response time (between 0-3 secs)
- Log each response in the format `{request method}, {response time in ms}, {timestamp}`
- An async job sends each line of log to kafka as new lines are being written in the log file
- A consumer catches the log going to Kafka, writes it into a database
- Create a real-time dashboard, each request method has its color

## Installation and Running
- Make sure Docker and docker-compose are installed in your environment
- Open the terminal
- Download the repo with `git clone`
- `cd` to the location where the repo is installed
- Run `docker-compose up`
    - The REST API runs on `http://localhost:5000`
    - See the REST API reference to learn how to use the API
    
### What if I encounter an error?
Run the following with the given order:
- `docker volume prune`
- `docker container prune`
- `docker builder prune`
- `docker-compose down -v`
- `docker-compose up --force-recreate --build`

## REST API Reference

| Endpoint | Request Method | Description | Query Parameters |
| ------------ | -------------- | ----------- | ---------------- |
| `/api/kitties` | **GET** | Get all kitties or a get a specific kitty by its Id | `kitty_id: Optional[int]` |
| `/api/add-kitty` | **POST** | Create a kitty with its name | `name: str` |
| `/api/update-kitty` | **PUT** | Rename a kitty | `kitty_id: int, new_name: Optional[str]` |
| `/api/delete-kitty` | **DELETE** | Delete a kitty by its Id | `kitty_id: int` |

**Q:** Why do POST and PUT endpoints have query parameters `name` and `new_name`?

**A:** As said in RFC 3986, HTTP query strings as an URI part works as a non-hierarchical
way of locating a resource. The query parameters `name` and `new_name` do not locate a resource. 
They are there as a quick solution to the requirement *POST and PUT endpoints should be able to accept requests 
with an empty body* in the hiring challenge specification.

