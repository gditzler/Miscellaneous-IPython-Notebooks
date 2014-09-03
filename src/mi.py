#!/usr/bin/env python 
import numpy as np
import ctypes as c
import itertools
from multiprocessing import Pool

gdata = None
glabels = None 

__author__ = "Gregory Ditzler"
__copyright__ = "Copyright 2014, EESI Laboratory (Drexel University)"
__credits__ = ["Gregory Ditzler"]
__license__ = "GPL"
__version__ = "0.1.0"
__maintainer__ = "Gregory Ditzler"
__email__ = "gregory.ditzler@gmail.com"

try:
  libMIToolbox = c.CDLL("libMIToolbox.so"); 
except:
  raise Exception("Error: could not load libMIToolbox.so")


def calc_mi(data, labels):
  """
  Calculate the Mutual Information 
  @data
  @labels

  @mutual_information
  """
  data, labels = __check_data__(data, labels)
  n_observations, n_features = data.shape
  c_n_observations = c.c_int(n_observations)
  output = []

  for c_data in data.transpose():
    libMIToolbox.calculateMutualInformation.restype = c.c_double 
    result = libMIToolbox.calculateMutualInformation(
        c_data.ctypes.data_as(c.POINTER(c.c_double)),
        labels.ctypes.data_as(c.POINTER(c.c_double)),
        c_n_observations)
    output.append(result.real)
  return np.array(output)



def p_calc_mi(d_in):
  """
  Calculate the Mutual Information 
  @data
  @labels

  @mutual_information
  """
  data, i, j = d_in 
  f0 = data[:,i]
  f1 = data[:,j]
  c_n_observations = c.c_int(len(f0))

  libMIToolbox.calculateMutualInformation.restype = c.c_double 
  result = libMIToolbox.calculateMutualInformation(
      f0.ctypes.data_as(c.POINTER(c.c_double)),
      f1.ctypes.data_as(c.POINTER(c.c_double)),
      c_n_observations)
  return (i,j,result.real)



def p_calc_cmi(d_in):
  """
  """
  data,labels,i,j = d_in
  c_n_observations = c.c_int(len(data))
  libMIToolbox.calculateMutualInformation.restype = c.c_double
  result = libMIToolbox.calculateConditionalMutualInformation(
      data[:,i].ctypes.data_as(c.POINTER(c.c_double)),
      data[:,j].ctypes.data_as(c.POINTER(c.c_double)),
      labels.ctypes.data_as(c.POINTER(c.c_double)),
      c_n_observations)
  return (i,j,result.real)
  #return (i,j,glabels)

def calc_cmi(X, Y, Z):
  """
  Calculate Mutual Information: I(X;Y|Z) = H(X|Z) - H(X|YZ)
  @X
  @Y
  @Z

  @CMI
  """
  c_n_observations = c.c_int(len(X))
  libMIToolbox.calculateMutualInformation.restype = c.c_double
  result = libMIToolbox.calculateConditionalMutualInformation(
        X.ctypes.data_as(c.POINTER(c.c_double)),
        Y.ctypes.data_as(c.POINTER(c.c_double)),
        Z.ctypes.data_as(c.POINTER(c.c_double)),
        c_n_observations)
  return result.real

def calc_mi_features(feat0, feat1):
  """
  Calculate the Mutual Information 
  """
  c_n_observations = c.c_int(len(feat0))

  libMIToolbox.calculateMutualInformation.restype = c.c_double 
  result = libMIToolbox.calculateMutualInformation(
      feat0.ctypes.data_as(c.POINTER(c.c_double)),
      feat1.ctypes.data_as(c.POINTER(c.c_double)),
      c_n_observations)
  return result.real


def mi_matrix(data, par=False, cpus=2):
  n_features = len(data[0])
  mi_mat = np.zeros((n_features,n_features))
  for i,j in itertools.combinations_with_replacement(range(n_features),2):
    val = calc_mi_features(data[:,i], data[:,j])
    mi_mat[i,j] = val
    mi_mat[j,i] = val
  
  if par == False:
    for i,j in itertools.combinations_with_replacement(range(n_features),2):
      val = calc_mi_features(data[:,i], data[:,j])
      mi_mat[i,j], mi_mat[j,i] = val, val
  else:
    p = Pool(cpus)
    global gdata
    gdata = data
    
    res = p.map(p_calc_mi, 
        [(data,i,j) for i,j in itertools.combinations_with_replacement(range(n_features),2)])
    for r in res:
      i,j,val = r
      mi_mat[i,j], mi_mat[j,i] = val, val
  return mi_mat

def cmi_matrix(data, labels, par=False, cpus=2):
  n_features = len(data[0])
  cmi_mat = np.zeros((n_features,n_features))

  if par == False:
    for i,j in itertools.combinations_with_replacement(range(n_features),2):
      val = calc_cmi(data[:,i], data[:,j], labels)
      cmi_mat[i,j], cmi_mat[j,i] = val, val
  else:
    p = Pool(cpus)
    global gdata
    global glabels
    gdata = data
    glabels = labels
    
    res = p.map(p_calc_cmi, 
        [(data,labels,i,j) for i,j in itertools.combinations_with_replacement(range(n_features),2)])
    for r in res:
      i,j,val = r
      cmi_mat[i,j], cmi_mat[j,i] = val, val
  return cmi_mat

def q():
  print gdata 

def mim(data, labels, n_select):
  """
  Mutual Information Maximization (MIM)
  @data
  @labels
  @n_select

  @selected_indices
  """
  return np.argsort(calc_mi(data, labels))[:n_select] 

def __check_data__(data, labels):
  """
    Check dimensions of the data and the labels.  Raise and exception
    if there is a problem.

    Data and Labels are automatically cast as doubles before calling the 
    feature selection functions

    @param data: the data 
    @param labels: the labels
    @return (data, labels): ndarray of floats
    @rtype: tuple
  """
  if isinstance(data, np.ndarray) is False:
    raise Exception("data must be an numpy ndarray.")
  if isinstance(labels, np.ndarray) is False:
    raise Exception("labels must be an numpy ndarray.")
  if len(data) != len(labels):
    raise Exception("data and labels must be the same length")
  return 1.0*data, 1.0*labels

