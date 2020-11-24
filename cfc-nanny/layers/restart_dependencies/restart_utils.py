import re
def clean_output(out):
    lines = out.split("\n")
    cleaned_lines = []

    for line in lines:
        line = line.split("\r").pop()
        line = re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", line) # remove ANSI formatting codes
        line = re.sub(r"/var/[^\s]*", "****", line)
        cleaned_lines.append( line )

    return "\n".join(cleaned_lines)
