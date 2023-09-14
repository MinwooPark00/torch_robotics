import numpy as np
import torch
from matplotlib import pyplot as plt

from torch_robotics.environments.env_base import EnvBase
from torch_robotics.environments.primitives import ObjectField, MultiSphereField, MultiBoxField
from torch_robotics.environments.utils import create_grid_spheres
from torch_robotics.robots import RobotPointMass
from torch_robotics.torch_utils.torch_utils import DEFAULT_TENSOR_ARGS
from torch_robotics.visualizers.planning_visualizer import create_fig_and_axes


class EnvNarrowPassageDense2D(EnvBase):

    def __init__(self,
                 name='EnvDense2D',
                 tensor_args=None,
                 **kwargs
                 ):
        # Old object placements
        obj_list = [
            MultiSphereField(
                np.array([
                    [0.3313474655151367, 0.6288051009178162],
                    [-0.36961784958839417, -0.12315540760755539],
                    [-0.8740217089653015, -0.4034936726093292],
                    [0.808782160282135, 0.5287870168685913],
                    [0.6775968670845032, 0.8817358016967773],
                    [-0.3608766794204712, 0.8313458561897278],
                    [0.7156378626823425, -0.6923345923423767],
                    [0.35, 0],
                 ]),
                np.array([
                    0.125,
                    0.125,
                    0.125,
                    0.125,
                    0.125,
                    0.125,
                    0.125,
                    0.125,
                 ])
                ,
                tensor_args=tensor_args
            ),
            MultiBoxField(
                np.array([
                    [0.607781708240509, 0.19512386620044708],
                    [-0.3352295458316803, -0.6887519359588623],
                    [-0.6572632193565369, 0.41827881932258606],
                    [-0.664594292640686, 0.016457155346870422],
                    [0.8165988922119141, -0.19856023788452148],
                    [-0.8222246170043945, -0.6448580026626587],
                    [-0.8946458101272583, 0.8962447643280029],
                    [-0.23994405567646027, 0.6021060943603516],
                    [0.305103600025177, -0.3661990463733673],
                    [0., 0.5+0.05],
                    [0., -0.5-0.05],
                 ]),
                np.array([
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.20000000298023224, 0.20000000298023224],
                    [0.2, 1.0-0.05/2],
                    [0.2, 1.0-0.05/2],
                 ])
                ,
                tensor_args=tensor_args
                )
        ]

        super().__init__(
            name=name,
            limits=torch.tensor([[-1, -1], [1, 1]], **tensor_args),  # environments limits
            obj_fixed_list=[ObjectField(obj_list, 'dense2d')],
            tensor_args=tensor_args,
            **kwargs
        )

    def get_rrt_connect_params(self, robot=None):
        params = dict(
            n_iters=10000,
            step_size=0.01,
            n_radius=0.3,
            n_pre_samples=50000,
            max_time=15
        )

        if isinstance(robot, RobotPointMass):
            return params
        else:
            raise NotImplementedError

    def get_gpmp2_params(self, robot=None):
        params = dict(
            n_support_points=64,
            dt=0.04,
            opt_iters=300,
            num_samples=64,
            sigma_start=1e-5,
            sigma_gp=1e-2,
            sigma_goal_prior=1e-5,
            sigma_coll=1e-5,
            step_size=5e-1,
            sigma_start_init=1e-4,
            sigma_goal_init=1e-4,
            sigma_gp_init=0.2,
            sigma_start_sample=1e-4,
            sigma_goal_sample=1e-4,
            solver_params={
                'delta': 1e-2,
                'trust_region': True,
                'method': 'cholesky',
            },
        )

        if isinstance(robot, RobotPointMass):
            return params
        else:
            raise NotImplementedError


if __name__ == '__main__':
    env = EnvNarrowPassageDense2D(
        precompute_sdf_obj_fixed=True,
        sdf_cell_size=0.005,
        tensor_args=DEFAULT_TENSOR_ARGS
    )
    fig, ax = create_fig_and_axes(env.dim)
    env.render(ax)
    plt.show()

    # Render sdf
    fig, ax = create_fig_and_axes(env.dim)
    env.render_sdf(ax, fig)

    # Render gradient of sdf
    env.render_grad_sdf(ax, fig)
    plt.show()
