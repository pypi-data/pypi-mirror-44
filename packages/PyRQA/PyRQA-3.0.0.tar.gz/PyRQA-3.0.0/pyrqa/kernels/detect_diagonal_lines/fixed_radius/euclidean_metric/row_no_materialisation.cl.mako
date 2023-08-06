/*
Author: Tobias Rawald
Copyright 2015, 2018, 2019 The PyRQA project
Credits: Tobias Rawald, Mike Sips
License: Apache-2.0
Maintainer: Tobias Rawald
Email: pyrqa@gmx.net
Status: Development
*/

#ifdef cl_khr_fp16
    #pragma OPENCL EXTENSION cl_khr_fp16 : enable
#endif

#ifdef cl_khr_fp64
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#endif

#ifdef cl_nv_pragma_unroll
   #pragma OPENCL EXTENSION cl_nv_pragma_unroll : enable
#endif

__kernel void detect_diagonal_lines_symmetric(
    __global const ${fp_type}* vectors_x,
    __global const ${fp_type}* vectors_y,
    const uint dim_x,
    const uint dim_y,
    const uint start_x,
    const uint start_y,
    const uint m,
    const ${fp_type} e,
    const uint w,
    const uint offset,
    __global uint* frequency_distribution,
    __global uint* carryover
)
{
    uint global_id_x = get_global_id(0);

    uint id_x = global_id_x + offset;
    uint id_y = 0;

    if (id_x < dim_x && abs_diff(start_x + id_x, start_y + id_y) >= w)
    {
        ${fp_type} diff;
        ${fp_type} sum;

        uint carryover_id = id_x;
        if (offset > 0)
        {
            carryover_id = dim_x - id_x;
        }

        uint buffer = carryover[carryover_id];

        #pragma unroll loop_unroll
        for (;id_x < dim_x && id_y < dim_y;)
        {
            sum = 0.0f;
            for (uint i = 0; i < m; ++i)
            {
                diff = vectors_x[(id_x * m) + i] - vectors_y[(id_y * m) + i];
                sum += diff * diff;
            }

            if (sum < e*e)
            {
                buffer++;
            }
            else
            {
                if(buffer > 0)
                {
                    atomic_inc(&frequency_distribution[buffer - 1]);
                }

                buffer = 0;
            }

            id_x++;
            id_y++;
        }

        carryover[carryover_id] = buffer;
    }
}
