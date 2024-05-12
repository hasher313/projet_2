import os
import sys
from encoding import Encoder, Decoder
import matplotlib.pyplot as plt
from datetime import datetime


def decompressor(file_path):
    # os.system(f"python3 toulbmp.py --force {file_path} convertedToulbmp.ulbmp")
    file_size = os.path.getsize(file_path)
    time_before = datetime.now()
    image = Decoder.load_from(file_path)
    time_after = datetime.now()

    elapsed_time = time_after - time_before
    
    return elapsed_time.total_seconds(), file_size, image

def compressor(image, file_path, version, depth: int = 1, rle: int = 1):
    time_before = datetime.now()
    encoder = Encoder(image, version, depth=depth, rle=bool(rle))
    time_after = datetime.now()
    if version == 3 and rle == 1:
        file_path = f"{file_path}_{version}_rle-1_encoded.ulbmp"
    elif version == 3 and rle == 0:
        file_path = f"{file_path}_{version}_rle-0_encoded.ulbmp"
    else:
        file_path = f"{file_path}_{version}_encoded.ulbmp"
    encoder.save_to(file_path)
    file_size = os.path.getsize(file_path)

    elapsed_time = time_after - time_before
    return elapsed_time.total_seconds(), file_size

def calculating(file_path, depth: int = 24):
    versions = []
    compr_execution_times = []
    decompr_execution_times = []
    file_sizes = []
    compression_rates = []
    if "checkers1.ulbmp" in file_path:
        depth = 1
    elif "lines1.ulbmp" in file_path:
        depth = 1
    elif "squares1.ulbmp" in file_path:
        depth = 1
    elif "external_n-b" in file_path:
        depth = 1 
    for i in range(1, 5):
        version = i
        print(f"Version {i}")
        decom_time, size_before, image = decompressor(file_path) 
        if i == 3:
            versions.append(f"Version {i}-rle1")
            comp_time, size_after = compressor(image, file_path, version, depth, 1)
            compr_execution_times.append(comp_time)
            decompr_execution_times.append(decom_time)
            compression_rates.append((size_before - size_after) / size_before*100)

            versions.append(f"Version {i}-rle0")
            comp_time, size_after = compressor(image, file_path, version, depth, 0)
            compr_execution_times.append(comp_time)
            decompr_execution_times.append(decom_time)
            compression_rates.append((size_before - size_after) / size_before*100)
        else:
            versions.append(f"Version {i}")
            comp_time, size_after = compressor(image, file_path, version, 0, 0)
            compr_execution_times.append(comp_time)
            decompr_execution_times.append(decom_time)
            compression_rates.append((size_before - size_after) / size_before*100)

    return versions, compr_execution_times, decompr_execution_times, file_sizes, compression_rates

def createGraph(filenames, data_dict):
    plt.figure(figsize=(10, 5))
    for filename in filenames:
        data = data_dict[filename]
        versions = data['versions']
        compr_execution_times = [time for time in data['compr_execution_times']]
        plt.plot(versions, compr_execution_times, marker='o', label=f'{filename}')
        # plt.legend(loc='upper left', fontsize='x-small', frameon=False)
    plt.xlabel('Versions')
    plt.ylabel('Time (seconds)')
    plt.title('Compression Execution Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 5))
    for filename in filenames:
        data = data_dict[filename]
        versions = data['versions']
        decompr_execution_times = [time for time in data['decompr_execution_times']]
        plt.plot(versions, decompr_execution_times, marker='o', label=f'{filename}')
        # plt.legend(loc='upper left', fontsize='x-small', frameon=False)
    plt.xlabel('Versions')
    plt.ylabel('Time (seconds)')
    plt.title('Decompression Execution Time Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 5))
    for filename in filenames:
        data = data_dict[filename]
        versions = data['versions']
        compression_rates = data['compression_rates']
        plt.plot(versions, compression_rates, marker='o', label=f'{filename}')
        # plt.legend(loc='upper left', fontsize='x-small', frameon=False)
    plt.xlabel('Versions')
    plt.ylabel('Compression Rate (%)')
    plt.title('Compression Rate Comparison')
    plt.legend()
    plt.grid(True)
    plt.show()
def main():
    directory = sys.argv[1]
    data_dict = {}
    filenames = []
    for filename in os.listdir(directory):
        filenames.append(filename)
        if filename.endswith(".ulbmp"):
            file_path = os.path.join(directory, filename)
            versions, compr_execution_times,decompr_execution_times, file_sizes, compression_rates = calculating(file_path=file_path, depth=int(sys.argv[2]))
            data_dict[filename] = {
                'versions': versions,
                'compr_execution_times': compr_execution_times,
                'decompr_execution_times': decompr_execution_times,
                'file_sizes': file_sizes,
                'compression_rates': compression_rates
            }
    createGraph(filenames=filenames, data_dict=data_dict)
    os.system("rm -rf *_encoded.ulbmp")

if __name__ == "__main__":
    main()
