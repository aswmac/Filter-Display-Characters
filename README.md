When running on the command line like the following:

nohup ollama run qwen2.5-coder:32b --verbose "$1" | tee -a "$lf" 2>&1 &

which is run with variables $1 and $lf defined through use by the bash function:

<pre>
q0() {
  if [ -z "$1" ]; then
    echo "Usage: q0 <input>"
    return 1
  fi
  dt=$(date +"%Y-%m-%d*%H%M%S")
  lf="LLM_qwen2.5_coder_32b.log"
  echo "" >> "$lf"
  echo "$dt" >> "$lf"
  echo "" >> "$lf"
  echo "<input>\n$1\n</input>" >> "$lf"
  nohup ollama run qwen2.5-coder:32b --verbose "$1" | tee -a "$lf" 2>&1 &
}

</pre>

where lf="LLM_qwen2.5-coder_32b_macM2.log" is the log filename.
$1 is the string quoted prompt input for the LLM. The resulting log file 
has many "invisible" characters that do not show up on cat, but if do 
nano they make the file unreadable. They look like ^[[?25l and ^[[?25h 
among others.

$: ./python.py > out.txt

comment out the line `print(f"{counter:<10}{hex_code:<15}{char}")` since
it is just a debug line to check the logic paths of the various characters 
as found empirically
