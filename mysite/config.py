class MyConfig:

    class App:
        MIN_ROOM_ID = 1
        MAX_ROOM_ID = 999
        SIZE_PASSWORD = 6
        MIN_ANSWERER_ID = 1
        MAX_ANSWERER_ID = 999
        ROOM_EXPIRE_SEC = 60 * 60 * 24
    
    class Redis:
        HOST = "127.0.0.1"
        PORT = 6379