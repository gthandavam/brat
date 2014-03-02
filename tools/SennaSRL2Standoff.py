__author__ = 'gt'

import commands
import codecs

encoding = 'UTF-8'

def get_sentences(lines):
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

    offset += int(sent_srl_arg[1][-1].split()[1]) + 1

  return ret

def main(args):
  files = commands.getoutput('find /home/gt/Downloads/senna/coref-recipes -type f ')

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
    ann_out = codecs.open(file.replace('coref-recipes','senna-standoff'),'w', encoding)

    symbol_counter = 1
    for standoff_group in standoff_groups:
      for standoff_line in standoff_group:
        ann_out.write('T' +str(symbol_counter) + '\t' + standoff_line + '\n')
        symbol_counter += 1

    ann_out.close()
    f.close()

if __name__ == '__main__':
  from sys import argv
  exit(main(argv))