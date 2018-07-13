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
- #### Create `TaskManager` class, which contains:
  - `func., that cuts list of tasks from cache - if task._time ~ current time (using threading & async)`
  - `func., that saves new task to cache (using threading & async)`
  - 
  - `dunder-methods`
- #### Create `ProcessManager` class, which contains:
  - `funcs to Manage threads and AsyncTasks`
- #### Create `AyncTask` class, which contains:
  - `funcs, that will start \"timer\" Jobs`
- #### Create `BasicAPI` class, which would help to send task to multiple APIs anf Bots
  
# Done:
  - `pymemcache *Cache* class defined'
  - `*Task* class defined`
  - `WebServers defined (Flask & aiohtttp)`


# Architecture(v0.1):
- `Polling system`:
  - `ThreadPool 1>`:
    - `Telegram bot instance (polling)`
  - `ThreadPool 2`:
    - `VK bot instance (polling)`
  - `ThreadPool 3`:
    - `TaskManager.waiter`
  - `Main thread`


1. Each thread connects processes update and connects to main thread and sends request to TaskManager instance
2. TaskManager instance starts (async?) request to database(if it's needed)
3. Returns result to Bot instance
4. Bot sends async requests bask to user

  
