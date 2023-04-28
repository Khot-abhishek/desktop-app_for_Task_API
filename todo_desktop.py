import requests
import json
import display as dp
import os 


BASE_URL = 'http://127.0.0.1:8000/api/'


class User:
	def __init__(self):
		self.id = None
		self.username = None
		self.USER_AUTHENTICATED = False

	def get_current_user(self, username=None):
		f_url = f'user/{username}'
		response = requests.get(url = BASE_URL+f_url)
		result = response.json()
		self.id = result.get('id')
		self.username = result.get('username')
		if username is not None:
			self.USER_AUTHENTICATED = True
			return True
		return False


	def login_user(self):
		print('Enter you credentials')
		username = input('Enter username: ')
		password = input('password: ')
		authenticated = self.get_current_user(username)
		if not authenticated:
			self.login_user()


class Task:
	def __init__(self):
		self.all_tasks = {}

	def get_present_tasks(self, id):
		f_url = f'tasks/{id}/'
		response = requests.get(url=BASE_URL+f_url)
		tasks = response.json()
		self.update_user_tasks(tasks)
		# print('tasks: ',tasks)

	def update_user_tasks(self, tasks):
		for task in tasks:
			self.all_tasks[task.get('id')] = task

	def display_all_tasks(self):
		for key,value in self.all_tasks.items():
			t_id = key
			t_title = value.get('title')
			t_descp = value.get('description')
			t_status = 'COMPLETED' if value.get('completed')==True else 'NOT -Completed' 

			dp.display_task(t_id,t_title,t_status)

	def add(self,user_id,title=None, descp=None):
		f_url = 'create/'
		headers = {'Content-Type': 'application/json'}

		if descp is not None:
			data = {'user':int(user_id),'title':title, 'description':descp, 'completed':False}
			json_data = json.dumps(data)
			
		else:
			data = {'user':int(user_id),'title':title, 'description':'', 'completed':False}
			json_data = json.dumps(data)
		
		response = requests.post(url=BASE_URL+f_url, data=json_data, headers=headers)
		if response.status_code == 201:
			print('task created')
			return True
		print('Something went wrong ... please enter again')
		print('status: ',response.status_code)
		return False


	def update(self,user_id,task_id,title=None,descp=None):
		if title != None and descp == None:
			data = {'user':int(user_id),'title':title}
			print('data selected : 1')
		elif title == None and descp != None:
			data = {'user':int(user_id), 'description':descp}
			print('data selected : 2')
		else:
			data = {'user':int(user_id),'title':title, 'description':descp}
			print('data selected : 3')

		print('data before json: ',data)
		json_data = json.dumps(data)
		print('json data : ',json_data)

		headers = {'Content-Type': 'application/json'}
		f_url = f'update/{task_id}/'
		response = requests.patch(url=BASE_URL+f_url, data=json_data, headers=headers)
		if response.status_code == 200:
			print('task Updated')
			return True
		print('Something went wrong ... please enter again')
		print('status: ',response.status_code)
		return False



	def delete(self,user_id, task_id):
		task_id = int( task_id.strip() )
		f_url = f'delete/{task_id}'
		response = requests.delete(url=BASE_URL+f_url)
		if response.status_code == 204:
			print('task Deleted')
			return True
		print('Something went wrong ... please enter again')
		print('status: ',response.status_code)
		return False

	def mark_task_complete(self,user_id,task_id):
		f_url = f'completed/{task_id}/'
		headers = {'Content-Type': 'application/json'}
		data = {'user':int(user_id),'completed':True}
		json_data = json.dumps(data)
		response = requests.post(url=BASE_URL+f_url,headers=headers, data=json_data)
		if response.status_code == 200:
			print('task marked completed')
			return True
		print('Something went wrong ... please enter again')
		print('status: ',response.status_code)
		return False


class App:
	def __init__(self, user, tasks):
		self.user = user
		self.tasks = tasks

	def display_screen(self):
		dp.upper_window(self.user.username)
		self.tasks.display_all_tasks()
		dp.instruction_window()

	def complete_response(self,response):
		title = None
		descp = None
		task_id = None
		command_no = response[0]

		if command_no == '1':
			if len(response) == 3:
				command_no, title, descp = response
			elif len(response) == 2:
				command_no, title = response
			return self.tasks.add(self.user.id,title,descp)
		elif command_no == '2':
			if len(response) == 4:
				_,task_id, title, descp = response
			elif len(response) == 3:
				_,task_id, title = response
			print('command_no :',_,task_id, title, descp)
			status = self.tasks.update(self.user.id,task_id,title,descp)
			return status
		elif command_no == '3':
			status =  self.tasks.delete(self.user.id, title)
			return status
		elif command_no == '4':
			_, task_id = response
			status = self.tasks.mark_task_complete(self.user.id, task_id)
			return status

	def get_input(self):
		response = input('Enter Instruction: ').split(':')
		if 'q' in response or 'Q' in response:
			global RUNNING
			RUNNING = False
			return
		success = self.complete_response(response)
		if not success:
			self.get_input()


	def run(self):
		if not self.user.USER_AUTHENTICATED:
			self.user.login_user()
		self.tasks.get_present_tasks(self.user.id)
		self.display_screen()
		self.get_input()


current_user = User()
current_tasks = Task()

tasks_app = App(current_user, current_tasks)
RUNNING = True

cycle_num = 1

while RUNNING:
	print(f'CYCLE NUMBER: {cycle_num}')
	tasks_app.run()
	os.system('cls')
	cycle_num += 1