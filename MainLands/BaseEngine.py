__author__ = 'claudio'

import glob, os, sys
from pathlib import Path
from Objects import NodeInfo
from Objects import NodeInfoOut


class TransformEngine:

    def __init__(self, destination, source, input_folder, work_folder, out_folder, end_folder):
        self.__destination_node__ = destination
        self.__source_node__ = source
        self.__input_folder__ = input_folder
        self.__work_folder__ = work_folder
        self.__out_folder__ = out_folder
        self.__end_folder__ = end_folder
        self.__main_folder__ = Path(self.__destination_node__).parent
        self.__sourceInfo_dict__ = {}

    def run(self):
        self.__build_sourceInfo__()
        self.__go_through_files_from_folder__()

    def __parse_dest_and_sour_file(self, file_name):
        """
        This function opens destination and source node file in order to fill node information dictionary
        """
        file_reader = open(file_name, "r")
        # temp_path = str.format("{0}/{1}", self.__main_folder__, "exitFile.txt")
        # file_writer = open(temp_path, "w+")
        for line in file_reader:
            #file_writer.write(line)
            elms = str.split(line, ",")
            if len(elms) < 9:
                continue
            node = NodeInfo(elms)
            node_name = node.get_source_name()
            if not(node_name in self.__sourceInfo_dict__.keys()):
                self.__sourceInfo_dict__[node_name] = node
        file_reader.close()

    def __build_sourceInfo__(self):
        """
        This function builds dictionary that will be used to get lat/long node information
        """
        # Reading destination file
        self.__parse_dest_and_sour_file(self.__destination_node__)

        # Now, Reading source nodes file
        self.__parse_dest_and_sour_file(self.__source_node__)

    def __go_through_files_from_folder__(self):
        """
        This function process each file inside main folder, it put each file on working folder while processing.
        When It ends, The processed file will be moved to worked file and a csv will be generated.
        """

        os.chdir(str(self.__input_folder__))
        file_list = glob.glob("*.txt")
        if len(file_list) == 0:
            print(str.format("Has no files on --> {0}", self.__input_folder__))

        final_file_name = str.format("{0}/{1}", self.__main_folder__,"final_file.csv")
        csv_file_name = final_file_name #os.path.join(self.__main_folder__, final_file_name)
        csv_final_file = open(csv_file_name, "w+")

        header = "lat_monitor,long_monitor,monitor_name,lat_monitorado,long_monitorado,monitorado_name,date_hour,value"
        csv_final_file.write(header + "\n")

        for file in file_list:
            self.__process_file__(file, csv_final_file)
        csv_final_file.close()

    def __process_file__(self, file, file_writer):
        #os.path.join combine paths
        full_file_path = os.path.join(self.__input_folder__, file)
        new_full_file_path = os.path.join(self.__work_folder__, file)
        #os.rename move file from folder to another
        os.rename(full_file_path, new_full_file_path)

        formatted_date = self.__get_date_from_file__(file)

        try:
            metrics_file = open(new_full_file_path, "r+")
            for line in metrics_file:
                elms = line.split(" ")
                metrics_info = elms[2:len(elms) - 2]
                monitor, monitorado = elms[:2]
                if monitor in self.__sourceInfo_dict__.keys() \
                   and monitorado in self.__sourceInfo_dict__.keys():
                    monitor_info = self.__sourceInfo_dict__.get(monitor)
                    monitorado_info = self.__sourceInfo_dict__.get(monitorado)
                    """
                    TODO: create each output object and write them on CSV file
                    """
                    for i, value in enumerate(metrics_info):

                        if value == ".":
                            value = "0"
                        date_hour = str.format("{0} {1}:00", formatted_date, i)
                        lat_monitor, long_monitor = monitor_info.get_lat_long()

                        lat_monitorado, long_monitorado = monitorado_info.get_lat_long()

                        out_object = NodeInfoOut(lat_monitor, long_monitor,
                                                 monitor, lat_monitorado, long_monitorado,
                                                 monitorado, date_hour, value)
                        line = out_object.print_info()
                        file_writer.write(line + "\n")
                # print(str.format("Monitor:{0}\nMonitorado:{1}", monitor, monitorado))
                # print(metrics_info)
                # print(line)
        except Exception:
            print("Deu Ruim")
            # So Lazy, has to be removed
            os.rename(new_full_file_path, full_file_path)
            sys.exit(2)

        # So Lazy, has to be removed
        os.rename(new_full_file_path, full_file_path)

    def __get_date_from_file__(self, file):
        file_name = file
        file_name = file_name.replace(".txt", "")
        elms = file_name.split("-")
        year, month, day = elms[len(elms) - 3:len(elms)]
        formatted_date = str.format("{0}-{1}-{2}", year, month, day)
        # print(formatted_date)
        return formatted_date