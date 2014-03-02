__author__ = 'gt'

import commands
import codecs

encoding = 'UTF-8'

'''
senna was run with the following flags

./senna-linux64 -posvbs  -offsettags -srl < input_file > output_file

-posvbs flag was required to handle for eg: add predicate in imperative sentence

'''

def get_sentences(lines):
  '''
  API to segregate the senna output into chunks per sentence
  '''
  ret = []
  ret.append([])
  i=0
  for line in lines:
    if(len(line.strip()) == 0):
      i += 1
      ret.append([])
      continue
    ret[i].extend([line])

  return ret

def get_column_args(arg_lines):
  '''
  API to transform the senna output column into a row

  arg_lines : chunk of lines for one sentence
  '''
  ret = []

  col_count = len(arg_lines[0].strip().split('\t'))

  for col in xrange(0, col_count):
    ret.append([])
    for arg_line in arg_lines:
      ret[-1].extend([arg_line.split('\t')[col].strip()])

  return ret

def generate_standoff(srl_args, idx, offset):
  """
  Assuming a grammar here:
  S-V is a predicate
  *-A0 translates to arg0
  *-A1 translates to arg1
  *-A2 translates to arg2
  Parse the IOBES format
  """
  ret = []
  tokens = len(srl_args[idx])
  for i in xrange(0, tokens):
    if(srl_args[idx][i].endswith('S-V')):
      #predicate + ' ' + span markers + text
      span_markers = srl_args[1][i].split()
      span_markers[0] = int(span_markers[0]) + offset
      span_markers[1] = int(span_markers[1]) + offset
      ret.append('predicate ' + str(span_markers[0]) + ' ' + str(span_markers[1]) + '\t' + srl_args[0][i])
    elif(srl_args[idx][i].endswith('-A0')):
      if(srl_args[idx][i] == 'S-A0'):
        span_markers = srl_args[1][i].split()
        span_markers[0] = int(span_markers[0]) + offset
        span_markers[1] = int(span_markers[1]) + offset
        ret.append('arg0 ' + str(span_markers[0]) + ' ' + str(span_markers[1]) + '\t' + srl_args[0][i])
      elif(srl_args[idx][i] == 'E-A0'):
        ret.append('arg0 ' + str(span) + ' ' + str(int(srl_args[1][i].split()[1]) + offset )+ '\t' + text +' ' + srl_args[0][i])
        text = ""
        span = ""
      elif(srl_args[idx][i] == 'B-A0'):
        span = int(srl_args[1][i].split()[0]) + offset
        text = srl_args[0][i]
      elif(srl_args[idx][i] == 'I-A0'):
        text += ' ' + srl_args[0][i]

    elif(srl_args[idx][i].endswith('-A1')):
      if(srl_args[idx][i] == 'S-A1'):
        span_markers = srl_args[1][i].split()
        span_markers[0] = int(span_markers[0]) + offset
        span_markers[1] = int(span_markers[1]) + offset
        ret.append('arg1 ' + str(span_markers[0]) + ' ' + str(span_markers[1]) + '\t' + srl_args[0][i])
      elif(srl_args[idx][i] == 'E-A1'):
        ret.append('arg1 ' + str(span) + ' ' + str(int(srl_args[1][i].split()[1]) + offset )+ '\t' + text +' ' + srl_args[0][i])
        text = ""
        span = ""
      elif(srl_args[idx][i] == 'B-A1'):
        span = int(srl_args[1][i].split()[0]) + offset
        text = srl_args[0][i]
      elif(srl_args[idx][i] == 'I-A1'):
        text += ' ' + srl_args[0][i]

    elif(srl_args[idx][i].endswith('-A2')):
      if(srl_args[idx][i] == 'S-A2'):
        span_markers = srl_args[1][i].split()
        span_markers[0] = int(span_markers[0]) + offset
        span_markers[1] = int(span_markers[1]) + offset
        ret.append('arg2 ' + str(span_markers[0]) + ' ' + str(span_markers[1]) + '\t' + srl_args[0][i])
      elif(srl_args[idx][i] == 'E-A2'):
        ret.append('arg2 ' + str(span) + ' ' + str(int(srl_args[1][i].split()[1]) + offset )+ '\t' + text +' ' + srl_args[0][i])
        text = ""
        span = ""
      elif(srl_args[idx][i] == 'B-A2'):
        span = int(srl_args[1][i].split()[0]) + offset
        text = srl_args[0][i]
      elif(srl_args[idx][i] == 'I-A2'):
        text += ' ' + srl_args[0][i]

  return ret

def get_standoff_groups(srl_args_per_sentence):
  '''
   srl_args_per_sentence - columns in senna output
   are converted into rows for further processing
   Col1  - Words
   Col2  - Word spans
   Col3  - chosen verb
   .     - argument structure per verb starts from this column
   .
   Coln
  '''
  ret = []

  offset = 0
  for sent_srl_arg in srl_args_per_sentence:
    no_of_tokens = len(sent_srl_arg[0])
    #per sentence processing:

    for i in xrange(3, len(sent_srl_arg)):
      ret.append(generate_standoff(sent_srl_arg, i, offset))

    # +1 to account for newline char
    offset += int(sent_srl_arg[1][-1].split()[1]) + 1

  return ret

def main(args):
  files = commands.getoutput('find <input_dir_containing_senna_output> -type f ')

  for file in files.rstrip().split('\n'):
    print "parsing annotation from " + file
    sentCnt = 0
    f = open(file)
    lines = f.readlines()

    sentences = get_sentences(lines)

    srl_args_per_sentence = []
    #convert senna output columns to rows for each s entence
    for sentence in sentences:
      if(len(sentence) != 0):
        srl_args_per_sentence.append(get_column_args(sentence))

    #standoff_lines for the document
    standoff_groups = get_standoff_groups(srl_args_per_sentence)

    # write the standoff output
    #input is in xxxxx dir, write the output to yyyy dir by changing the dirname in the path
    ann_out = codecs.open(file.replace('xxxxx','yyyy'),'w', encoding)

    symbol_counter = 1
    relation_counter = 1
    for standoff_group in standoff_groups:
      relation_line = ['', '', '', '']
      for standoff_line in standoff_group:
        ann_out.write('T' +str(symbol_counter) + '\t' + standoff_line + '\n')
        if(standoff_line.startswith('predicate')):
          relation_line[0] = 'T' + str(symbol_counter)
        elif standoff_line.startswith('arg0'):
          relation_line[1] = 'T' + str(symbol_counter)
          pass
        elif standoff_line.startswith('arg1'):
          relation_line[2] = 'T' + str(symbol_counter)
          pass
        elif standoff_line.startswith('arg2'):
          relation_line[3] = 'T' + str(symbol_counter)
          pass
        symbol_counter += 1

      #writing out relation line
      if(len(relation_line[0]) != 0):

        if(len(relation_line[1])!=0):
          ann_out.write('R' + str(relation_counter) + '\tParg0 Arg1:' + relation_line[0] +' Arg2:'+relation_line[1]+'\n')
          relation_counter += 1
        if len(relation_line[2]) != 0:
          ann_out.write('R' + str(relation_counter) + '\tParg1 Arg1:' + relation_line[0] +' Arg2:'+relation_line[2]+'\n')
          relation_counter += 1
        if len(relation_line[3]) != 0:
          ann_out.write('R' + str(relation_counter) + '\tParg2 Arg1:' + relation_line[0] +' Arg2:'+relation_line[3]+'\n')
          relation_counter += 1


    ann_out.close()
    f.close()

if __name__ == '__main__':
  from sys import argv
  exit(main(argv))