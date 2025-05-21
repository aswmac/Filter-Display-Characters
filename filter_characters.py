#!/usr/bin/env python3

import sys

class HBUF:
  '''
  Trying to filter out invisible characters from my LLM_log file which is run like:
  nohup ollama run qwen2.5-coder:32b --verbose "$1" | tee -a "$lf" 2>&1 &
  where lf="LLM_qwen2.5-coder_32b_macM2.log"
  0 -- 1b
  1 -- 5b
  2 -- 3f
  3 -- 32
  4 -- 35 then to 5 or 6
  5 -- 68 or 6c then END
  5 -- 30 then continue to 6
  6 -- 32
  7 -- 36
  8 -- 68 or 6c then END
  '''
  def __init__(self):
    self.count = 0
  def __call__(self, char):
    ''' if char is part of one of the sequences, deal with it,
    else just pass it throuhg '''
    if self.count == 0:
      if char == "1b":
        self.count = 1
        return self.count
    if self.count == 1:
      if char == "5b":
        self.count = 2
        return self.count
    if self.count == 2:
      if char == "3f":
        self.count = 3
        return self.count
      if char == "32":
        self.count = 17
        return self.count
      if char == "31":
        self.count = 9
        return self.count
      if char == "4b":
        self.count = 11
        return self.count
    if self.count == 3:
      if char == "32":
        self.count += 1
        return self.count
    if self.count == 4:
      if char == "35":
        self.count += 1
        return self.count
      if char == "30":
        self.count = 6
        return self.count
    if self.count == 5:
      if char == "30":
        self.count = 15
        return self.count
      elif char == "68" or char == "6c":
        self.count = 16
        return self.count
    if self.count == 6:
      if char == "32":
        self.count = 7
        return self.count
    if self.count == 7:
      if char == "36":
        self.count = 8
        return self.count
    if self.count == 8:
      if char == "68" or char == "6c":
        self.count = 12
        return self.count
    if self.count == 9:
      if char == "47":
        self.count = 10
        return self.count
    if self.count == 10:
      if char == "1b": # sometimes (right at start of answer I think) it skips the braille character
        self.count = 1
        return self.count
      if char == "2819" or char == "283c" or char == "2807" or char == "280f":
        self.count = 13
        return self.count
      if char == "2839" or char == "2834" or char == "2827" or char == "2826":
        self.count = 14
        return self.count
      if char == "2839" or char == "280b" or char == "2838" or char == "2826":
        self.count = 14
        return self.count
    if self.count == 11:
      self.count = 0 # A K control character FINI
      return self(char)
    if self.count == 12:
      self.count = 0 # A control character FINI
      return self(char)
    if self.count == 13:
      if char == "20": # space after braille is also erased
        self.count = 18
        return self.count 
    if self.count == 14:
      if char == "20": # space after braille is also erased
        self.count = 18
        return self.count
    if self.count == 15:
      self.count = 0 # A control character FINI
      return self(char)  
    if self.count == 16:
      self.count = 0 # A control character FINI
      return self(char)  
    if self.count == 17: # At the start of the answer it does this one
      if char == "4b":
        self.count = 18
        return self.count  
    if self.count == 18:
      self.count = 0 # A control character FINI
      return self(char)
    self.count = 0
    return 0

def read_and_display_characters(file_path):
    filter = HBUF()
    try:
        with open(file_path, 'r', encoding='utf-8') as file, open("out.txt", 'w') as outfile:
            content = file.read()  # Read the first 100 characters from the file

            print(f"{'Counter':<10}{'Hex':<15}{'Display'}")
            print("-" * 35)
            control_counter = 0

            for counter, char in enumerate(content, start=1):
                hex_code = format(ord(char), '02x')
                f = filter(hex_code)
                if f != 0:
                  char = f"CONTROL_{f}"
                else:
                  outfile.write(char)
                print(f"{counter:<10}{hex_code:<15}{char}")

    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Replace 'your_file.txt' with the path to your file
read_and_display_characters('LLM_qwen2.5_coder_32b.log')
