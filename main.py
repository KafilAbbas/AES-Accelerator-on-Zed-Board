from decrypt.AES_decrypt import decrypt_and_save
from csv_files.extract import preprocess_the_ila_data


ila_csv_path = './csv_files/iladata3.csv'
csv_file_path = './csv_files/fourth_ila_readings.csv'
output_file_path = './input_output_txt/output_file.txt'


preprocess_the_ila_data(ila_csv_path,csv_file_path)
decrypt_and_save(csv_file_path,output_file_path)