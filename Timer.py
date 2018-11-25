class Timer:
    
    # Constructor
    # self.__start  : (int) Stores the time at which Timer was start (in milliseconds)
    # self.__time   : (int) Stores the time passed since Timer was started (in milliseconds)
    # self.__pause  : (bool) Shows if Timer is paused or not
    # self.__is_set : (bool) Shows if Timer is started or not
    def __init__(self):
        self.__start = 0
        self.__time = 0
        self.__pause = False
        self.__is_set = False
    
    @property
    def time(self):
        if self.__is_set and not self.__pause:
            self.__time = (hour() * 3600000 + minute() * 60000 + second() * 1000 + millis()) - self.__start
        return self.__time
    @property
    def is_set(self):
        return self.__is_set
    
    def start_timer(self):
        self.__start = hour() * 3600000 + minute() * 60000 + second() * 1000 + millis()
        self.__is_set = True
    def pause_timer(self):
        self.__time = (hour() * 3600000 + minute() * 60000 + second() * 1000 + millis()) - self.__start
        self.__pause = True
    def resume_timer(self):
        self.__pause = False
    def reset(self):
        self.__start = 0
        self.__time = 0
        self.__pause = False
        self.__is_set = False
