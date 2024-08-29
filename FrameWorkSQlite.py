# Frame work program on CRUDS operations to work with sqlite3 database

import sqlite3
import sys
import os

INVALID_INPUT_MESSAGE = "Invalid input message\nInput should be in given option"
operation = ""
table = "fwTable"
configTable = "fwConfig"
database = "FrameWork.db"

def getConfiguredData():
	global updatablefieldNumbers
	global menu
	global messages
	data = cursor.execute(f"SELECT * FROM {configTable}").fetchall()
	menu = data[0][1]
	menu = menu.replace("\\n","\n")
	updatablefieldNumbers = eval(data[1][1])
	messages = eval(data[2][1])

def getFieldNames():
	global fieldNames
	fieldNames = []
	data = cursor.execute(f"PRAGMA table_info({table})").fetchall()
	for item in data:
		fieldNames.append(item[1])

def getUpdatableFieldNames():
	global updatableFieldNames
	updatableFieldNames = []
	for fieldNumber in updatablefieldNumbers:
		updatableFieldNames.append(fieldNames[fieldNumber])
		
def createRecord():
	fieldValues = []
	for fieldName in fieldNames:
		fieldValue = input(f"Enter the {fieldName}: ")
		fieldValues.append(fieldValue)
	fieldValues = list(map("\'{}\'".format, fieldValues))
	fieldValues = ",".join(fieldValues)
	cursor.execute(f"INSERT INTO {table} VALUES({fieldValues})")
	connection.commit()
	print("Record added!")

def showRecords():
	fields = ",".join(fieldNames)
	selectQuery = f"SELECT {fields} FROM {table}"
	records = cursor.execute(selectQuery).fetchall()
	for record in records:
		print("-"*30)
		for index,fieldValue in enumerate(record):
			print(f"{fieldNames[index]}: {fieldValue}")

def printRecord(record):
	for index,fieldValue in enumerate(record):
		print(f"{fieldNames[index]}: {fieldValue}")

def searchId():
	inputRecordId = input(f"Enter {fieldNames[0]} to {operation}: ")
	returnedValue = cursor.execute(f"SELECT {fieldNames[0]} FROM {table} WHERE {recordId} = '{inputRecordId}'").fetchall()
	if returnedValue == []:
		return None
	else:
		return inputRecordId

def updateRecord():
	global operation
	operation = "update"
	temproraryRecordId = searchId()
	if temproraryRecordId == None:
		print(messages['RecordCreated'])
	else:
		for index,field in enumerate(updatableFieldNames):
			print(f"{index+1}. Update {field}")
		choice = int(input("Enter your choice: "))
		if choice > 0 and choice <= len(updatableFieldNames):
			updatableField = updatableFieldNames[choice-1]
			newValue = input(f"Enter new {updatableField}: ")
			updateQuery = f"UPDATE {table} SET {updatableField} = {newValue} WHERE {recordId} = '{temproraryRecordId}'"
			cursor.execute(updateQuery)
			connection.commit()
			print(messages['RecordUpdated'])
		else:
			print(INVALID_INPUT_MESSAGE)

def deleteRecord():
	global operation
	operation = "delete"
	temproraryRecordId = searchId()
	if temproraryRecordId == None:
		print(messages['RecordNotFound'])
	else:
		choice = int(input("Press 1 to conform deletion: "))
		if choice == 1:
			cursor.execute(f"DELETE FROM {table} WHERE {recordId} = '{temproraryRecordId}'")
			connection.commit()
			print(messages['RecordDeleted'])

def searchRecord():
	global operation
	operation = "search"
	fields = ",".join(fieldNames)
	recordId = searchId()
	if recordId == None:
		print(messages['RecordNotFound'])
	else:
		selectQuery = f"SELECT {fields} FROM {table} WHERE {recordId} = '{recordId}'"
		record = cursor.execute(selectQuery).fetchall()
		printRecord(record[0])

if __name__ == "__main__":
	connection = sqlite3.connect(database)
	cursor = connection.cursor()
	getConfiguredData()
	getFieldNames()
	getUpdatableFieldNames()
	recordId = fieldNames[0]
	option = 1
	operations = [createRecord, showRecords,updateRecord, deleteRecord, searchRecord, deleteRecord]
	while option == 1:
		os.system('cls')
		print(menu)
		choice = int(input("Enter your choice: "))
		if choice > 0 and choice < 6:
			operations[choice-1]()
		elif choice == 6:
			print("Thank you!")
			connection.close()
			sys.exit()
		else:
			print(INVALID_INPUT_MESSAGE)
		option = int(input("Press 1 to continue: "))	