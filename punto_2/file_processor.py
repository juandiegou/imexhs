# Class that can handle and process files

import os
import logging
import pandas as pd
from datetime import datetime
from typing import Optional, List, Tuple


class FileProcessor:
    
    
    def __init__(self, path):
        logging.basicConfig(filename=f'{path}/file_processor.txt', filemode='a', level=logging.INFO, format='%(asctime)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.path = path
        
    def __file_exists__(self, filename):
        return os.path.exists(os.path.join(self.path, filename))
    
    def __is_csv__(self, filename):
        return filename.endswith('.csv')
    
    def __is_dicom__(self, filename):
        return filename.endswith('.dicom')
        
    def list_folder_content(self, folder_name: str, details: bool = False) -> None:
        files = []
        folders = []
        try:
            path = os.path.join(self.path, folder_name)
            if details:
                for f in os.listdir(path):
                    full_path = os.path.join(path, f)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(full_path)).strftime('%Y-%m-%d %H:%M:%S')
                    if os.path.isfile(full_path):
                        size = f"{os.path.getsize(full_path)/1048576:.2f} MB"
                        files.append(f"- {f} ({size}, Last Modified: {mod_time})")
                    else:
                        folders.append(f"- {f} (Last Modified: {mod_time})")
                
                print("Files:")
                for file in files:
                    print(file)
                    self.logger.info(file)
                
                print("\nFolders:")
                for folder in folders:
                    print(folder)
                    self.logger.info(folder)
            else:
                files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
                print("\n".join(files))
                self.logger.info("\n".join(files))
                
        except FileNotFoundError:
            self.logger.exception(f"Folder {folder_name} not found.")            
            return

                
    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False) -> None:
        try:
            df = pd.read_csv(os.path.join(self.path, filename))
            
            if summary:
                print("CSV Analysis:")
                print(f"Columns: {list(df.columns)}")
                print(f"Rows: {len(df)}")
                
                # Handle numeric columns
                numeric_cols = df.select_dtypes(include='number')
                if not numeric_cols.empty:
                    print("Numeric Columns:", end=" ")
                    stats = numeric_cols.agg(['mean', 'std']).round(1)
                    for col in numeric_cols.columns:
                        print(f"- {col}: Average = {stats.loc['mean', col]}, Std Dev = {stats.loc['std', col]}", end=" \n")
                
                # Handle non-numeric columns
                non_numeric = df.select_dtypes(exclude='number')
                if not non_numeric.empty:
                    print("\nNon-Numeric Summary:", end=" \n")
                    for col in non_numeric.columns:
                        unique_count = df[col].nunique()
                        print(f"- {col}: Unique Values = {unique_count}", end=" \n")
                    
                    # for col in non_numeric.columns:
                    #     print(f"\n{col} frequency:")
                    #     print(df[col].value_counts())
                        
            
            if report_path:
                summary_stats = numeric_cols.agg(['mean', 'std']).round(2)
                summary_stats.to_csv(os.path.join(report_path, f'{filename}_summary.txt'))
                
        except FileNotFoundError:
            self.logger.error(f"File {filename} not found")
            return None
        except pd.errors.EmptyDataError:
            self.logger.error(f"File {filename} is empty")
            return None
        except Exception as err:
            self.logger.error(f"Error processing file {filename}: {str(err)}")
            return None

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False) -> None:
        try:
            import pydicom
            from pydicom.errors import InvalidDicomError
            import matplotlib.pyplot as plt

            dicom_path = os.path.join(self.path, filename)
            ds = pydicom.dcmread(dicom_path)

            # Print basic information
            print("\nDicom Analysis:")
            print(f"Patient's Name: {ds.PatientName}")
            print(f"Study Date: {datetime.strptime(ds.StudyDate, '%Y%m%d').strftime('%Y-%m-%d')}")
            print(f"Modality: {ds.Modality}")


            # Print additional tags if provided
            if tags:
                for tag in tags:
                    try:
                        value = ds[tag].value
                        print(f"Tag {ds[tag]}: {value}")
                    except KeyError:
                        self.logger.warning(f"Tag {tag} not found in DICOM file")

            # Extract and save image if requested
            if extract_image:
                try:
                    middle_slice = ds.pixel_array.shape[0] // 2
                    plt.imshow(ds.pixel_array[middle_slice], cmap=plt.cm.bone)
                    plt.axis('off')
                    output_path = os.path.join(self.path, f"{os.path.splitext(filename)[0]}.png")
                    plt.title(f"Patient: {ds.PatientName}, Study Date: {ds.StudyDate}")
                    plt.imsave(output_path, ds.pixel_array[middle_slice], cmap=plt.cm.bone)
                    #plt.savefig(output_path)
                    plt.close()
                    print(f"Extracted image saved to {output_path}")
                except Exception as e:
                    self.logger.error("Could not extract image from DICOM file")
                    self.logger.error(str(e), exc_info=True)

        except FileNotFoundError as er:
            self.logger.error(f"DICOM file {filename} not found")
            self.logger.error(str(er))
            return None
        except InvalidDicomError as iner:
            self.logger.error(f"Invalid DICOM format in file {filename}")
            self.logger.error(str(iner))
            return None
        except Exception as e:
            self.logger.error(f"Error processing DICOM file {filename}: {str(e)}")
            return None
        
        
    
    
    def read_file(self, filename):
        if not self.__file_exists__(filename):
            return None
        
        if self.__is_csv__(filename):
            return self.read_csv(filename)
        
        if self.__is_dicom__(filename):
            return self.read_dicom(filename)
        
        try:
            with open(os.path.join(self.path, filename), 'r') as file:
                return file.read()
        except FileNotFoundError:
            self.logger.exception(f"File {filename} not found.")
            
            
if __name__ == '__main__':
    processor = FileProcessor('C:\\Users\\JUAN\\Desktop\\imexhs\\developer_test_py_ang\\')
    processor.list_folder_content('C:\\Users\\JUAN\\Desktop\\Prueba modelos\\data\\', details=True)
    processor.read_csv(filename='C:\\Users\\JUAN\\Desktop\\imexhs\\developer_test_py_ang\\sample-02-csv.csv', report_path='C:\\Users\\JUAN\\Desktop\\imexhs', summary=True)
    processor.read_dicom(filename="C:\\Users\\JUAN\Desktop\\imexhs\\developer_test_py_ang\\sample-02-dicom.dcm", tags=[(0x0010, 0x0010), (0x0008, 0x0060)], extract_image=True) 