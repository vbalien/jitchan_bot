start :
	@sudo ./slackbot.py
	@echo "start slackbot"
	@sudo ./telegrambot.py
	@echo "start telegrambot"
stop :
	@-ps -ef | grep -v grep | grep slackbot.py | awk '{print $$2}' | xargs sudo kill -9
	@-ps -ef | grep -v grep | grep telegrambot.py | awk '{print $$2}' | xargs sudo kill -9
