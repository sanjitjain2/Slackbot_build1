import os,slackclient
#xoxb-204855229783-69I76aQki6cyGcyi0gmJ35Wo
#slavebot
#U60R56RP1                                           
SLAVE_SLACK_NAME ='slavebot'
SLAVE_SLACK_TOKEN ='xoxb-204855229783-yoyi98I1PUWFslReooEJF354'

#initialize the slack client
slave_slack_client = slackclient.SlackClient(SLAVE_SLACK_TOKEN)

#check if everything is alright
print (SLAVE_SLACK_NAME)
print (SLAVE_SLACK_TOKEN)
is_ok = slave_slack_client.api_call("users.list").get('ok')
print(is_ok)

#find the id of the slack bot
if(is_ok):
	for user in slave_slack_client.api_call("users.list").get('members'):
		if user.get('name') == SLAVE_SLACK_NAME:
			print (user.get('id'))
