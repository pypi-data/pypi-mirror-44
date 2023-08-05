This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [6.0.1] - 2019-03-16
### Added
* Added send message input in cortex ActionsClient.

## [6.0.0] - 2019-03-11
### Changed
* `from_model` in `ActionBuilder` is no longer limited to scikit-learn models. 
  
  `from_model` used to only support scikit-learn models, and it implicitly installed scikit-learn as a dependency. The method no longer does so and the user is required to add dependencies explicitly via `with_requirements()`. e.g., 
  ```
  builder.action('kaggel/ames-housing-predict') \
    .with_requirements(['scikit-learn>=0.20.0,<1']) \
    .from_model(model, x_pipeline=x_pipe, y_pipeline=y_pipe, target='SalePrice') \
    .build()
  ```


## [5.6.0] - 2019-02-27
### Added

* Added notebook with a deployment example
* New `Cortex.login()` method for interactive (prompt based) login to Cortex.

## [5.5.4] - 2019-02-08
### Added

* `Client.message()` Message constructor method.
* Bug fixes for experiments & runs

## [5.5.3] - 2019-01-31
### Added

* Jupyter notebook example for experiments
* `ActionBuilder.from_model()` now sets numpy dependency to range `>=1.16,<2`


## [5.5.1] - 2019-01-24
### Added

* ConnectionsClient: Added retry logic for `upload`, `uploadStreaming` and `download`.
* Jupyter notebook examples for pipelines and datasets

### Changed

* Namespace validation on resource creation. You must specify a namespace when creating:
    * datasets
    * skills
    * actions
    * connections
* `RemoteRun.get_artifact()` now returns a deserialized object by default, instead of the serialized object. The function now also has an optional `deserializer` parameter.


### Removed
