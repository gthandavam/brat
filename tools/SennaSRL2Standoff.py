__author__ = 'gt'

import commands

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

def get_standoff_lines(srl_args_per_sentence):
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

  for sent_srl_arg in srl_args_per_sentence:
    no_of_tokens = len(sent_srl_arg[0])
    for i in xrange(3, len(sent_srl_arg)):

      for j in xrange(0, no_of_tokens):
        print sent_srl_arg[i][j]


  return []

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
    standoff_lines = get_standoff_lines(srl_args_per_sentence)

    #write the standoff output
    # ann_out = codecs.open(file+'.standout','w', encoding)
    #
    # for standoff_line in standoff_lines:
    #   ann_out.write(standoff_line)
    #
    # ann_out.close()
    f.close()

if __name__ == '__main__':
  from sys import argv
  exit(main(argv))