# Getting Started

First, create your topic schemas in the [topics](./topics/topics.json) file.  An example is already provided.

Next, create sample inputs.  An example sample input is provided in the [example](./samples/example.json) file.  

Next, edit the [process](./process.py) file which takes an array of inputs (one for each topic) and outputs a single dataframe.  Adjust the logic to match your needs.

Once you are ready to test your code, run the "Run spark streaming job" by going to Terminal -> Run Task -> Run spark streaming job.  This job will create your topic folders and watch for changes.  

Finally, move or copy your sample inputs into the appropriate topic folders created in the previous step.  The output will be printed to the console.  

You can add as many samples as you want.  Any new samples will be automatically picked up by the streaming job.  If the spark streaming job is stopped (by hitting `ctrl+c` in the terminal) or errors, you can restart the "Run spark streaming job".  This will automatically rename every file in order to force the spark streaming job to notice previous files.  If you need to update your [process](./process.py) code, you will need to restart the "Run spark streaming job" in order for it to recognize your changes.

# Taking code to production

First, you will need to edit the contents of [configuration](./config/config.yml).  This will specify your confluent kafka settings as well as several other configuration items for you job.  

Once you are satisfied with your code, you can run the "Save inputs and outputs" task.  This will automatically re-run all your samples and generate the output into memory.  You can check the console to make sure that the output is what you expected.  By default, the "Save inputs and outputs" task will only print out your results.  However, if you supply your StreamState token as described [here](https://github.com/StreamState/terraform-k8s-configuration#deploy-workflow), then the job will automatically push your code to the StreamState server which will run tests, lint your code, and deploy your streaming job.

Of course, you can also set up your CI/CD pipeline to run this and push the code so that full provenance is retained.  

