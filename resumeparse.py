import re
import os
import shutil
import docx2txt
import pdfplumber
import logging
import sys
import operator
import string
import mysql.connector
import aspose.words as aw


base_path = os.path.dirname(__file__)



class resumeparse(object):
    def convert_docx_to_txt(docx_file):
        try:
            print(docx_file)
            text = docx2txt.process(docx_file)  # Extract text from docx file
            print("242")
            
            clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            print("243")
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            print("244")
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces

            return resume_lines, text
        except KeyError:
            text = textract.process(docx_file)
            text = text.decode("utf-8")
            clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
            return resume_lines, text
        try:
            clean_text = re.sub(r'\n+', '\n', text)
            clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if
                            line.strip()]  # Remove empty strings and whitespaces
            return resume_lines, text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "

    def convert_doc_to_txt(doc_file):
        try:
            
            doc = aw.Document(doc_file)
            doc.save('True_Talent(doc_to_docx).docx')
            
            text = docx2txt.process('True_Talent(doc_to_docx).docx')  # Extract text from docx file
            
            resume_lines = ""
            clean_text = text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob            print("242")
            resume_lines = clean_text.splitlines()  # Split text blob into individual lines
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
            resume_lines = resume_lines[1:]
            resume_lines = resume_lines[:-3]
        
            return resume_lines, text
        except Exception as e:
            logging.error('Error in doc file:: ' + str(e))
            return [], " "




    def convert_pdf_to_txt(pdf_file):
        try:
            print("in excpt")          
            pdf = pdfplumber.open(pdf_file)
            raw_text= ""
            for page in pdf.pages:
                raw_text += page.extract_text() + "\n"
                
            pdf.close()  
            print('out except 313')              
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
        try:
            full_string = re.sub(r'\n+', '\n', raw_text)
            full_string = full_string.replace("\r", "\n")
            full_string = full_string.replace("\t", " ")

            # Remove awkward LaTeX bullet characters

            full_string = re.sub(r"\uf0b7", " ", full_string)
            full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
            full_string = re.sub(r'• ', " ", full_string)

            # Split text blob into individual lines
            resume_lines = full_string.splitlines(True)

            # Remove empty strings and whitespaces
            resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
            return resume_lines, raw_text
        except Exception as e:
            logging.error('Error in docx file:: ' + str(e))
            return [], " "
            
    

    def extract_email(text):
        email = re.findall(r"([^@|\s]+@[^@]+\.[^@|\s]+)", text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    
        
        
    
    def read_file(self, file, count_newfile, count_oldfile, count_dublicate, emailsave):
        """
        file : Give path of resume file
        docx_parser : Enter docx2txt or tika, by default is tika
        """
        # file = "/content/Asst Manager Trust Administration.docx"
        print("comming to file")
        print("\n\n\n\n File == ",file,"\n\n")
        
        count_newfile = int(count_newfile)
        count_oldfile = int(count_oldfile)
        print(count_newfile, "864")
        file = os.path.join(file)
        print("15")
        if file.endswith('docx'):
            print("in docx")
            resume_lines, raw_text = resumeparse.convert_docx_to_txt(file)
        
        elif file.endswith('doc') or file.endswith('.rtf'):
            resume_lines, raw_text = resumeparse.convert_doc_to_txt(file)
        
        elif file.endswith('pdf'):
            print("in pdf")
            resume_lines, raw_text = resumeparse.convert_pdf_to_txt(file)
        elif file.endswith('txt'):
            print("in txt")
            with open(file, 'r', encoding='latin') as f:
                resume_lines = f.readlines()

        else:
            resume_lines = None
        
        
        full_text = " ".join(resume_lines)

        
        
        
        def save_file(file_path, destination_directory, new_filename):
    
            if os.path.isfile(file_path):
        
                destination_path = os.path.join(destination_directory, new_filename)

        
                shutil.copy(file_path, destination_path)

                print("File saved successfully at")
            else:
                print(f"Error: File not found at {file_path}")

        def save_file1(file_path, destination_directory, new_filename):
    
            if os.path.isfile(file_path):
        
                destination_path = os.path.join(destination_directory, new_filename)
                shutil.copy(file_path, destination_path)

                print("File saved successfully at")
            else:
                print(f"Error: File not found at {file_path}")

        email = resumeparse.extract_email(full_text)
        found = False
        print(email, "882")
        

        # host = 'localhost'
        # user = 'root'
        # password = 'sai@12pra'
        # database = 'truetalent'
        # connection = mysql.connector.connect(
        # host=host,
        # user=user,
        # password=password,
        # database=database
        # )

        # for emailnew in emailsave:
        #     if emailnew == email:
        #         found = True
        #         break
        # if not found:
        #     emailsave.append(email)
        #     cursor = connection.cursor()
        #     query = "SELECT Email FROM email WHERE Email = %s"
        #     cursor.execute(query, (email,))
        #     row = cursor.fetchone()
        #     if row:
        #         print(f"Row with ID {email} exists:")
        #         print(row)
        #         count_oldfile +=1
        #         file_path = file
        #         destination_directory = "./Old files"
        #         new_filename = file
        #         save_file(file_path, destination_directory, new_filename)
        #     else:
        #         conn = mysql.connector.connect(
        #         user='root',
        #         password='sai@12pra',
        #         host='localhost',
        #         database='truetalent'
        #         )
        #         cursor = conn.cursor()
        #         insert_query = "SELECT * FROM email_email"
               
        #         cursor.execute(insert_query)
        #         rows = cursor.fetchall()
        #         print(rows, "sql")
        #         conn.commit
        #         cursor.close()
        #         conn.close()


        #         print(f"Row with ID {email} does not exist.")
        #         count_newfile += 1
        #         file_path = file
        #         destination_directory = "./New File"
        #         new_filename = file
        #         save_file(file_path, destination_directory, new_filename)
        # else:
        #     count_dublicate +=1
        #     file_path = file
        #     destination_directory = "./Old files"
        #     new_filename = file
        #     save_file(file_path, destination_directory, new_filename)
        # print(emailsave)   

        return {
            "email": email,
            "row_newfile": count_newfile,
            "row_oldfile": count_oldfile,
            "row_dublicate": count_dublicate
        }
    def display(self):
        print("\n\n ========= Inside display() ========== \n\n")
parser_obj = resumeparse()