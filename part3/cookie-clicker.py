"""
Cookie Clicker Simulator
Counting and optimization problem
http://www.codeskulptor.org/#user47_2WRkSR1T8g_39.py
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(50)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        """
        total_cookies :- total cookies made till this time
        cps			  :- cookies per second
        current_time  :- time elapsed
        current_no_cookies :- net cookie
        history_list  :- We will track the history as a list of tuples 
                        a time, an item that was bought at that time, the cost of the item, 
                        and the total number of cookies produced by that time.
                        
        """
        self._total_cookies = 0.0
        self._current_no_cookies = 0.0
        self._cps = 1.0
        self._current_time = 0.0
        self._history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        return "Total: " + str(self._total_cookies) + " Current Cookies: "+\
                str(self._current_no_cookies) + " CPS: " + str(self._cps)+" Time: "+str(self._current_time)+\
                "History (length: "+ str(len(self._history_list))+"): "+str(self._history_list)
    
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_no_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history_list[:]

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        cookie_needed = cookies - self.get_cookies() 
        time_needed = 0.0
        if cookie_needed > 0:
            time_needed = math.ceil(cookie_needed / self.get_cps())
            #time_needed = cookie_needed / self.get_cps()
        return time_needed

    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time <= 0.0:
            return
        self._total_cookies += time*self._cps
        self._current_no_cookies += time*self._cps
        self._current_time += time

    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        print '\n\n\nbuy item function call', item_name, cost, additional_cps
        if self._current_no_cookies >= cost:
            # a time, an item that was bought at that time None, the cost of the item, and 
            # the total number of cookies produced by that time.
            
            (self._history_list).append(tuple((self.get_time(), item_name, cost, self._total_cookies)))
            self._current_no_cookies -= cost
            self._cps += additional_cps
            print '>>>>>>>> length of history list', len(self._history_list)

   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    my_build_info = build_info.clone()
    my_cookie_clicker = ClickerState()
    
    current_time = my_cookie_clicker.get_time()
    
    if strategy is not None:
        while True:#current_time < duration:    
            print str(my_cookie_clicker)
            
            time_left = duration -  current_time
            cookies = my_cookie_clicker.get_cookies()
            cps = my_cookie_clicker.get_cps()
            history = my_cookie_clicker.get_history()
            
            item = strategy(cookies, cps, history, time_left, my_build_info)
            if item is None:
                break
            
            waiting_time = my_cookie_clicker.time_until(my_build_info.get_cost(item))
            print 'waiting_time ', waiting_time
            
            if (waiting_time +  current_time) > duration:
                break
           
            my_cookie_clicker.wait(waiting_time)
            my_cookie_clicker.buy_item(item, my_build_info.get_cost(item), my_build_info.get_cps(item))
            my_build_info.update_item(item)
            current_time = my_cookie_clicker.get_time()
    
    if current_time < duration:
        my_cookie_clicker.wait(duration - current_time)
    return my_cookie_clicker



def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    items =[(item, build_info.get_cost(item)) for item in build_info.build_items()]
    items.sort(key = lambda x:x[1])
    cheap = None
    if (time_left*cps + cookies)>= items[0][1]:
        cheap = items[0][0]
    return cheap

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    items =[(item, build_info.get_cost(item)) for item in build_info.build_items()]
    items.sort(key = lambda x:x[1], reverse= True)
    expensive = None
    cookies += time_left*cps
    print items, cookies
    for element in items:
        if element[1] <= cookies:
            expensive = element[0]
            break
    return expensive

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    best = None
    
    items = [
            (item, build_info.get_cost(item), build_info.get_cps(item)) 
        for item in build_info.build_items()
    ]
    items.sort(key = lambda x:x[2]/x[1], reverse = True)
    
    cookies += time_left*cps
    for ele in items:
        if cookies >= ele[1]:
            best = ele[0]
            break
    return best
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
# print strategy_cheap(2.0, 1.0, [(0.0, None, 0.0, 0.0)], 1.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15))    
# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.1]}, 1.15), 10000000000.0, strategy_cursor_broken)
# print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 50.0]}, 1.15), 16.0,  strategy_cursor_broken)

# print  strategy_cheap(2.0, 1.0, [(0.0, None, 0.0, 0.0)], 1.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 
# cookies, cps, history, time_left, build_info
#print  strategy_expensive(500000.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 

