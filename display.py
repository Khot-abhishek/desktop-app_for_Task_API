
def upper_window(username='NewUser'):
	current_user = username.center(28,' ')
	brand = 'Wonder List'.ljust(40)
	placement = current_user + brand + ' '*8 

	print('#'*80)
	print('#',' '*76,'#')
	print('#',placement,'#')
	print('#',' '*76, '#')
	print("#"*80)


def instruction_window():
	in_1 = '1: Add Task || 2: Update Task  || 3: Delete Task || 4: complete a task '
	in_2 = 'Enter ( q/Q ) to Quit'
	in_3 = '[Command no] : Your task title  : description(*optional)'

	print('Instructions'.center(80,'-'))
	print('#',' '*76, '#')
	# print('#',' '*76,'#')
	print('#',in_1.center(76, ' '), '#')
	print('#',in_2.center(76, ' '), '#')
	print('#',in_3.center(76, ' '), '#')
	# print('#',' '*76, '#')
	print('-'.center(80,'-'))


def display_task(id,title,status):
	result = f'[{id}] {title} | {status}'

	# print()
	# print('-'*80)	
	print(result.ljust(80,' '))
	print('-'*80)


if '__name__' == '__main__':
	
	upper_window()
	print()
	instruction_window()

