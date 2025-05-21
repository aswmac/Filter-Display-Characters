When running on the command line like the following:

nohup ollama run qwen2.5-coder:32b --verbose "$1" | tee -a "$lf" 2>&1 &

where example lf="LLM_qwen2.5-coder_32b_macM2.log" could be the filename.
$1 is the string quoted prompt input for the LLM. The resulting log file 
has many "invisible" characters that do not show up on cat, but if do 
nano they make the file unreadable. They look like ^[[?25l and ^[[?25h 
among others.

$: ./python.py > out.txt

if the output has something like CONTROL_16, it needs more refinement
