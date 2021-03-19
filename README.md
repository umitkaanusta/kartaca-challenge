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
will update here

## REST API Reference

| Endpoint | Request Method | Description | Query Parameters |
| ------------ | -------------- | ----------- | ---------------- |
| `/api/kitties` | **GET** | Get all kitties or a get a specific kitty by its Id | `kitty_id: Optional[int]` |
| `/api/add-kitty` | **POST** | Create a kitty with its name | `name: str` |
| `/api/update-kitty` | **PUT** | Rename a kitty | `kitty_id: int, new_name: Optional[str]` |
| `/api/delete-kitty` | **DELETE** | Delete a kitty by its Id | `kitty_id: int` |
