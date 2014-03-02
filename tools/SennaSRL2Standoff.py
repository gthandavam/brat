__author__ = 'gt'

import commands

if __name__ =='__main__':
  files = commands.getoutput('find /home/gt/Downloads/senna/coref-recipes -type f ')

  for file in files.rstrip().split('\n'):
    print "parsing annotation from " + file
    sentCnt = 0
    f = open(file)
    lines = f.readlines()

    a0 = []
    a1 = []
    a2 = []
    a3 = []
    a4 = []
    a5 = []
    pred = []

    for line in lines:
      if len(line.strip()) == 0:

        sentCnt += 1

        if(len(pred) > 0 ):
          print "Annotations for sentnumber: " + str(sentCnt)
          for i in range(0, len(a0)):
            if len(pred[i].strip()) == 0:
              continue
            print "pred: " + pred[i]
            print "a0: " + a0[i]
            print "a1: " + a1[i]
            print "a2: " + a2[i]
            print "a3: " + a3[i]
            print "a4: " + a4[i]
            print "a5: " + a5[i]

        a0 = []
        a1 = []
        a2 = []
        a3 = []
        a4 = []
        a5 = []
        pred = []
        continue

      columns = line.split('\t')
      if(len(a0) == 0):
        for i in xrange(0, len(columns) - 2):
          a0.append('')
          a1.append('')
          a2.append('')
          a3.append('')
          a4.append('')
          a5.append('')
          pred.append('')
        pass

      for i in xrange(2, len(columns)):
        column = columns[i].strip()
        if column.endswith('-A0'):
          a0[i-2] += columns[0].strip() + ' '
        elif column.endswith('-A1'):
          a1[i - 2] += columns[0].strip() + ' '
        elif column.endswith('-A2'):
          a2[i - 2] += columns[0].strip() + ' '
        elif column.endswith('-A3'):
          a3[i - 2] += columns[0].strip() + ' '
        elif column.endswith('-A4'):
          a4[i - 2] += columns[0].strip() + ' '
        elif column.endswith('-A5'):
          a5[i - 2] += columns[0].strip() + ' '
        elif column.endswith('-V'):
          pred[i - 2] += columns[0].strip() + ' '
