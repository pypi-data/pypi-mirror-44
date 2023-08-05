# microcosm-sagemaker
Opinionated machine learning with SageMaker

## Usage
After creating a new model, there are a few steps to integrate with microcosm-sagemaker.

1. Create a training graph

   The training graph holds the dependencies that are required at train time.  These typically include the bundles you have defined or any related helper functions.

   ```py
   from microcosm_sagemaker.loaders import load_train_conventions

   def create_app(debug=False, testing=False, extra_config={}):
       config_loader = load_each(
           load_from_dict(extra_config),
           load_from_environ,
           load_train_conventions,
       )

       graph = create_object_graph(
           name="my model",
       )

       graph.use(
           "active_bundle",
           "my_primary_bundle",
       )

       return graph.lock()
   ```

2. Create a service graph.

   The service graph holds the dependencies that are required at service time.  These typically include Flask and the web service routes.

   ```py
   from microcosm_sagemaker.loaders import load_model_artifact_config

   def create_app(artifact_path, debug=False, testing=False, model_only=False, extra_config={}):
       loader = load_each(
           load_model_artifact_config(artifact_path),
       )

       graph = create_object_graph(
           name="my model",
       )

       graph.use(
           "active_bundle",
           "active_evaluation",
       )

       if not model_only:
           graph.use(
               "my_primary_bundle",
               "my_primary_evaluator",
           )

       return graph.lock()
   ```

3. Expose the graphs in `setup.py`.

   ```py
   setup(
       name="my_model",
       entry_points={
           "microcosm_sagemaker.app_hooks": [
               "train = my_model.train.app:create_app",
               "serve = my_model.serve.app:create_app",
           ],
       },
   )
   ```
