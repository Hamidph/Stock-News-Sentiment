import pandas as pd

# Load the Excel file
input_file = 'Ydata.xlsx'  # Replace with your input file name
df = pd.read_excel(input_file)

# Calculate the number of rows per chunk
n = len(df) // 5

# Function to save each chunk to a new Excel file
def save_chunk_to_excel(chunk, index):
    output_file = f'output_file_part_{index+1}.xlsx'
    chunk.to_excel(output_file, index=False)
    print(f'Saved: {output_file}')

# Split the DataFrame into 5 smaller chunks and save them
for i in range(5):
    if i < 4:
        chunk = df.iloc[i*n:(i+1)*n]
    else:
        chunk = df.iloc[i*n:]  # The last chunk takes all remaining rows
    save_chunk_to_excel(chunk, i)
