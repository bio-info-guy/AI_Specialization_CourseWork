import sys
import os
import numpy as np


num_obj = int(sys.argv[1])
size_constraint = int(sys.argv[2])
weight_constraint = int(sys.argv[3])

weights = np.random.random(size = num_obj)*round(weight_constraint/(np.sqrt(num_obj)), 4)+0.0001
sizes = np.random.random(size = num_obj)*round(size_constraint/(np.sqrt(num_obj)), 4)+0.0001
values = np.random.randint(1, 1000, size = num_obj)



lp_writer = open('MKS_MLP.lp', 'w')
csv_writer = open('MKS_problem.csv', 'w')
csv_writer.write('{:.0f} {:.0f} {:.0f}\n'.format(num_obj, size_constraint,weight_constraint))
for i, (w,s) in enumerate(zip(weights, sizes)):
    csv_writer.write('{:.0f} {:.4f} {:.4f} {:.0f}\n'.format(i,s,w,values[i]))
csv_writer.close()

lp_writer.write('Maximize total_value\nSubject To\n')
for i, w in enumerate(weights):
    lp_writer.write('+ {:.4f} x{:.4f} '.format(w,i))
lp_writer.write('<= '+str(weight_constraint)+'\n')

for i, s in enumerate(sizes):
    lp_writer.write('+ {:.4f} x{:.4f} '.format(s,i))
lp_writer.write('<= '+str(size_constraint)+'\n')

lp_writer.write('total_value ')
for i, v in enumerate(values):
    lp_writer.write('- {:.0f} x{:.0f} '.format(v,i))
lp_writer.write('= 0\nBinary\n')

for i in range(len(values)):
    lp_writer.write('x{:.0f}\n'.format(i))

lp_writer.write('End')
lp_writer.close()
