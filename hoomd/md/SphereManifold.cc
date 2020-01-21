// Copyright (c) 2009-2020 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.


// Maintainer: pschoenhoefer

#include "SphereManifold.h"

namespace py = pybind11;

using namespace std;

/*! \file SphereManifold.cc
    \brief Contains code for the SphereManifold class
*/

/*!
    \param P position of the sphere
    \param r radius of the sphere
*/
SphereManifold::SphereManifold(std::shared_ptr<SystemDefinition> sysdef,
                               std::shared_ptr<ParticleGroup> group,
                               Scalar r,
                               Scalar3 P)
  : Manifold(sysdef, group), m_r(r), m_P(P) 
       {
    m_exec_conf->msg->notice(5) << "Constructing SphereManifold" << endl;
       }

SphereManifold::~SphereManifold() 
       {
    m_exec_conf->msg->notice(5) << "Destroying SphereManifold" << endl;
       }

        //! Return the value of the implicit surface function of the sphere.
        /*! \param point The position to evaluate the function.
        */
Scalar SphereManifold::implicit_function(Scalar3 point)
       {
       Scalar3 delta = point - m_P;
       return dot(delta, delta) - m_r*m_r;
       }

       //! Return the gradient of the constraint.
       /*! \param point The location to evaluate the gradient.
       */
Scalar3 SphereManifold::derivative(Scalar3 point)
       {
       return point - m_P;
       }

//! Exports the SphereManifold class to python
void export_SphereManifold(pybind11::module& m)
    {
    py::class_< SphereManifold, std::shared_ptr<SphereManifold> >(m, "SphereManifold", py::base<Manifold>())
    .def(py::init< std::shared_ptr<SystemDefinition>,std::shared_ptr<ParticleGroup>,Scalar, Scalar3 >())
    .def("implicit_function", &SphereManifold::implicit_function)
    .def("derivative", &SphereManifold::derivative)
    ;
    }
