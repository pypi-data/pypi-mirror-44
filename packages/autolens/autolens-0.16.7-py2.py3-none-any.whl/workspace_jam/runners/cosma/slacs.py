from autofit import conf
from autofit.tools import path_util
from autolens.data import ccd
from autolens.data.array.util import array_util
from autolens.data.plotters import ccd_plotters

import os
import sys

### NOTE - if you have not already, complete the setup in 'workspace/runners/cosma/setup' before continuing with this
### cosma pipeline script.

# Welcome to the Cosma pipeline runner. Hopefully, you're familiar with runners at this point, and have been using them
# with PyAutoLens to model lenses on your laptop. If not, I'd recommend you get used to doing that, before trying to
# run PyAutoLens on a super-computer. You need some familiarity with the software and lens modeling before trying to
# model a large sample of lenses on a supercomputer!

# If you are ready, then let me take you through the Cosma runner. It is remarkably similar to the ordinary pipeline
# runners you're used to, however it makes a few changes for running jobs on cosma:

# 1) The data path is over-written to the path '/cosma5/data/durham/cosma_username/autolens/data' as opposed to the
#    workspace. As we saw in the setup, on cosma we don't store our data in our workspace.

# 2) The output path is over-written to the path '/cosma5/data/durham/cosma_username/autolens/output' as opposed to
#    the workspace. This is for the same reason as the data.

# Given your username is where your data is stored, you'll need to put your cosma username here.
cosma_username = 'pdtw24'

# The path where data and output are stored on cosma
cosma_path = '/cosma5/data/autolens/'

# Get the relative path to the config files and output folder in our workspace.
workspace_path = '{}/../'.format(os.path.dirname(os.path.realpath(__file__)))

# Use this path to explicitly set the config path, and override the output path with the Cosma path.
conf.instance = conf.Config(config_path=workspace_path + 'config', output_path=cosma_path + '/output_' + cosma_username)

# Lets take a look at a Cosma batch script, which can be found at 'workspace/runners/cosma/batch/pipeline_runner_cosma'.
# When we submit a PyAutoLens job to Cosma, we submit a 'batch' of jobs, whereby each job will run on one CPU of Cosma.
# Thus, if our lens sample contains, lets say, 17 lenses, we'd submit 17 jobs at the same time where each job applies
# our pipeline to each image.

# The fifth line of this batch script - '#SBATCH --array=1-17' is what species this. Its telling Cosma we're going to
# run 17 jobs, and the id's of those jobs will be numbered from 1 to 17. Infact, these ids are passed to this runner,
# and we'll use them to ensure that each jobs loads a different image. Lets get the cosma array id for our job.
cosma_array_id = int(sys.argv[1])

# Now, I just want to really drive home what the above line is doing. For every job we run on Cosma, the cosma_array_id
# will be different. That is, job 1 will get a cosma_array_id of 1, job 2 will get an id of 2, and so on. This is our
# only unique identifier of every job, thus its our only hope of specifying for each job which image they load!

# Fortunately, we're used to specifying the lens name as a string, so that our pipeline can be applied to multiple
# images with ease. On Cosma, we can apply the same logic, but put these strings in a list such that each Cosma job
# loads a different lens name based on its ID. neat, huh?

data_type = 'slacs'

data_name = []
data_name.append('') # Task number beings at 1, so keep index 0 blank
data_name.append('slacs0216-0813') # Index 1
data_name.append('slacs0252+0039') # Index 2
data_name.append('slacs0737+3216') # Index 3
data_name.append('slacs0912+0029') # Index 4
data_name.append('slacs0959+4410') # Index 5
data_name.append('slacs0959+4416') # Index 6
data_name.append('slacs1011+0143') # Index 7
data_name.append('slacs1205+4910') # Index 8
data_name.append('slacs1250+0523') # Index 9
data_name.append('slacs1402+6321') # Index 10
data_name.append('slacs1420+6019') # Index 11
data_name.append('slacs1430+4105') # Index 12
data_name.append('slacs1627+0053') # Index 13
data_name.append('slacs1630+4520') # Index 14
data_name.append('slacs2238-0754') # Index 15
data_name.append('slacs2300+0022') # Index 16
data_name.append('slacs2303+1422') # Index 17

data_name = data_name[cosma_array_id]

pixel_scale = 0.03 # Make sure your pixel scale is correct!

# We now use the lens_name list to load the image on each job, noting that in this example I'm assuming our lenses are
# on the Cosma data directory folder called 'slacs'
data_path = path_util.make_and_return_path_from_path_and_folder_names(
    path=cosma_path, folder_names=['data_share', data_type, data_name])

ccd_data = ccd.load_ccd_data_from_fits(image_path=data_path + 'F814W_image.fits',
                                       psf_path=data_path + 'F814W_psf.fits',
                                       noise_map_path=data_path + 'F814W_noise_map.fits',
                                       pixel_scale=pixel_scale, resized_ccd_shape=(301, 301),
                                       resized_psf_shape=(15, 15))

# ccd_plotters.plot_ccd_subplot(ccd_data=ccd_data)

# Running a pipeline is exactly the same as we're used to. We import it, make it, and run it, noting that we can
# use the lens_name's to ensure each job outputs its results to a different directory.

from workspace_jam.pipelines import lens_light_and_source_inversion

pipeline = lens_light_and_source_inversion.make_pipeline(phase_folders=[data_type, data_name])

pipeline.run(data=ccd_data)

# Finally, its worth us going through a batch script in detail, line by line, as you may we need to change different
# parts of this script to use different runners. Therefore, checkout the 'doc' file in the batch folder.