define(['base/js/namespace'], function(IPython){
    console.log("Kernel event handler loaded")
    $([IPython.events]).on('kernel_ready.Kernel', function() {
        IPython.notebook.kernel.execute(`import os; os.environ['AZUREML_NB_PATH'] = '${IPython.notebook.notebook_path}'; import azureml.contrib.notebook.run;`)
    });
    return {onload:function() {console.log("Setting up kernel event handler: %o",IPython)}}
})