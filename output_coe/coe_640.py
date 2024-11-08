import os
import zlib
import struct

def compress_file(file_path):
    """Read and compress the contents of a file, including original length for padding removal."""
    with open(file_path, 'rb') as file:
        data = file.read()
        original_length = len(data)
        print("Original length:", original_length)
        compressed_data = zlib.compress(data)
        print("Compressed length:", len(compressed_data))
        # Prepend the original length to compressed data for padding reference
        length_prefix = struct.pack('>I', original_length)  # 4 bytes to store length
        return length_prefix + compressed_data

def chunk_data(data, chunk_size=80):
    """Divide the data into chunks of specified size, padding the last chunk if necessary."""
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    if len(chunks[-1]) < chunk_size:
        chunks[-1] = chunks[-1].ljust(chunk_size, b'\x00')  # Pad the last chunk
    return chunks

def create_coe_file(file_index, chunk_data, output_directory):
    """Generate a COE file with 640-bit width entries in the specified output directory."""
    os.makedirs(output_directory, exist_ok=True)  # Ensure the output directory exists
    coe_file_path = os.path.join(output_directory, f'output_{file_index}.coe')
    
    with open(coe_file_path, 'w') as coe_file:
        coe_file.write('memory_initialization_radix=16;\n')
        coe_file.write('memory_initialization_vector=\n')
        
        for i, chunk in enumerate(chunk_data):
            line = ''.join(f'{byte:02X}' for byte in chunk)
            if i < len(chunk_data) - 1:
                coe_file.write(line + ',\n')
            else:
                coe_file.write(line + ';\n')  # Last line without a comma

def main(file_path, output_directory='./output_coe_files'):
    compressed_data = compress_file(file_path)
    chunks = chunk_data(compressed_data)
    num_coe_files = 1  # Number of COE files to create
    coe_chunks = [[] for _ in range(num_coe_files)]

    for i, chunk in enumerate(chunks):
        coe_chunks[i % num_coe_files].append(chunk)

    for i in range(num_coe_files):
        create_coe_file(i, coe_chunks[i], output_directory)

if __name__ == "__main__":
    input_file_path = './input_output_txt/input.jpg'  # Change to your input file path
    output_dir = './output_coe/'  # Set your desired output directory path
    main(input_file_path, output_dir)
