// Copyright (c) 2009-2016 The Regents of the University of Michigan
// This file is part of the HOOMD-blue project, released under the BSD 3-Clause License.


// Maintainer: jglaser

#ifndef __COMMUNICATOR_GRID_H__
#define __COMMUNICATOR_GRID_H__

#include "hoomd/GPUArray.h"
#include "hoomd/SystemDefinition.h"
#include <memory>

#ifdef ENABLE_MPI

/*! Class to communicate the boundary layer of a regular grid
 */
template<typename T>
class CommunicatorGrid
    {
    public:
        //! Constructor
        CommunicatorGrid(std::shared_ptr<SystemDefinition> sysdef, uint3 dim,
            uint3 embed, uint3 offset, bool add_outer_layer_to_inner);

        //! Communicate grid
        virtual void communicate(const GPUArray<T>& grid);

    protected:
        std::shared_ptr<SystemDefinition> m_sysdef;        //!< System definition
        std::shared_ptr<ParticleData> m_pdata;             //!< Particle data
        std::shared_ptr<const ExecutionConfiguration> m_exec_conf; //!< Execution configuration
        std::shared_ptr<Profiler> m_prof;                  //!< Profiler

        uint3 m_dim;                                         //!< Dimensions of grid
        uint3 m_embed;                                       //!< Embedding dimensions
        uint3 m_offset;                                      //!< Offset of inner grid in array
        bool m_add_outer;                                    //!< True if outer ghost layer is added to inner cells

        std::set<unsigned int> m_neighbors;                  //!< List of unique neighbor ranks
        GPUArray<T> m_send_buf;                              //!< Send buffer
        GPUArray<T> m_recv_buf;
        GPUArray<unsigned int> m_send_idx;                   //!< Indices of grid cells in send buf
        GPUArray<unsigned int> m_recv_idx;                   //!< Indices of grid cells in recv buf
        std::map<unsigned int,unsigned int> m_begin;         //!< Begin offset of every rank in send/recv buf
        std::map<unsigned int,unsigned int> m_end;           //!< End offset of every rank in send/recv buf

        //! Initialize grid communication
        virtual void initGridComm();
    };

#endif // ENABLE_MPI
#endif // __COMMUNICATOR_GRID_H__