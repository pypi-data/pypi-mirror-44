# dispatch
Python package for timed dispatching of events or work

# Usage

	### The Reactor ###
	from dispatch import Reactor

	r = Reactor()
	# The dispatch function needs two parameters, a schedule and an action
	schedule = r.schedule_interval(seconds=2) # Run every 2 seconds
	action = r.action(print, "hello") # Call the print function with the parameter "hello"
	r.dispatch(schedule, action)
	r.run()
	

	### The Actions ###
	# There are two helper functions that build actions based on functions:
	
	r.action(func, parameter, parameter2, kwarg1=value) # Runs in main loop
	r.background_action(func, parameter, parameter2, kwarg1=value) # Runs in new thread

	### The Schedules ###
	# A schedule is just an iterator that returns timestamps but there are 
	# several constructors included which make needing to write one rare

	from datetime import datetime

	# Run once on April 1st 2012 at 4 am
	r.schedule_one_time(datetime(2020,4,1,4)) 

	# Run on August 5th and 8th, 2020 
	timestamps = [datetime(2020, 8, 1), datetime(2020, 8, 5)]
	schedule = iter(timestamps) 

	# To run at 8am and 5pm on Tuesdays and thursdays
	r.schedule_calendar(days_of_week=["Tuesday", "Thursday"], hours=[8, 17])

	# To run hourly on the 15th minute
	r.schedule_hourly(minute=15)

	# To run daily at 5:12 pm 
	r.schedule_daily(hour=17, minute=12)

	# To run every hour and a half
	r.schedule_interval(hours=1, minutes=30)

	# To run every 26 hours till the year 2020 
	r.schedule_interval(days=1 hours=2, till=datetime(2020, 1, 1))

	# To run on the 1st 5th, 10th, 15th, 20th, and 25th of the month @ midnight
	r.schedule_calendar(days=[1,5,10,15,20,25])

	# To run mondays on every hour 
	r.schedule_calendar(days_of_week=['Monday'], hours='*')
