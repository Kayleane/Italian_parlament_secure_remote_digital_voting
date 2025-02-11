#!/usr/bin/python3 

from pathlib import Path
import time
import os
import hashlib

class Votazioni():

    #Count the number of ID
    def count_id():
        try:
            file = open('elenco.txt', 'r')
            count = int(file.read().count('\n'))
            file.close
            return count

        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e

    #Constructor
    def __init__(self):
        self.defid = self.count_id()
    
    #Set the id of the vote to use
    def set_id(self, id):
        self.defid = int(id)
    
    #Create a new vote
    def create_vote(self, name, desc, type, who):
        try:
            #Save current date and time
            datetime = time.strftime('%d/%m/%Y-%H:%M:%S')
            
            #Update the ID
            fileid = self.count_id + 1
            self.defid = fileid
            
            #Add the vote to the vote list file
            file = open('elenco.txt', 'a')
            file.write(str(fileid) + '_' + name + '_' + datetime + '\n')
            file.close()

            #Create the vote file and write things
            file = open(str(fileid) + '.txt', 'w')
            file.write('0\n')
            file.write(datetime + '\n')
            file.write(name + '\n')
            file.write(desc + '\n')
            file.write(type + '\n')
            file.write(who + '\n')
            file.close()

            return fileid

        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e
    
    #Add a vote to defined vote
    def add_vote(self, vote, name, id = None):
        try:
            if (id == None):
                file = open(str(self.defid) + '.txt', 'r+')
            else:
                file = open(str(id) + '.txt', 'r+')

            #Verify that the vote is open
            read = file.readline()
            if (int(read[1]) == 1):
                print('Votazione ancora in corso')
                return 1

            #Writing the vote
            text = str(vote) + '_' + name + '\n'
            file.seek(0, 2)
            file.write(text)
            file.close()

            return 0

        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e

    #Close vote
    def close_vote(self, id = None):
        try:
            if (id == None):
                filename = str(self.defid) + '.txt'
            else:
                filename = str(id) + '.txt'
            file = open(filename, 'r+')
            file.write('0')
            file.close()
            os.system('chmod 444 ' + filename)
            
            return 0
        
        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e
    
    #Return a dictionary with the result of a vote
    def res_vote(self, id = None):
        try:
            #Open file and verify that the vote is closed
            if (id == None):
                file = open(str(self.defid) + '.txt', 'r')
            else:
                file = open(str(id) + '.txt', 'r')
            
            if (int(file.readline()) == 0):
                print('Votazione ancora in corso')
                return 1

            #Read and save basic information
            datetime = file.readline()
            name = file.readline()
            desc = file.readline()
            type = file.readline()
            who = file.readline()

            #Initialize counter
            count0 = 0
            count1 = 0
            count2 = 0

            #Read and count the vote
            text = file.readline()
            while (text != ''):
                if (int(text[0]) == 0):
                    count0 = count0 + 1
                elif (int(text[0]) == 1):
                    count1 = count1 + 1
                elif (int(text[0]) == 2):
                    count2 = count2 + 1
                text = file.readline()
            
            #Generate the hash from the file
            file.seek(0, 0)
            md5 = hashlib.md5(file.read())
            hashmd5 = md5.hexdigest()

            file.close()

            #Create the dictionary
            res = {'datetime': datetime, 'name': name, 'description': desc, 'type': type, 'who': who, 'md5': hashmd5, 'yes': count0, 'no': count1, 'abstention': count2}

            return res

        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e
    
    def list_vote(self):
        try:
            lista = list()
            file = open('elenco.txt', 'r')

            #Read file and split the line
            text = file.readline()
            while (text != ''):
                splitted = text.split('_')
                lista.append({'id': splitted[0], 'name': splitted[1], 'datetime': splitted[2]})
                text = file.readline()
            
            file.close()
            return lista
        
        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e

    #Find the vote of a user in a defined vote
    def find_vote(self, name, id = None):
        try:
            if (id == None):
                file = open(str(self.defid) + '.txt', 'r')
            else:
                file = open(id + '.txt', 'r')
            text = file.readline()
            while (text != ''):
                splitted = text.split('_')
                if (text[1] == name):
                    file.close()
                    return splitted[0]
                text = file.readline()
            
            file.close()
            return -1

        except Exception as e:
            print('Error!')
            print('Exception message: ' + str(e))
            return e