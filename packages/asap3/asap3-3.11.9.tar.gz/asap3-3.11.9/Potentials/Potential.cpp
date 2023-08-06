// -*- C++ -*-
// Potential.cpp: Common functionality for all potentials.
//
// Copyright (C) 2001-2012 Jakob Schiotz and Center for Individual
// Nanoparticle Functionality, Department of Physics, Technical
// University of Denmark.  Email: schiotz@fysik.dtu.dk
//
// This file is part of Asap version 3.
//
// This program is free software: you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// version 3 as published by the Free Software Foundation.  Permission
// to use other versions of the GNU Lesser General Public License may
// granted by Jakob Schiotz or the head of department of the
// Department of Physics, Technical University of Denmark, as
// described in section 14 of the GNU General Public License.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// and the GNU Lesser Public License along with this program.  If not,
// see <http://www.gnu.org/licenses/>.

#include "AsapPython.h"
#include "Asap.h"
#include "Atoms.h"
#include "Potential.h"
#include "Debug.h"

// Standard mapping of the six independent parts of the stress tensor to
// vector notation
const static int stresscomp[3][3] = {{0, 5, 4}, {5, 1, 3}, {4, 3, 2}};

void Potential::RecoverAfterException()
{
  DEBUGPRINT;
  if (atoms != NULL && atoms->IsActive())
    atoms->End();
}


SymTensor Potential::GetVirial(PyObject *a)
{
  DEBUGPRINT;
  SymTensor result;
  for (int i = 0; i < 6; i++)
    result[i] = 0;
  const vector<SymTensor> &virials = GetVirials(a);
  for (int i = 0; i < virials.size(); i++)
    result += virials[i];
  DEBUGPRINT;
  return result;
}


#ifdef ASAP_FOR_KIM
// When building as an OpenKIM model, there is no Python layer to pass through.
void Potential::SetAtoms_ThroughPython(PyObject *pyatoms, Atoms* accessobj /* = NULL */)
{
  SetAtoms(pyatoms, accessobj);
}
#else
// The normal version
void Potential::SetAtoms_ThroughPython(PyObject *pyatoms, Atoms* accessobj /* = NULL */)
{
  DEBUGPRINT;
  // Call self.set_atoms(...) as implemented in Python
  PyObject *py_accessobj;
  if (accessobj == NULL)
    {
      py_accessobj = Py_None;
      Py_INCREF(Py_None);
    }
  else
    {
#if PY_VERSION_HEX < 0x02070000
    py_accessobj = PyCObject_FromVoidPtr(accessobj, NULL);
#else
    py_accessobj = PyCapsule_New(accessobj, "asap3.accessobj", NULL);
#endif    
    }
  if (py_accessobj == NULL)
    throw AsapPythonError();
  PyObject *method = PyAsapString_FromString("set_atoms");
  if (method == NULL)
    throw AsapPythonError();
  PyObject *result = PyObject_CallMethodObjArgs(self, method, pyatoms, py_accessobj, NULL);
  bool error = (result == NULL);
  Py_XDECREF(result);
  Py_DECREF(method);
  Py_DECREF(py_accessobj);
  if (error)
    throw AsapPythonError();
  DEBUGPRINT;
}
#endif
