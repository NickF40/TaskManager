# Python-based Task Manager

### Project would be based on functional, that is done in `Buisbot` project

## Backend
- `memcached for storing current tasks`
- `PostgreSQL database for storing users information & system configurations`
- `Usage of Webhook, connected to Flask web server`
- `AsyncIO for running threaded tasks`

## Telegram module
- `PyTelegramBotAPI for connecting with Telegram Bot API`

## Vk module
- `Pure urllib2.request http requests + AsyncIO for sending requests to VK API`

# Stages:
- [x] Initialize files in `Backend` part
- [x] Initialize files in `Telegram` part
- [ ] Initialize files in `VK` part
- [x] Edit `README.md`
- [ ] Create some docs. and comment `*.py` files
- [ ] Finish `Backend`
- [ ] Finish `Telegram`
- [ ] Finish `VK`
- [ ] Finish documentation

# Todo:
- #### Create 'TaskManager` class, which contains:
  - `func., that cuts list of tasks from cache - if task._time ~ current time (using threading & async)`
  - `func., that saves new task to cache (using threading & async)`
  - `dunder-methods`
- #### Create `Task` class, which contains:
  - `funcs., that sets values to incapsulated lines`
  - `dunder-methods`
  - `json serialisers and deserialisers for mongodb`
- #### Create `TaskEditor` class, that:
  - `Connects to Telegram Bot API, and strarts sequence of questions to user, defining each line of Task class (multithreaded)`
  - `Connects to TaskManager instance and saves new Task`
  
